// Hollowtide QA: runner headless sobre a libmgba para testes in-game reproduziveis.
// Le um roteiro (um comando por linha) e executa no ROM:
//   wait N                 avanca N frames sem botoes
//   press KEYS N [M]       segura KEYS (ex.: A, UP, A+B) por N frames, depois solta por M (padrao 8)
//   walk DIR N             anda N tiles (DIR = UP/DOWN/LEFT/RIGHT), 16 frames por tile + 4 de folga
//   mash KEY N             aperta e solta KEY N vezes (para avancar dialogos)
//   shot arquivo.png       salva a tela (240x160)
//   pos                    imprime grupo/numero do mapa e coordenadas do jogador
//   expect_map G N         falha (exit 2) se o mapa atual nao for G.N
//   expect_pos X Y         falha (exit 2) se o jogador nao estiver em X,Y
//   peek ENDERECO_HEX N    imprime N palavras de 32 bits da memoria
//   setflag OFF FLAG       liga FLAG (hex) no SaveBlock1, OFF = offsetof(SaveBlock1, flags) (QA)
//   poke8 ADDR VAL         escreve um byte na memoria (QA)
//   setvar OFF VAR VAL     escreve uma var de script; OFF = offsetof(SaveBlock1, vars) (QA)
//   savestate arq / loadstate arq
// Uso: mgba_runner rom.gba roteiro.txt [save.sav] [endereco_hex_gSaveBlock1Ptr]
#include <mgba/core/core.h>
#include <mgba/core/serialize.h>
#include <mgba-util/vfs.h>
#include <png.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <stdarg.h>
#include <mgba/core/log.h>

static void quietLog(struct mLogger *l, int cat, enum mLogLevel lvl, const char *fmt, va_list args)
{
    (void)l; (void)cat; (void)lvl; (void)fmt; (void)args;
}
static struct mLogger sQuiet = { .log = quietLog };

static struct mCore *core;
static color_t *fb;
static unsigned stride;
static uint32_t sb1ptrAddr;
static unsigned long frameCount;

static int keyBit(const char *k)
{
    static const char *names[] = { "A", "B", "SELECT", "START", "RIGHT", "LEFT", "UP", "DOWN", "R", "L" };
    for (int i = 0; i < 10; i++)
        if (!strcmp(k, names[i]))
            return 1 << i;
    fprintf(stderr, "tecla desconhecida: %s\n", k);
    exit(1);
}

static int parseKeys(char *s)
{
    int keys = 0;
    for (char *t = strtok(s, "+"); t; t = strtok(NULL, "+"))
        keys |= keyBit(t);
    return keys;
}

static void run(int frames, int keys)
{
    core->setKeys(core, keys);
    for (int i = 0; i < frames; i++, frameCount++)
        core->runFrame(core);
    core->setKeys(core, 0);
}

static void shot(const char *path)
{
    unsigned w, h;
    core->desiredVideoDimensions(core, &w, &h);
    FILE *f = fopen(path, "wb");
    if (!f) { perror(path); exit(1); }
    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    png_infop info = png_create_info_struct(png);
    png_init_io(png, f);
    png_set_IHDR(png, info, w, h, 8, PNG_COLOR_TYPE_RGB, PNG_INTERLACE_NONE,
                 PNG_COMPRESSION_TYPE_DEFAULT, PNG_FILTER_TYPE_DEFAULT);
    png_write_info(png, info);
    unsigned char *row = malloc(w * 3);
    for (unsigned y = 0; y < h; y++) {
        for (unsigned x = 0; x < w; x++) {
            uint32_t c = fb[y * stride + x];
            row[x * 3 + 0] = c & 0xFF;
            row[x * 3 + 1] = (c >> 8) & 0xFF;
            row[x * 3 + 2] = (c >> 16) & 0xFF;
        }
        png_write_row(png, row);
    }
    png_write_end(png, NULL);
    png_destroy_write_struct(&png, &info);
    free(row);
    fclose(f);
}

// SaveBlock1: pos (s16 x, s16 y) no offset 0; location (s8 grupo, s8 numero, ...) no offset 4.
static void readPos(int *g, int *n, int *x, int *y)
{
    uint32_t sb1 = core->busRead32(core, sb1ptrAddr);
    *x = (int16_t)core->busRead16(core, sb1 + 0);
    *y = (int16_t)core->busRead16(core, sb1 + 2);
    *g = (int8_t)core->busRead8(core, sb1 + 4);
    *n = (int8_t)core->busRead8(core, sb1 + 5);
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "uso: %s rom.gba roteiro.txt [save.sav] [gSaveBlock1Ptr_hex]\n", argv[0]);
        return 1;
    }
    mLogSetDefaultLogger(&sQuiet);
    core = mCoreFind(argv[1]);
    if (!core || !core->init(core)) { fprintf(stderr, "falha ao iniciar core\n"); return 1; }
    mCoreInitConfig(core, NULL);
    unsigned w, h;
    core->desiredVideoDimensions(core, &w, &h);
    stride = w;
    fb = calloc(w * h, sizeof(color_t));
    core->setVideoBuffer(core, fb, stride);
    if (!mCoreLoadFile(core, argv[1])) { fprintf(stderr, "falha ao carregar ROM\n"); return 1; }
    if (argc > 3 && strcmp(argv[3], "-")) {
        struct VFile *sv = VFileOpen(argv[3], O_CREAT | O_RDWR);
        if (!sv || !core->loadSave(core, sv)) { fprintf(stderr, "falha ao abrir save\n"); return 1; }
    }
    if (argc > 4)
        sb1ptrAddr = strtoul(argv[4], NULL, 16);
    core->reset(core);

    FILE *sc = fopen(argv[2], "r");
    if (!sc) { perror(argv[2]); return 1; }
    char line[256];
    int lineNo = 0;
    while (fgets(line, sizeof(line), sc)) {
        lineNo++;
        char *hash = strchr(line, '#');
        if (hash) *hash = 0;
        char cmd[32] = "", a[128] = "", b[64] = "", c[64] = "";
        if (sscanf(line, "%31s %127s %63s %63s", cmd, a, b, c) < 1)
            continue;
        if (!strcmp(cmd, "wait")) {
            run(atoi(a), 0);
        } else if (!strcmp(cmd, "press")) {
            run(atoi(b), parseKeys(a));
            run(c[0] ? atoi(c) : 8, 0);
        } else if (!strcmp(cmd, "walk")) {
            int k = keyBit(a);
            for (int i = 0; i < atoi(b); i++)
                run(16, k);
            run(4, 0);
        } else if (!strcmp(cmd, "mash")) {
            int k = keyBit(a);
            for (int i = 0; i < atoi(b); i++) { run(4, k); run(12, 0); }
        } else if (!strcmp(cmd, "shot")) {
            shot(a);
            printf("[%lu] shot %s\n", frameCount, a);
        } else if (!strcmp(cmd, "pos") || !strcmp(cmd, "expect_map") || !strcmp(cmd, "expect_pos")) {
            int g, n, x, y;
            if (!sb1ptrAddr) { fprintf(stderr, "linha %d: pos requer endereco gSaveBlock1Ptr\n", lineNo); return 1; }
            readPos(&g, &n, &x, &y);
            printf("[%lu] mapa %d.%d pos %d,%d\n", frameCount, g, n, x, y);
            if (!strcmp(cmd, "expect_map") && (g != atoi(a) || n != atoi(b))) {
                printf("FALHA linha %d: esperado mapa %s.%s\n", lineNo, a, b);
                return 2;
            }
            if (!strcmp(cmd, "expect_pos") && (x != atoi(a) || y != atoi(b))) {
                printf("FALHA linha %d: esperado pos %s,%s\n", lineNo, a, b);
                return 2;
            }
        } else if (!strcmp(cmd, "peek")) {
            // peek ENDERECO_HEX N : imprime N palavras de 32 bits
            uint32_t addr = strtoul(a, NULL, 16);
            printf("[%lu] peek %08x:", frameCount, addr);
            for (int i = 0; i < atoi(b); i++)
                printf(" %08x", core->busRead32(core, addr + 4 * i));
            printf("\n");
        } else if (!strcmp(cmd, "setflag")) {
            // setflag OFFSET_FLAGS_HEX FLAG_HEX : liga uma flag no SaveBlock1 (somente para QA de transicoes)
            uint32_t sb1 = core->busRead32(core, sb1ptrAddr);
            uint32_t off = strtoul(a, NULL, 16), flag = strtoul(b, NULL, 16);
            uint32_t addr = sb1 + off + flag / 8;
            core->busWrite8(core, addr, core->busRead8(core, addr) | (1 << (flag % 8)));
            printf("[%lu] setflag 0x%x\n", frameCount, flag);
        } else if (!strcmp(cmd, "poke8")) {
            // poke8 ENDERECO_HEX VALOR : escreve um byte (QA)
            core->busWrite8(core, strtoul(a, NULL, 16), strtoul(b, NULL, 0));
        } else if (!strcmp(cmd, "setvar")) {
            // setvar OFFSET_VARS_HEX VAR_HEX VALOR : escreve uma var de script no SaveBlock1 (QA)
            uint32_t sb1 = core->busRead32(core, sb1ptrAddr);
            uint32_t var = strtoul(b, NULL, 16);
            core->busWrite16(core, sb1 + strtoul(a, NULL, 16) + 2 * (var - 0x4000), strtoul(c, NULL, 0));
        } else if (!strcmp(cmd, "savestate") || !strcmp(cmd, "loadstate")) {
            int save = !strcmp(cmd, "savestate");
            struct VFile *vf = VFileOpen(a, save ? (O_CREAT | O_TRUNC | O_RDWR) : O_RDONLY);
            if (!vf) { fprintf(stderr, "linha %d: nao abriu %s\n", lineNo, a); return 1; }
            bool ok = save ? mCoreSaveStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC)
                           : mCoreLoadStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC);
            vf->close(vf);
            if (!ok) { fprintf(stderr, "linha %d: %s falhou\n", lineNo, cmd); return 1; }
        } else {
            fprintf(stderr, "linha %d: comando desconhecido %s\n", lineNo, cmd);
            return 1;
        }
    }
    printf("OK: roteiro concluido em %lu frames\n", frameCount);
    core->deinit(core);
    return 0;
}
