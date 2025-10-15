import numpy as np
import copy

linhas = 6
colunas = 7


def checar_vitoria(tabuleiro, peca):
    """Verifica se uma peça ganhou o jogo"""
    # Horizontal
    for l in range(linhas):
        for c in range(colunas - 3):
            if all(tabuleiro[l, c + i] == peca for i in range(4)):
                return True

    # Vertical
    for c in range(colunas):
        for l in range(linhas - 3):
            if all(tabuleiro[l + i, c] == peca for i in range(4)):
                return True

    # Diagonal /
    for l in range(3, linhas):
        for c in range(colunas - 3):
            if all(tabuleiro[l - i, c + i] == peca for i in range(4)):
                return True

    # Diagonal \
    for l in range(linhas - 3):
        for c in range(colunas - 3):
            if all(tabuleiro[l + i, c + i] == peca for i in range(4)):
                return True

    return False


def movimentos_validos(tabuleiro):
    colunas_validas = []
    for c in range(tabuleiro.shape[1]):
        if tabuleiro[0][c] == ' ':
            colunas_validas.append(c)
    return colunas_validas


def simular_jogada(tabuleiro, coluna, peca):
    novo_tabuleiro = copy.deepcopy(tabuleiro) #copia um tabuleiro
    for l in range(linhas - 1, -1, -1):
        if novo_tabuleiro[l][coluna] == ' ':
            novo_tabuleiro[l][coluna] = peca #simula a peça nesse tabuleiro novo
            break
    return novo_tabuleiro


def checar_fim(tabuleiro):
    if checar_vitoria(tabuleiro, 'X') or checar_vitoria(tabuleiro, '0'):
        return True

    #checa se tem empata
    movimentos = movimentos_validos(tabuleiro)
    if not movimentos:  
        return True

    return False


def avaliar_janela_iniciante(janela, peca_ia):
    score = 0
    peca_humano = 'X' if peca_ia == '0' else '0'

    if janela.count(peca_ia) == 3 and janela.count(' ') == 1:
        score += 1
    if janela.count(peca_humano) == 3 and janela.count(' ') == 1:
        score -= 10
    return score

def avaliar_janela_intermediaria(janela, peca_ia):
    score = 0
    peca_humano = 'X' if peca_ia == '0' else '0'

    if janela.count(peca_ia) == 4:
        score += 100
    elif janela.count(peca_ia) == 3 and janela.count(' ') == 1:
        score += 50
    elif janela.count(peca_ia) == 2 and janela.count(' ') == 2:
        score += 10
    if janela.count(peca_humano) == 3 and janela.count(' ') == 1:
        score -= 80
    return score

def avaliar_janela_avancada(janela, peca_ia):
    #tem que implementar ainda
    return 0

def pontuacao_tabuleiro(tabuleiro, peca_ia, funcao_avaliacao):
    score = 0
    linhas_t, colunas_t = tabuleiro.shape

    # Horizontal
    for l in range(linhas_t):
        for c in range(colunas_t - 3):
            janela = [tabuleiro[l, c + i] for i in range(4)]
            score += funcao_avaliacao( janela, peca_ia)

    # Vertical
    for l in range(linhas_t - 3):
        for c in range(colunas_t):
            janela = [tabuleiro[l + i, c] for i in range(4)]
            score += funcao_avaliacao( janela, peca_ia)

    # Diagonal \
    for l in range(linhas_t - 3):
        for c in range(colunas_t - 3):
            janela = [tabuleiro[l + i, c + i] for i in range(4)]
            score += funcao_avaliacao( janela, peca_ia)

    # Diagonal /
    for l in range(3, linhas_t):
        for c in range(colunas_t - 3):
            janela = [tabuleiro[l - i, c + i] for i in range(4)]
            score += funcao_avaliacao( janela, peca_ia)

    return score


def max_value(tabuleiro, depth, max_depth, peca_ia, heuristica):
    #condição de parada da recursão: vit/empara e profundidade max
    if checar_fim(tabuleiro) or depth == max_depth:
        return pontuacao_tabuleiro(tabuleiro, peca_ia, heuristica)

    valor = -np.inf
    for col in movimentos_validos(tabuleiro):
        novo_tabuleiro = simular_jogada(tabuleiro, col, peca_ia)
        valor = max(valor, min_value(novo_tabuleiro, depth + 1, max_depth, peca_ia, heuristica))
    return valor


def min_value(tabuleiro, depth, max_depth, peca_ia, heuristica):
    if checar_fim(tabuleiro) or depth == max_depth:
        return pontuacao_tabuleiro(tabuleiro, peca_ia, heuristica)

    peca_humano = 'X' if peca_ia == '0' else '0'
    valor = np.inf
    for col in movimentos_validos(tabuleiro):
        novo_tabuleiro = simular_jogada(tabuleiro, col, peca_humano)
        valor = min(valor, max_value(novo_tabuleiro, depth + 1, max_depth, peca_ia, heuristica))
    return valor


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
