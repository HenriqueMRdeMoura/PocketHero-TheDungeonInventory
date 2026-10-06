import random
import os

# Vetores que armazenarão os itens do jogador e a fila de monstros.
mochila = []
monstros = []

# Variáveis com atributos do jogador.
player_hp = 100
player_gold = 50
player_armor = 0
player_class = ""
hp_perdido = 0

# Variáveis com atributos do jogo.
onda = 1
quantidade_monstros = 1

# Vetores com os possíveis itens da loja
estoque_armas = ["Wooden Sword", "Stone Sword", "Iron Sword", "Diamond Sword", "Soul Reaver",
                 "Wooden Bow", "Hunter Bow", "Bone Bow", "Shadow Bow", "Soulseeker",
                 "Wooden Axe", "Stone Axe", "Iron Axe", "Diamond Axe", "Soul Cleaver"]
estoque_comidas = ["Cookie", "Bread", "Cake", "Apple Pie"]
estoque_armaduras = ["Leather Armor", "Chainmail Armor", "Bronze Armor", "Steel Armor", "Dragon's Scale Armor"]
id_armadura = 0
# Dicionário com todos os itens
tabela_itens = {
    # Espadas - Dano médio e durabilidade alta
    "Wooden Sword": {"preço": 5, "dano": 5, "durabilidade": 10, "tipo": "Sword"},
    "Stone Sword": {"preço": 20, "dano": 15, "durabilidade": 25, "tipo": "Sword"},
    "Iron Sword": {"preço": 40, "dano": 25, "durabilidade": 35, "tipo": "Sword"},
    "Diamond Sword": {"preço": 70, "dano": 35, "durabilidade": 50, "tipo": "Sword"},
    "Soul Reaver": {"preço": 250, "dano": 75, "durabilidade": 100, "tipo": "Sword"},
    # Arcos - Ataca 2x, mas consome 2 de durabilidade
    "Wooden Bow": {"preço": 5, "dano": 5, "durabilidade": 10, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Hunter Bow": {"preço": 30, "dano": 15, "durabilidade": 20, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Bone Bow": {"preço": 50, "dano": 25, "durabilidade": 30, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Shadow Bow": {"preço": 75, "dano": 30, "durabilidade": 40, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Soulseeker": {"preço": 250, "dano": 50, "durabilidade": 100, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    # Machados - Dano alto e durabilidade baixa
    "Wooden Axe": {"preço": 5, "dano": 10, "durabilidade": 5, "tipo": "Axe"},
    "Stone Axe": {"preço": 20, "dano": 25, "durabilidade": 15, "tipo": "Axe"},
    "Iron Axe": {"preço": 40, "dano": 35, "durabilidade": 25, "tipo": "Axe"},
    "Diamond Axe": {"preço": 70, "dano": 50, "durabilidade": 35, "tipo": "Axe"},
    "Soul Cleaver": {"preço": 250, "dano": 100, "durabilidade": 75, "tipo": "Axe"},
    # Drops de bosses - As mais fortes do jogo
    "Soul Reaper": {"dano": 250, "durabilidade": 250, "tipo": "Scythe", "descrição": "A arma definitiva dos deuses da morte."},
    "Vampiric Blade": {"dano": 50, "durabilidade": 20, "tipo": "Sword", "descrição": "Cura 5 de HP a cada golpe."},
    "Dragon Bow": {"dano": 50, "durabilidade": 10, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Alpha's Cleaver": {"dano": 75, "durabilidade": 15, "tipo": "Axe"},
    # Armaduras - Redução de dano sofrido
    "Leather Armor": {"preço": 25, "armadura": 5, "tipo": "Armor"},
    "Chainmail Armor": {"preço": 50, "armadura": 10, "tipo": "Armor"},
    "Bronze Armor": {"preço": 75, "armadura": 15, "tipo": "Armor"},
    "Steel Armor": {"preço": 100, "armadura": 25, "tipo": "Armor"},
    "Dragon's Scale Armor": {"preço": 150, "armadura": 50, "tipo": "Armor"},
    # Comidas - Cura vida
    "Cookie": {"preço": 5, "cura": 15},
    "Bread": {"preço": 15, "cura": 30},
    "Cake": {"preço": 25, "cura": 50},
    "Apple Pie": {"preço": 40, "cura": 75}
}
# Dicionário com todos os montros (bosses e minibosses não incluídos)
tabela_monstros = {
    "Esqueleto": {"hp": 40, "dano": 15, "ouro": 20},
    "Goblin": {"hp": 30, "dano": 10, "ouro": 15},
    "Lobo": {"hp": 20, "dano": 20, "ouro": 20},
    "Orc": {"hp": 60, "dano": 25, "ouro": 30},
    "Rato Gigante": {"hp": 15, "dano": 10, "ouro": 5},
    "Slime": {"hp": 25, "dano": 5, "ouro": 5},
    "Zumbi": {"hp": 30, "dano": 20, "ouro": 20}
}
# Dicionário com todos os minibosses
# Note for self: Ajustar os atributos dos minibosses
tabela_minibosses = {
    "Dragãozinho": {"hp": 75, "dano": 35, "ouro": 50},
    "Lobisomem": {"hp": 75, "dano": 35, "ouro": 50},
    "Vampiro": {"hp": 75, "dano": 35, "ouro": 50}
}
# Dicionário com todos os bosses
# Note for self: Ajustar os atributos dos bosses
tabela_bosses = {
    "Dragão": {"hp": 100, "dano": 50, "ouro": 100},
    "Lobisomem Alfa": {"hp": 100, "dano": 50, "ouro": 100},
    "Vampiro Rei": {"hp": 100, "dano": 50, "ouro": 100}
}
# Dicionário com o chefão final
tabela_bossfinal = {
    "The Soul Reaper": {"hp": 1000, "dano": 250, "ouro": 1000}
}
# Função para adicionar itens à mochila.
def adicionar_item_mochila(nome_item):
  if "dano" in tabela_itens[nome_item]: # Se for uma arma
    item_para_mochila = {
        "nome": nome_item,
        "durabilidade": tabela_itens[nome_item]["durabilidade"]
    }
    mochila.append(item_para_mochila)
  else: # Se for uma comida
    mochila.append({"nome": nome_item})

def limpar_tela():
  try:
    # Se estiver a rodar no Google Colab, usa a limpeza do Colab
    from google.colab import output
    output.clear()
  except ImportError:
    # Se estiver no terminal do computador (.py), usa o comando do sistema
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para selecionar a classe.
def escolher_classe():
  global player_hp, player_class

  # Menu de escolha de classes.
  print("="*41)
  print("|      ESCOLHA SUA CLASSE DE HERÓI       |")
  print("="*41)
  ## Warrior
  print("| [1]⚔️ Warrior 🛡️")
  print("|❤️ Vida inicial: 100 HP")
  print("|🎒 Arma inicial: Wooden Sword")
  print("|ℹ️ Habilidade Passiva: Começa com 5 de armadura. Aumenta em +5 a cada 10 ondas.")
  print("|✨ Habilidade Ativa: Retaliação de Escudo")
  print("|   Causa dano baseado em 2x a sua armadura total.")
  print("="*41)
  ## Archer
  print("| [2]🏹 Archer 🏹")
  print("|❤️ Vida inicial: 75 HP")
  print("|🎒 Arma inicial: Wooden Bow")
  print("|ℹ️ Habilidade Passiva: Arcos atiram 3 vezes, ainda gastando apenas 2 de durabilidade.")
  print("|✨ Habilidade Ativa: Chuva de Flechas")
  print("|   Dispara uma rajada de flechas causando 30 de dano por monstro na onda.")
  print("="*41)
  ## Berserker
  print("| [3]🪓 Berserker 🪓")
  print("|❤️ Vida inicial: 125 HP")
  print("|🎒 Arma inicial: Wooden Axe")
  print("|ℹ️ Habilidade Passiva: Aumenta o dano em 5 a cada 20 de HP perdido durante a luta.")
  print("|✨ Habilidade Ativa: Grito de Fúria")
  print("|   Aumenta a fúria em +5 de dano por monstro na onda.")
  print("="*41)

  while True:
    escolha = input("Digite o número da sua classe: ")

    # Se escolher 1, seleciona Warrior.
    if escolha == "1":
      player_class = "Warrior"
      player_hp = 100
      adicionar_item_mochila("Wooden Sword")
      print("\n⚔️ Você escolheu Warrior!🛡️ Pronto para proteger o reino.")
      return "Warrior"

    # Se escolher 2, seleciona Archer.
    elif escolha == "2":
      player_class = "Archer"
      player_hp = 75
      adicionar_item_mochila("Wooden Bow")
      print("\n🏹 Você escolheu Archer! Suas flechas vão chover sobre os monstros.")
      return "Archer"

    # Se escolher 3, seleciona Berserker.
    elif escolha == "3":
      player_class = "Berserker"
      player_hp = 125
      adicionar_item_mochila("Wooden Axe")
      print("\n🪓 Você escolheu Berserker! O sangue e a fúria guiam sua lâmina.")
      return "Berserker"

    else:
      print("⚠️ Opção inválida! Escolha 1, 2 ou 3.")

# Função para mostrar a mochila
def mostrar_mochila():
  if not mochila:
    print("\n🎒 Sua mochila está vazia!")
    return

  print("\n")
  print("=-"*15 + "=")
  print("       INVENTÁRIO DA MOCHILA")
  print("=-" * 15 + "=")

  for contador, item in enumerate(mochila, start=1):
    nome_item = item["nome"]

    # Verifica se o item é uma arma (se tem 'dano' na tabela)
    if "dano" in tabela_itens[nome_item]:
      tipo_arma = tabela_itens[nome_item]["tipo"]
      dano = tabela_itens[nome_item]["dano"]
      durabilidade = item["durabilidade"]

      print(f"| [{contador}] {nome_item} [{tipo_arma}]")
      print(f"| ⚔️ Dano: {dano} | 🛡️ Durabilidade: {durabilidade}")

      if "descrição" in tabela_itens[nome_item]:
        print(f"| ℹ️ {tabela_itens[nome_item]['descrição']}")

      # Se não for arma, é comida
    else:
      cura = tabela_itens[nome_item]["cura"]
      print(f"| [{contador}] {nome_item} [Comida]")
      print(f"| ❤️ Cura: {cura}")

    print("=-" * 15 + "=")
  input("\nPressione Enter para continuar...")

# Sistema da lojinha :D
def loja():
  global player_gold
  global player_armor
  global id_armadura
  while True:
    limpar_tela()
    print("="*40)
    print("Seja muito bem-vindo(a) à minha loja!")
    print("="*40,"\n")
    print(f"💰 Seu ouro atual: {player_gold} ouros.\n")

    # Soteia e define os itens da loja
    item1 = random.choice(estoque_armas)
    item2 = random.choice(estoque_comidas)
    preco1 = tabela_itens[item1]["preço"]
    preco2 = tabela_itens[item2]["preço"]

    # Verificação de segurança para o estoque de armaduras
    armadura_disponivel = id_armadura < len(estoque_armaduras)

    if armadura_disponivel:
      item3 = estoque_armaduras[id_armadura]
      preco3 = tabela_itens[item3]["preço"]
      valor_armadura = tabela_itens[item3]["armadura"]

    # Menu de escolha da loja
    print("=-=-"*7+"=")
    ## Arma
    print(f"| [1] {item1} ({tabela_itens[item1]['tipo']}) - {preco1} ouros.")
    print(f"| ⚔️ Dano: {tabela_itens[item1]['dano']}")
    print(f"| 🛡️ Durabilidade: {tabela_itens[item1]['durabilidade']}")
    if "descrição" in tabela_itens[item1]:
      print(f"| ℹ️ {tabela_itens[item1]['descrição']}")
    print("=-=-"*7+"=")
    ## Comida
    print(f"| [2] {item2} - {preco2} ouros.")
    print(f"| ❤️ Cura: {tabela_itens[item2]['cura']}")
    print("=-=-"*7+"=")
    ## Armadura
    if armadura_disponivel:
      print(f"| [3] {item3} - {preco3} ouros.")
      print(f"| 🛡️ Armadura: {valor_armadura}")
    else:
      print(f"| [3] Armadura Máxima Adquirida (Estoque Esgotado)")
    print("=-=-"*7+"=")
    print("| [0] Sair da loja.")
    print("=-=-"*7+"=\n")
    print("\n"*2)

    escolha = input("Escolha o número do item que deseja comprar (ou 0 para sair): ")
    # Se escolher 1, compra a arma.
    if escolha == "1":
      if player_gold >= preco1:
        player_gold -= preco1
        adicionar_item_mochila(item1)
        print(f"\nVocê comprou {item1} com sucesso!")
      else:
        print("\n❌ Você não tem ouro suficientes!")
    # Se escolher 2, compra a comida.
    elif escolha == "2":
      if player_gold >= preco2:
        player_gold -= preco2
        adicionar_item_mochila(item2)
        print(f"\nVocê comprou {item2} com sucesso!")
      else:
        print("\n❌ Você não tem ouro suficientes!")
    # Se escolher 3, compra a armadura.
    elif escolha == "3":
      if not armadura_disponivel:
        print("\n❌ Você já comprou todas as armaduras disponíveis na loja!")
      elif player_gold >= preco3:
        player_gold -= preco3
        adicionar_item_mochila(item3)
        id_armadura += 1
        print(f"\nVocê comprou {item3} com sucesso!")
        player_armor = tabela_itens[item3]["armadura"]
      else:
        print("\n❌ Você não tem ouro suficientes!")
    # Se escolher 0, sai da lojinha.
    elif escolha == "0":
      print("\nSaindo da loja...")
      print("Volte sempre!")
      break
    else:
      print("\n⚠️ Opção inválida. Tente novamente.")
      continue

    print(f"🎒 Mochila atual: {mochila}")
    print(f"💰 Ouros restantes: {player_gold} ouros.\n")
    input("Pressione Enter para continuar...")

# Função que define qual tabela usar pra geração de monstros dependendo da onda atual.
def obter_tabela_atual():
  if onda % 100 == 0:
    return tabela_bossfinal, "Boss Supremo"
  elif onda % 10 == 0:
    return tabela_bosses, "Boss"
  elif onda % 5 == 0:
    return tabela_minibosses, "Miniboss"
  else:
    return tabela_monstros, "Monstro"

def adicionar_monstro():
    # Define qual tabela e qual texto usar dependendo da onda atual
    tabela_atual, tipo = obter_tabela_atual()

    # Sorteia o monstro, pega os atributos da tabela escolhida e adiciona na fila
    novo_monstro = random.choice(list(tabela_atual.keys()))
    monstros.append(novo_monstro)

    hp = tabela_atual[novo_monstro]["hp"]
    dano = tabela_atual[novo_monstro]["dano"]
    ouro = tabela_atual[novo_monstro]["ouro"]

    # Aumenta o HP dos monstros ao passar das ondas
    if tipo in ["Miniboss", "Boss"]:
      hp *= quantidade_monstros
    elif tipo == "Monstro" and onda > 10:
      hp += (quantidade_monstros-1)*5

    # Aumenta o dano dos monstros ao passar das ondas
    if tipo == "Boss" and onda > 10:
      dano += (quantidade_monstros-1)*25
    elif tipo == "Miniboss" and onda > 10:
      dano += (quantidade_monstros-1)*10
    elif tipo == "Monstro" and onda > 10:
      dano += (quantidade_monstros-1)*5

    # Exibe o aviso na tela usando a variável 'tipo'
    if tipo == "Monstro":
      print(f"⚔️ Um {novo_monstro} (HP: {hp} | Dano: {dano} | Ouro: {ouro}) apareceu!")
    else:
      print(f"⚔️ O {tipo} {novo_monstro} (HP: {hp} | Dano: {dano} | Ouro: {ouro}) apareceu!")

def enfrentar_monstro():
    # Descobre qual tabela usar dependendo da onda atual
    tabela_atual, tipo = obter_tabela_atual()

    # Puxa os atributos usando a tabela escolhida
    if len(monstros) > 0:
      monstro_atual = monstros.pop(0)
      hp = tabela_atual[monstro_atual]["hp"]
      dano = tabela_atual[monstro_atual]["dano"]
      ouro = tabela_atual[monstro_atual]["ouro"]

        # Aumenta o HP dos monstros ao passar das ondas
      if tipo in ["Miniboss", "Boss"]:
        hp *= quantidade_monstros
      elif tipo == "Monstro" and onda > 10:
        hp += (quantidade_monstros-1)*5

      # Aumenta o dano dos monstros ao passar das ondas
      if tipo == "Boss" and onda > 10:
        dano += (quantidade_monstros-1)*25
      elif tipo == "Miniboss" and onda > 10:
        dano += (quantidade_monstros-1)*10
      elif tipo == "Monstro" and onda > 10:
        dano += (quantidade_monstros-1)*5

      print(f"\n⚔️ Combate iniciado contra o {tipo} {monstro_atual}!")
      print(f"   Status do Monstro -> HP: {hp}, Dano: {dano}")
      input("\nPressione Enter para iniciar o combate...")
      return monstro_atual
    else:
      print("\n🎉 A onda de monstros está vazia! O herói está seguro por enquanto.")
      return None

# Mochila: Armas
def mochila_armas():
  contador = 1
  print("\n")
  print("=-=-=-=-=-=-=-=-=-=-=")

  armas_na_mochila = [item for item in mochila if "durabilidade" in item]
  if not armas_na_mochila:
    return None

  for item in armas_na_mochila:
    nome_arma = item["nome"]
    tipo_arma = tabela_itens[nome_arma]["tipo"]
    print(f"| {contador} - {nome_arma} [{tipo_arma}]")
    print(f"| Dano: {tabela_itens[nome_arma]['dano']}")
    print(f"| Durabilidade: {item['durabilidade']}")
    if "descrição" in tabela_itens[nome_arma]:
      print(f"| ℹ️ {tabela_itens[nome_arma]['descrição']}")
    print("=-=-=-=-=-=-=-=-=-=-=")
    contador += 1

  try:
    acao = int(input("Digite o número da arma: "))
    if 1 <= acao <= len(armas_na_mochila):
      return armas_na_mochila[acao-1]
  except ValueError:
      pass
  return None

# Mochila: Comidas
def mochila_comidas():
  contador = 1
  print("\n")
  print("=-=-=-=-=-=-=-=-=-=-=")

  comidas_na_mochila = [item for item in mochila if "cura" in tabela_itens[item["nome"]]]
  if not comidas_na_mochila:
    return None

  for item in comidas_na_mochila:
    nome_comida = item["nome"]
    print(f"| {contador} - {nome_comida}")
    print(f"| Cura: {tabela_itens[nome_comida]['cura']}")
    print("=-=-=-=-=-=-=-=-=-=-=")
    contador += 1

  try:
    acao = int(input("Digite o número da comida: "))
    if 1 <= acao <= len(comidas_na_mochila):
      return comidas_na_mochila[acao - 1]
  except ValueError:
    pass
  return None

# O sistema de luta
def lutar():
  global player_hp
  global player_gold
  global player_armor
  global player_class
  global onda
  global quantidade_monstros
  global hp_perdido

  habilidade_disponivel = True

  # Warrior's ability check:
  armadura_atual = player_armor
  if player_class == "Warrior":
    armadura_atual += (quantidade_monstros * 5)

  # Continua lutando enquanto houver monstros na fila e o player estiver vivo
  while len(monstros) > 0 and player_hp > 0:

    # Descobre qual tabela usar dependendo da onda atual
    tabela_atual, tipo = obter_tabela_atual()

    # Puxa um monstro da lista
    monstro_atual = enfrentar_monstro()

    if not monstro_atual:
      return # Se não houver monstros, encerra a função lutar.
    # Pega os atributos na tabela correta definida acima.
    hp_monstro = tabela_atual[monstro_atual]["hp"]
    dano_monstro = tabela_atual[monstro_atual]["dano"]
    ouro_monstro = tabela_atual[monstro_atual]["ouro"]

    # Aumenta o HP dos monstros ao passar das ondas
    if tipo in ["Miniboss", "Boss"]:
      hp_monstro *= quantidade_monstros
    elif tipo == "Monstro" and onda > 10:
      hp_monstro += (quantidade_monstros-1)*5

    # Aumenta o dano dos monstros ao passar das ondas
    if tipo == "Boss" and onda > 10:
      dano_monstro += (quantidade_monstros-1)*25
    elif tipo == "Miniboss" and onda > 10:
      dano_monstro += (quantidade_monstros-1)*10
    elif tipo == "Monstro" and onda > 10:
      dano_monstro += (quantidade_monstros-1)*5

    # Registra o dano reduzido pela armadura
    dano_recebido = max(0, dano_monstro - armadura_atual)

    while hp_monstro > 0 and player_hp > 0:
      limpar_tela()
      # Menu da batalha
      print("\n" + "="*40)
      print(f"| ❤️ Seu HP: {player_hp} | 👾 HP do {monstro_atual}: {hp_monstro}")
      if player_class == "Warrior":
        print(f"| 🛡️ Sua armadura: {player_armor + (quantidade_monstros*5)}")
      else:
        print(f"| 🛡️ Sua armadura: {player_armor}")
      print("="*40)
      print("[1] Atacar")
      print("[2] Usar item de cura da mochila")
      print("[3] Usar Habilidade Especial")
      print("[0] Tentar fugir")

      acao = input("Escolha sua ação: ")

      ## Atacar
      if acao == "1":
        arma_escolhida = mochila_armas()
        if not arma_escolhida:
          print("\n❌ Nenhuma arma selecionada ou você não tem armas na mochila!")
          input("Pressione Enter para continuar...")
          continue
        # Pega o dano da arma e ataca
        nome_arma = arma_escolhida["nome"]
        tipo_arma = tabela_itens[nome_arma]["tipo"]
        dano_player = tabela_itens[nome_arma]["dano"]
        if player_class == "Berserker":
          furia = (hp_perdido // 20) * 5
          dano_player += furia
        if tipo_arma != "Bow":
          hp_monstro -= dano_player
          print(f"\n⚔️ Você atacou o {monstro_atual} com {nome_arma} e causou {dano_player} de dano!")
        else:
          disparos = 3 if player_class == "Archer" else 2
          hp_monstro -= dano_player*disparos
          print(f"\n⚔️ Você atacou o {monstro_atual} {disparos}x com {nome_arma} e causou {dano_player*disparos} de dano!")
        if nome_arma == "Vampiric Blade":
          player_hp += 5

        # Reduz a durabilidade da arma
        arma_escolhida["durabilidade"] -= 1
        if tipo_arma == "Bow":
          arma_escolhida["durabilidade"] = max(0, arma_escolhida["durabilidade"] - 1)
        print(f"⚠️ A durabilidade de {nome_arma} caiu para {arma_escolhida['durabilidade']}.")
        # Se a durabilidade zerar, a arma quebra e some da mochila
        if arma_escolhida["durabilidade"] <= 0:
          print(f"💥 {nome_arma} quebrou!")
          mochila.remove(arma_escolhida)
      ## Comer/Curar
      elif acao == "2":
        comida_escolhida = mochila_comidas()
        if not comida_escolhida:
          print("\n❌ Nenhuma comida selecionada ou você não tem comidas na mochila!")
          input("Pressione Enter para continuar...")
          continue

        nome_comida = comida_escolhida["nome"]
        cura_player = tabela_itens[nome_comida]["cura"]
        player_hp += cura_player
        mochila.remove(comida_escolhida)
        print(f"\n✨ Você comeu {nome_comida} e recuperou {cura_player} de HP! HP atual: {player_hp}")
      ## Habilidade Ativa
      elif acao == "3":
        if habilidade_disponivel:
          # Habilidade do Warrior.
          if player_class == "Warrior":
            dano_player = armadura_atual*2
            hp_monstro -= dano_player
            print(f"\n🛡️ Retaliação de Escudo! Você avança com o peso do seu escudo e causa {dano_player} de dano em {monstro_atual}!")
          # Habilidade do Archer.
          if player_class == "Archer":
            dano_player = 30*quantidade_monstros
            hp_monstro -= dano_player
            print(f"\n🏹 Chuva de Flechas! Você dispara uma rajada letal sobre o campo e causa {dano_player} de dano em {monstro_atual}!")
          # Habilidade do Berserker.
          if player_class == "Berserker":
            hp_perdido += 20*quantidade_monstros
            print(f"\n🪓 Grito de Fúria! O sangue em suas veias ferve, aumentando seu dano em +{5*quantidade_monstros} até o fim da onda!")
          habilidade_disponivel = False
        else:
          # Se a habilidade special já foi usada.
          print("\n⚠️ Você já gastou sua Habilidade Especial nesta onda!")
          input("Pressione Enter para continuar...")
          continue
      ## Fugir da luta.
      elif acao == "0":
        print("\n🏃 Você conseguiu fugir da batalha correndo perigosamente!")
        monstros.clear()
        return
      else:
        print("\n⚠️ Ação inválida! Escolha 1, 2 ou 0.")
        continue

      # Turno do monstro
      if hp_monstro > 0:
        player_hp -= dano_recebido
        hp_perdido += dano_recebido
        print(f"💥 O {monstro_atual} retaliou e te causou {dano_recebido} de dano!")

      input("\nPressione Enter para avançar o turno...")

    # Resultado do combate (Vitória ou derrota)
    if player_hp <= 0:
      print(f"\n💀 Você foi derrotado na onda {onda}... Fim de jogo no Pocket Hero!")
    elif hp_monstro <= 0:
      print(f"\n🎉 Vitória! Você derrotou o {monstro_atual}!")
      player_gold += ouro_monstro
      print(f"💰 Você ganhou {ouro_monstro} de ouro! Ouro total: {player_gold}")

      if monstro_atual == "The Soul Reaper":
        adicionar_item_mochila("Soul Reaper")
        print("☠️ A mítica Soul Reaper foi adicionada à sua mochila...")
      if monstro_atual == "Vampiro Rei":
        adicionar_item_mochila("Vampiric Blade")
        print("🧛 A lendária Vampiric Blade foi adicionada à sua mochila...")
      if monstro_atual == "Dragão":
        adicionar_item_mochila("Dragon Bow")
        print("🐉 O poderoso Dragon Bow foi adicionado à sua mochila...")
      if monstro_atual == "Lobisomem Alfa":
        adicionar_item_mochila("Alpha's Cleaver")
        print("🐺 O devastador Alpha's Cleaver foi adicionado à sua mochila...")

      # Verifica se o monstro derrotado foi um boss
      if onda % 10 == 0:
        quantidade_monstros += 1
        print(f"\n🔥 O Boss foi aniquilado! A masmorra enfureceu-se!")
        print(f"⚠️ ATENÇÃO: Agora hordas de {quantidade_monstros} monstros começarão a aparecer por onda!")

      input("\nPressione Enter para avançar o turno...")

  if player_hp > 0:
    # Reseta o hp_perdido pra habilidade do Berserker.
    # Avança a onda
    hp_perdido = 0
    onda += 1

def menu():
  # O menu do menu :D
  print("\n" + "="*41)
  print("|   Pocket Hero: The Dungeon Inventory")
  print("="*41)
  print("|        Seja Muito Bem-Vindo(a)")
  print("="*41)
  print(f"| ❤️ Seu HP: {player_hp}")
  print(f"| 💰 Seu ouro: {player_gold}")
  if player_class == "Warrior":
    print(f"| 🛡️ Sua armadura: {player_armor + (quantidade_monstros*5)}")
  else:
    print(f"| 🛡️ Sua armadura: {player_armor}")
  print("="*41)
  print(f"|                ONDA {onda}")
  print("|        O QUE VOCÊ DESEJA FAZER? ")
  print("="*41)
  print("| [1] Ir para a Loja")
  print("| [2] Enfrentar um Monstro")
  print("| [3] Ver mochila")
  print("| [0] Sair do Jogo")

  escolha_principal = input("Escolha: ")

  # Se escolher 1, vai pra lojinha :D
  if escolha_principal == "1":
    loja()
  # Se escolher 2, inicia a luta.
  elif escolha_principal == "2":
    if onda % 5 == 0:
      adicionar_monstro()
    else:
      for _ in range(quantidade_monstros):
        adicionar_monstro()
    lutar()
  # Se escolher 3, mostra os itens na mochila.
  elif escolha_principal == "3":
    mostrar_mochila()
  # Se escolher 0, o programa encerra.
  elif escolha_principal == "0":
    print("\n👋 Até a próxima aventura em Pocket Hero!")
    return False
  else:
    print("⚠️ Opção inválida!")
  return True

# O jogo em si
if __name__ == "__main__":
  # Chama a função pra escolher a classe.
  escolher_classe()
  # Adiciona 4 Cookies na mochila.
  for carlos in range(4):
    adicionar_item_mochila("Cookie")

  while player_hp > 0:
    limpar_tela()
    continuar = menu()
    if not continuar:
      break