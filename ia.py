import numpy as np
import time

def PVIA(dificuldade):
    if dificuldade == 1:
        pass
    elif dificuldade == 2:
        pass
    else:
        pass

class Heuristicas():

    def avaliar_janela_iniciante(janela, peca_ia):
        score = 0
        peca_humano = 'X' if peca_ia == '0' else '0'

        if janela.count(peca_ia) == 3 and janela.count(' ') == 1:
            score += 1 # adiciona 1 ponto por chance de vitória

        if janela.count(peca_humano) == 3 and janela.count(' ') == 1:
            score -= 10 # bloquear o oponente
        return score
    
    

    def avaliar_janela_intermediaria(janela, peca_ia): #cz   #recebe uma lista de 4 elementos, e pra cada elemento da lista, soma ou subtrai pontos dependendo do conteudo
        #funcao auxiliar para a heuristica intermediaria
        score = 0
        peca_humano = 'X'
        if janela.count(peca_ia) == 4:
            score += 100
        if janela.count(peca_ia) == 3 and janela.count(' ') == 1:
            score += 50
        if janela.count(peca_ia) == 2 and janela.count(' ') == 2:
            score += 10

        if janela.count(peca_humano) == 3 and janela.count(' ') == 1:
            score -= 80

        return score
    

    def avaliar_janela_avancada(janela, peca_ia): 
        return 0; #precisa fazer
    
    def pontuacao_tabuleiro(tabuleiro, peca_ia, funcao_avaliacao): #apenas mude a heuristica 
        score = 0
        linhas, colunas = tabuleiro.shape

        #L -> linhas
        #C -> colunas
        #pontuacao horizontal
        for l in range(linhas):
            for c in range(colunas - 3):
                janela = []
                for i in range(4):
                    janela.append(tabuleiro[l, c + i])
                score += Heuristicas.funcao_avaliacao(janela, peca_ia)

        #pontuacao vertical
        for l in range(linhas - 3):
            for c in range(colunas):
                janela = []
                for i in range(4):
                    janela.append(tabuleiro[l + i, c])
                score += Heuristicas.funcao_avaliacao(janela, peca_ia)

        # pontuacao diagonal /
        for l in range(linhas - 3):
            for c in range(colunas - 3):
                janela = []
                for i in range(4):
                    janela.append(tabuleiro[l + i, c + i])
                score += Heuristicas.funcao_avaliacao(janela, peca_ia)

        # pontuacao diagonal \
        for l in range(3, linhas ):
            for c in range(colunas - 3):
                janela = []
                for i in range(4):
                    janela.append(tabuleiro[l - i, c + i])
                score += Heuristicas.funcao_avaliacao(janela, peca_ia)

        return score
        #pode fazer uma funcao de desempate, caso jogadas empatem em score = 0, escolher a que estiver mais proximo do centro ou fazer um random das casas vazias.

