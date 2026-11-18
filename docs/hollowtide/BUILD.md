# Build reproduzível — Hollowtide GBA

Ambiente verificado: Ubuntu 24.04, 4 núcleos.

```sh
sudo apt-get install -y build-essential libpng-dev gcc-arm-none-eabi \
    binutils-arm-none-eabi libnewlib-arm-none-eabi xdelta3
make -j$(nproc)          # gera pokeemerald.gba (não versionar)
sha256sum pokeemerald.gba
```

Patch para distribuição privada (nunca publicar a ROM):

```sh
xdelta3 -e -s <rom_base_declarada>.gba pokeemerald.gba hollowtide.xdelta
xdelta3 -d -s <rom_base_declarada>.gba hollowtide.xdelta teste.gba && sha256sum teste.gba
```
