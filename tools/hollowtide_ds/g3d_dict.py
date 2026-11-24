#!/usr/bin/env python3
"""Dicionarios de nomes dos arquivos G3D da Nintendo (NSBMD/NSBTX): leitura e construcao byte a byte.

Formato conferido nos 4056 dicionarios dos 676 modelos de mapa do HeartGold:
  u8 0, u8 n, u16 tamanho_total, u16 8 (inicio da arvore), u16 inicio_das_entradas
  arvore PATRICIA: (n+1) nos de 4 bytes (bit de referencia, filho esquerdo, filho direito, indice da entrada);
     o no 0 e a raiz (bit 127); o no i+1 e o da entrada i. Bits contados do byte 0, bit menos significativo primeiro.
  entradas: u16 tamanho_da_unidade, u16 inicio_dos_nomes (a partir do bloco de entradas), n * unidade, n nomes de 16 bytes.
Conferido: com a ordem de insercao gravada no arquivo, tree() reproduz byte a byte os 3380 dicionarios nao vazios dos
676 modelos; com a ordem padrao (insertion_order), a busca acha todos os nomes nos 3380 (a forma de uma arvore
PATRICIA e unica; a ordem so muda a numeracao dos nos e qual entrada cada no guarda).
"""
import struct


def bit(name, b):
    return (name[b >> 3] >> (b & 7)) & 1


def tree(names, order=None):
    """Nos (bit, esquerda, direita, entrada) da arvore PATRICIA da Nintendo. A insercao segue `order` (indices); o
    padrao e o do conversor da Nintendo, conferido nos dicionarios da ROM (ver insertion_order)."""
    nodes = [[127, 0, 0, 0]]
    for i in (order if order is not None else insertion_order(names)):
        key = names[i]
        # busca: o no folha mais proximo (para quando o link aponta para cima)
        p, c = 0, nodes[0][1]
        while nodes[c][0] < nodes[p][0]:
            p, c = c, (nodes[c][2] if bit(key, nodes[c][0]) else nodes[c][1])
        other = names[nodes[c][3]] if c != 0 else bytes(16)
        d = 127
        while d >= 0 and bit(key, d) == bit(other, d):
            d -= 1
        # insercao: desce enquanto o bit do filho for maior que d e o link for para baixo
        p, c = 0, nodes[0][1]
        side = 1
        while nodes[c][0] < nodes[p][0] and nodes[c][0] > d:
            p = c
            side = 2 if bit(key, nodes[c][0]) else 1
            c = nodes[c][side]
        new = len(nodes)
        node = [d, 0, 0, i]
        if bit(key, d):
            node[1], node[2] = c, new
        else:
            node[1], node[2] = new, c
        nodes.append(node)
        nodes[p][side if p != 0 else 1] = new
    return nodes


def insertion_order(names):
    """Ordem de insercao: nome como inteiro de 128 bits (byte 0 menos significativo), do maior para o menor."""
    return sorted(range(len(names)), key=lambda i: int.from_bytes(names[i], "little"), reverse=True)


def build(names, data, unit, order=None):
    """Dicionario completo. names: str (ate 16), data: lista de bytes de tamanho unit; order: ordem de insercao
    (a do arquivo original, para conferir byte a byte; None = padrao)."""
    raw = [n.encode("ascii").ljust(16, b"\0") for n in names]
    nodes = tree(raw, order)
    n = len(names)
    tree_b = b"".join(struct.pack("<4B", *nd) for nd in nodes)
    ofs_entry = 8 + len(tree_b)
    entries = struct.pack("<HH", unit, 4 + unit * n) + b"".join(data) + b"".join(raw)
    size = ofs_entry + len(entries)
    return struct.pack("<BBHHH", 0, n, size, 8, ofs_entry) + tree_b + entries


def read(b, base=0):
    """(nomes, dados, unidade) de um dicionario em b[base:]."""
    n = b[base + 1]
    ofs_entry = struct.unpack_from("<H", b, base + 6)[0]
    e = base + ofs_entry
    unit, ofs_names = struct.unpack_from("<HH", b, e)
    data = [bytes(b[e + 4 + unit * i:e + 4 + unit * (i + 1)]) for i in range(n)]
    names = [bytes(b[e + ofs_names + 16 * i:e + ofs_names + 16 * (i + 1)]).rstrip(b"\0").decode("ascii") for i in range(n)]
    return names, data, unit


def read_order(b, base=0):
    """Ordem de insercao gravada num dicionario (a entrada de cada no, na ordem dos nos)."""
    n = b[base + 1]
    return [b[base + 8 + 4 * k + 3] for k in range(1, n + 1)]
