import os, time, unicodedata

def limpar():
    os.system("cls")

def esperar(segundos):
    time.sleep(segundos)

def remove_acento(string: str) -> str:
    normalized = unicodedata.normalize('NFD', string)
    return normalized.encode('ascii', 'ignore').decode('utf8')

def monta_tabuleiro(vidas, palavra_oculta, dicas_pedidas): # FUNÇÃO PARA MONTAR O TABULEIRO
    limpar()

    print(" --------")
    print("|       |")
    print("|       {0}".format(vidas[4]))
    print("|       {0}".format(vidas[3]))
    print("|       {0}".format(vidas[2]))
    print("|      {0} {1}".format(vidas[1], vidas[0]))
    print("|")
    print("| ",palavra_oculta)
    print(" ")
    print(" (0) Tentar adivinhar uma letra.")
    if dicas_pedidas + 1 <= 3:
        print(" (1) Solicitar uma dica. (%d/3)"%(dicas_pedidas))
    print("")

def mostrar_vitoria(vencedor, nome_vencedor, dados): # FUNÇÃO PARA MOSTRAR O VENCEDOR E OS DADOS DA PARTIDA
    limpar()

    print("Hmm, a palavra era: ",dados[2])
    print("Parabéns, %s %s você é o vencedor! :D\n"%(vencedor, nome_vencedor))

    print("Histórico de partidas:")
    print()
    print(''.join(ler_registro()))
    print()

    print("Opções disponíveis:")
    print("(0) Para SAIR.")
    print("(1) Nova PARTIDA.")

def pede_dados(perguntas): # FUNÇÃO QUE VAI VERIFICAR SE O DIGITO INFORMADO É NÚMERO OU LETRA E SE POSSUI MAIS DE 2 LETRAS SEM ESPAÇO
    respostas = []
    vez = 0
    while vez < len(perguntas):
        resposta = input(perguntas[vez])
        try:
            resposta = int(resposta)
            limpar()
            print("Oops, não pode ser números, somente letras. :/")
            continue
        except:
            if vez == 1:
                limpar()

            if len(resposta) < 2:
                limpar()
                print("Oops, isso deve possuir mais que DUAS letras. :/")

            elif resposta[0] == " " or resposta[1] == " ":
                limpar()
                print("Oops, isso deve possuir DUAS ou MAIS letras e NÃO pode ter ESPAÇOS. :D")

            else:
                respostas.append(resposta)
                vez = vez + 1 
    return respostas

def monta_oculta(oculta, palavra_chave): # FUNÇÃO QUE VAI MONTAR A PALAVRA E OCULTAR ELA NA TELA PARA O JOGADOR
    for letra in palavra_chave:
        if letra == " ":
            oculta = oculta + " "
        else:
            oculta = oculta + "*"
    return oculta

def pede_dicas(): # FUNÇÃO QUE VAI PEDIR AS 3 DICAS
    array_dicas = []
    vez = 1
    while vez < 4:
        dica = input("Por gentileza, informe a dica %d: "%vez)
        if len(dica) == 0:
            limpar()
            print("Preencha o campo corretamente")

        elif dica[0] == " ":
            limpar()
            print("Oops, não pode possuir espaço antes da dica. :D")

        else:
            array_dicas.append(dica)
            vez = vez + 1
    return array_dicas

def opcoes_usuario(vidas, palavra_oculta, dicas_pedidas, dicas):
    while True:
        try:
            escolha = int(input("Por gentileza, faça uma escolha: '0' ou '1': "))  # USUARIO ESCOLHE CHUTAR LETRA OU PEDIR DICA

            if escolha > 1 or escolha < 0: 
                monta_tabuleiro(vidas, palavra_oculta, dicas_pedidas)
                print("Oops, isso não é válido, tente novamente!")

            elif escolha == 1 and dicas_pedidas >= 3:
                monta_tabuleiro(vidas, palavra_oculta, dicas_pedidas)
                print("Que pena! Você não possui mais dicas. Agora é você e você, kkkk.")

            elif escolha == 1:
                return "Dica %d: %s"%(dicas_pedidas + 1, dicas[dicas_pedidas])
            else:
                return ""
        except:
            monta_tabuleiro(vidas, palavra_oculta, dicas_pedidas)
            print("Oops, isso não é válido, tente novamente!")

def verifica_letra(letra_jogada, palavra_oculta, palavra_chave, palavra_sem_acento): # FUNÇÃO QUE VERIFICA SE A LETRA CONDIZ COM A LETRA DA PALAVRA A SER ADIVINHDA
    errou = True
    nova_oculta = ""

    if letra_jogada.lower() == palavra_chave.lower() or letra_jogada.lower() == palavra_sem_acento.lower():
        nova_oculta = palavra_chave

    else:
        for posicao, letra in enumerate(palavra_sem_acento):
            if letra.lower() != letra_jogada.lower() and palavra_oculta[posicao] == "*":
                nova_oculta = nova_oculta + "*"

            elif letra_jogada.lower() == letra.lower() and palavra_oculta[posicao] == "*":
                nova_oculta = nova_oculta + palavra_chave[posicao]
                errou = False
                
            elif letra == " ":
                nova_oculta = nova_oculta + " "
            else:
                nova_oculta = nova_oculta + palavra_chave[posicao]

    return [errou, nova_oculta]

def verifica_errou(se_errou, quantidade_erros, desafiante, competidor, vidas):

    ganhador = ["Competidor", competidor, 0]

    if se_errou == True and quantidade_erros < 4:
        quantidade_erros = quantidade_erros + 1
        vidas[quantidade_erros - 1] = " "
        limpar()
        print("Poxa, você errou, tentativas disponíveis: %d/5"%quantidade_erros)
        esperar(1)
                
    elif se_errou == True and quantidade_erros >= 4:
        quantidade_erros = quantidade_erros + 1
        ganhador = ["Desafiante", desafiante, 1]
    
    return [ganhador, quantidade_erros, vidas]


def registrar(informacoes): # FUNÇÃO VAI CRIAR AS LOGS DA PARTIDA
    arquivo = open("Logs das partidas.txt", "w")
    arquivo.write(informacoes)
    arquivo.close()

def ler_registro(): # FUNÇÃO QUE VAI LER O REGISTRO QUANDO OUTRA PARTIDA COMEÇAR
    arquivo = open("logs das partidas.txt", "r")
    conteudo = arquivo.readlines()
    arquivo.close()
    return conteudo

def armazenar(palavra, vencedor, perdedor): # FUNÇÃO QUE VAI ARMAZENAR AS LOGS DA PARTIDA
    try:
        conteudo = ler_registro()
    except:
        conteudo = []
        
    conteudo.append("Vencedor: %s - Perdedor: %s, Palavra da partida: %s\n"%(vencedor, perdedor, palavra))
    registrar(''.join(conteudo))

def escolha_jogo(vencedor, nome_vencedor, dados):
    mostrar_vitoria(vencedor, nome_vencedor, dados)
    while True:
        try:
            opcao_usuario = int(input("Por gentileza, faça uma escolha: ")) # AQUI PEDE PARA O JOGADOR FAZER UMA ESCOLHA, '' OU '1'

            if opcao_usuario < 0 or opcao_usuario > 1:
                mostrar_vitoria(vencedor, nome_vencedor, dados)
                print("Oops, isso não é válido. :/")

            else:
                return opcao_usuario
        except:
            mostrar_vitoria(vencedor, nome_vencedor, dados)
            print("Oops, isso não é válido. :/")