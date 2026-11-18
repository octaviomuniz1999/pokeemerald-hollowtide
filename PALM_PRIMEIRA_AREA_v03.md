# Pokémon PALM — Primeira área jogável (v0.3)

**O QUE FOI ALTERADO DE VERDADE:**
- Vila Inicial usa temporariamente o layout de Littleroot; placa e nome de mapa alterados.
- Professor Alex aparece como nome da apresentação inicial, dos diálogos do laboratório e começo da aventura. **Sprite e retrato ainda são os do Birch**.
- Escolha de iniciais no motor trocada para **Snivy, Fennekin e Mudkip**.
- Rota 01 usa temporariamente o layout de Route 101. Diálogos e placas novos.
- Vila da Colheita usa temporariamente o layout de Oldale; casas, Centro Pokémon e mercado continuam jogáveis.
- A porta da segunda casa de Oldale (x=15, y=16) agora entra no Ginásio do Nevard.
- O ginásio usa temporariamente o mapa interno do Ginásio de Rustboro, com saída de volta para Colheita.
- Sprite de caminhada de Nevard (frente) substitui o NPC original da Roxanne no ginásio.
- Nevard mantém seu sprite de batalha **APROVADO** e sua equipe Shroomish 12 / Treecko 14.
- Três treinadores do ginásio trocaram Geodude por Pokémon de Grama.
- Diálogos de ginásio atualizados, recompensa mudou para **TM Bullet Seed**.

**O QUE AINDA É PROVISÓRIO:**
- Os mapas ainda NÃO são os desenhos 32x28, 30x52 e 44x36 planejados. Reutilizamos a malha e tiles do Emerald para demonstrar o caminho e os eventos.
- O evento inicial de resgate do professor, o rival, os sistemas de quests e os mapas além da vila ainda usam o roteiro do Emerald.
- O professor ainda tem a imagem/overworld original do Birch, só o nome nos diálogos iniciais mudou.
- A primeira insígnia usa mecanicamente a posição e o ícone de Stone Badge da ROM; os textos dizem "INSIGNIA COLHEITA".
- A Pokédex e a equipe do rival ainda têm componentes do Emerald que devem ser adequados aos novos iniciais.
- Não houve compilação GBA nesta máquina (falta toolchain ARM). O código e dados foram validados pelos utilitários disponíveis, mas a ROM v0.3 ainda precisa do teste no mGBA.

**TESTAR:**
1. Extraia o kit Windows v0.3, execute `COMPILAR_POKEMON_PALM.cmd` (mesmo processo que funcionou na v0.2).
2. Comece um novo save para testar os iniciais. A atualização do mapa e do ginásio pode funcionar em saves antigos, mas eventos de história dependem de flags existentes.
3. Da Vila Inicial (Littleroot) siga para norte pela Rota 01 (Route101), até a Vila da Colheita (Oldale).
4. Na Vila da Colheita, entre na **casa da direita, no sul da cidade**, que agora é o ginásio.
5. Enfrente os treinadores de Grama, o Nevard e ganhe a TM Bullet Seed.
6. Alternativamente, o menu de debug R + START, Trainers -> ID 265 -> Try Battle testa apenas o combate, sem roteiro, troféu ou recompensa.

**ATENÇÃO:** Não aplicar este ZIP com Floating IPS/Lunar IPS: é um código-fonte a compilar. Nenhum `.gba` foi incluído.
