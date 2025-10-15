import numpy as np
import copy

linhas = 6
colunas = 7

# ve se alguem ganhou checando todas as direcoes possiveis
def checar_vitoria(tabuleiro, peca):

    # checa na horizontal
    for l in range(linhas):
        for c in range(colunas - 3):
            if all(tabuleiro[l, c + i] == peca for i in range(4)):
                return True

    # checa na vertical
    for c in range(colunas):
        for l in range(linhas - 3):
            if all(tabuleiro[l + i, c] == peca for i in range(4)):
                return True

    # checa diagonal pra cima
    for l in range(3, linhas):
        for c in range(colunas - 3):
            if all(tabuleiro[l - i, c + i] == peca for i in range(4)):
                return True

    # checa diagonal pra baixo
    for l in range(linhas - 3):
        for c in range(colunas - 3):
            if all(tabuleiro[l + i, c + i] == peca for i in range(4)):
                return True

    return False

# retorna as colunas que ainda tem espaco pra jogar
def movimentos_validos(tabuleiro):
    colunas_validas = []
    for c in range(tabuleiro.shape[1]):
        if tabuleiro[0][c] == " ":
            colunas_validas.append(c)
    return colunas_validas

# faz uma copia do tabuleiro e simula a jogada nele
def simular_jogada(tabuleiro, coluna, peca):
    novo_tabuleiro = copy.deepcopy(tabuleiro)  # copia um tabuleiro
    for l in range(linhas - 1, -1, -1):
        if novo_tabuleiro[l][coluna] == " ":
            novo_tabuleiro[l][coluna] = peca
            break
    return novo_tabuleiro

# ve se o jogo acabou por vitoria ou empate
def checar_fim(tabuleiro):
    # checa se alguem ganhou
    if checar_vitoria(tabuleiro, "X") or checar_vitoria(tabuleiro, "0"):
        return True

    # ve se empatou (tabuleiro cheio)
    movimentos = movimentos_validos(tabuleiro)
    if not movimentos:
        return True

    return False

# avalia uma janela de 4 casas pra ia iniciante, da pontos ou tira se precisar bloquear
def avaliar_janela_iniciante(janela, peca_ia):
    score = 0
    peca_humano = "X" if peca_ia == "0" else "0"

    if janela.count(peca_ia) == 3 and janela.count(" ") == 1:
        score += 1
    if janela.count(peca_humano) == 3 and janela.count(" ") == 1:
        score -= 10
    return score

# avalia uma janela de 4 casas pra ia intermediaria, da pontos de acordo com as possibilidades
def avaliar_janela_intermediaria(janela, peca_ia):
    score = 0
    peca_humano = "X" if peca_ia == "0" else "0"

    if janela.count(peca_ia) == 4:
        score += 100
    elif janela.count(peca_ia) == 3 and janela.count(" ") == 1:
        score += 50
    elif janela.count(peca_ia) == 2 and janela.count(" ") == 2:
        score += 10
    if janela.count(peca_humano) == 3 and janela.count(" ") == 1:
        score -= 80
    return score

# avalia uma janela de 4 casas pra ia avancada, considera posicoes estrategicas
def avaliar_janela_avancada(janela, peca_ia): 
    score = 0
    peca_humano = "X" if peca_ia == "0" else "0"

    count_ia = janela.count(peca_ia)
    count_humano = janela.count(peca_humano)
    count_vazio = janela.count(" ")

    # se tem pecas dos dois, nao serve pra nada
    if count_ia > 0 and count_humano > 0:
        return 0

    # da pontos pras jogadas da ia
    if count_ia == 4:
        score += 1000
    elif count_ia == 3 and count_vazio == 1:
        score += 100
        if janela[1] == peca_ia and janela[2] == peca_ia:
            score += 50
    elif count_ia == 2 and count_vazio == 2:
        score += 20
        if janela[0] == " " and janela[3] == " ":
            score += 30
        if janela[1] == peca_ia and janela[2] == peca_ia:
            score += 15

    # tira pontos pras jogadas do humano (bloquear)
    if count_humano == 4:
        score -= 1000
    elif count_humano == 3 and count_vazio == 1:
        score -= 200
    elif count_humano == 2 and count_vazio == 2:
        if janela[0] == " " and janela[3] == " ":
            score -= 40
        else:
            score -= 15

    return score

# calcula a pontuacao total do tabuleiro somando todas as janelas possiveis
def pontuacao_tabuleiro(tabuleiro, peca_ia, funcao_avaliacao):
    score = 0
    linhas_t, colunas_t = tabuleiro.shape

    # checa horizontal
    for l in range(linhas_t):
        for c in range(colunas_t - 3):
            janela = [tabuleiro[l, c + i] for i in range(4)]
            score += funcao_avaliacao(janela, peca_ia)

    # checa vertical
    for l in range(linhas_t - 3):
        for c in range(colunas_t):
            janela = [tabuleiro[l + i, c] for i in range(4)]
            score += funcao_avaliacao(janela, peca_ia)

    # checa diagonal pra baixo
    for l in range(linhas_t - 3):
        for c in range(colunas_t - 3):
            janela = [tabuleiro[l + i, c + i] for i in range(4)]
            score += funcao_avaliacao(janela, peca_ia)

    # checa diagonal pra cima
    for l in range(3, linhas_t):
        for c in range(colunas_t - 3):
            janela = [tabuleiro[l - i, c + i] for i in range(4)]
            score += funcao_avaliacao(janela, peca_ia)

    return score

# parte max do minimax, tenta maximizar o valor da ia
def max_value(tabuleiro, depth, max_depth, peca_ia, heuristica):
    # para se chegou no fim do jogo ou na profundidade maxima
    if checar_fim(tabuleiro) or depth == max_depth:
        return pontuacao_tabuleiro(tabuleiro, peca_ia, heuristica)

    valor = -np.inf
    for col in movimentos_validos(tabuleiro):
        novo_tabuleiro = simular_jogada(tabuleiro, col, peca_ia)
        valor = max(
            valor, min_value(novo_tabuleiro, depth + 1, max_depth, peca_ia, heuristica)
        )
    return valor

# parte min do minimax, tenta minimizar o valor pro humano
def min_value(tabuleiro, depth, max_depth, peca_ia, heuristica):
    if checar_fim(tabuleiro) or depth == max_depth:
        return pontuacao_tabuleiro(tabuleiro, peca_ia, heuristica)

    peca_humano = "X" if peca_ia == "0" else "0"
    valor = np.inf
    for col in movimentos_validos(tabuleiro):
        novo_tabuleiro = simular_jogada(tabuleiro, col, peca_humano)
        valor = min(
            valor, max_value(novo_tabuleiro, depth + 1, max_depth, peca_ia, heuristica)
        )
    return valor

# algoritmo minimax pra achar a melhor jogada
def minimax(tabuleiro, depth, max_depth, peca_ia, heuristica):
    """Função minimax que retorna a melhor coluna e o valor associado."""
    melhor_valor = -np.inf
    melhor_coluna = None

    for col in movimentos_validos(tabuleiro):
        novo_tabuleiro = simular_jogada(tabuleiro, col, peca_ia)
        valor = min_value(novo_tabuleiro, depth + 1, max_depth, peca_ia, heuristica)
        if valor > melhor_valor:
            melhor_valor = valor
            melhor_coluna = col

    return melhor_coluna, melhor_valor
