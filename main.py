from funcoes import * # IMPORTA TODAS AS FUNÇÕES PARA O MAIN PRINCIPAL 

os.system("color 3") # MUDA A COR DE FUNDO PARA CIANO

def jogo(): 
	limpar()

perguntas = ["Digite o nome do DESAFIANTE: ", "Digite o nome do COMPETIDOR: ", "Agora, digite a PALAVRA SECRETA: "] # REGISTRO DA PARTIDA

def jogo():
    limpar()

    dicas_pedidas = 0
    erros = 0
    vidas = ["|", "|", "|", "|", "O"] # AQUI MOSTRA AS VIDAS DO JOGADOR

    dados = pede_dados(perguntas)
    palavra_oculta = monta_oculta("", dados[2])
    dicas = pede_dicas()
    palavra_sem_acento = remove_acento(dados[2])

    while True:
        monta_tabuleiro(vidas, palavra_oculta, dicas_pedidas) # AQUI É ONDE O GAME INICIA 

        opcao_usuario = opcoes_usuario(vidas, palavra_oculta, dicas_pedidas, dicas)

        if opcao_usuario != "":
            dicas_pedidas = dicas_pedidas + 1
            
        limpar()

        while True:
            print(opcao_usuario)
            print(palavra_oculta)
            print()
            jogada = input("Heey, informe uma letra: ") # AQUI PEDE PARA O JOGADOR INFORMAR UMA LETRA

            limpar()

            if len(jogada) > 1 and len(jogada) < len(dados[2]) or len(jogada) < 1 or len(jogada) > len(dados[2]):
                print("Preencha corretamente") # AQUI É CASO DE UM ERRO DE SINTAXE, VAI AVISAR

            elif jogada[0] == " ":
                print("Não use espaços em branco no ínicio da letra")

            else:
                break

        array_vericou_letra = verifica_letra(jogada, palavra_oculta, dados[2], palavra_sem_acento) # AQUI VAI VERIFICAR E INFORMAR SE A LETRA É VÁLIDA
        array_de_errou = verifica_errou(array_vericou_letra[0], erros, dados[0], dados[1], vidas) # AQUI VAI VERIFICAR E INFORMAR SE A LETRA É INVÁLIDA

        erros = array_de_errou[1]
        vidas = array_de_errou[2]
        ganhador = array_de_errou[0]
        palavra_oculta = array_vericou_letra[1]

        if palavra_oculta.count("*") == 0 or erros >= 5:
            armazenar(dados[2], dados[-(ganhador[2]) + 1], dados[ganhador[2]]) # REGISTRAR E ARMAZENAR OS DADOS
            opcao_usuario = escolha_jogo(ganhador[0], ganhador[1], dados)
            return opcao_usuario

while True:
    if jogo() == 0:
        break