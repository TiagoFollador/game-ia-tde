import numpy as np
import random
from ia import *


class Jogo:
    def __init__(self):
        self.linhas = 6
        self.colunas = 7

        self.posicao_vazia = " "
        self.posicao_vermelha = "X"
        self.posicao_amarela = "0"

        self.teclas = {"A": 0, "S": 1, "D": 2, "F": 3, "G": 4, "H": 5, "J": 6}

        self.tabuleiro = self.criar_tabuleiro()

    def criar_tabuleiro(self):
        return np.full((self.linhas, self.colunas), self.posicao_vazia)

    def mostrar_tabuleiro(self):
        print("\n   A S D F G H J")
        for n, linha in enumerate(self.tabuleiro):
            print(f"{n} ", " ".join(linha), f" {n}")
        print("\n   A S D F G H J")
        print("-----------------------------------------")

    def movimento_valido(self, coluna):
        return self.tabuleiro[0, coluna] == self.posicao_vazia

    def proxima_linha_disponivel(self, coluna):
        for l in range(self.linhas - 1, -1, -1):
            if self.tabuleiro[l, coluna] == self.posicao_vazia:
                return l
        return None

    def colocar_peca(self, linha, coluna, peca):
        self.tabuleiro[linha, coluna] = peca

    def checar_vitoria(self, peca):
        # Checar horizontal
        for l in range(self.linhas):
            for c in range(self.colunas - 3):
                if all(self.tabuleiro[l, c + i] == peca for i in range(4)):
                    return True

        # Checar vertical
        for c in range(self.colunas):
            for l in range(self.linhas - 3):
                if all(self.tabuleiro[l + i, c] == peca for i in range(4)):
                    return True

        # Checar diagonal /
        for l in range(3, self.linhas):
            for c in range(self.colunas - 3):
                if all(self.tabuleiro[l - i, c + i] == peca for i in range(4)):
                    return True

        # Checar diagonal \
        for l in range(self.linhas - 3):
            for c in range(self.colunas - 3):
                if all(self.tabuleiro[l + i, c + i] == peca for i in range(4)):
                    return True

        return False

    def checar_empate(self, resultado, fim_de_jogo):
        if not any(self.movimento_valido(c) for c in range(self.colunas)):
            resultado = "Empate!"
            fim_de_jogo = True
        return resultado, fim_de_jogo

    def PVP(self):
        resultado = None
        fim_de_jogo = False
        turno = 0

        self.mostrar_tabuleiro()

        while not fim_de_jogo:
            if turno == 0:
                mov_valido = False
                while not mov_valido:
                    jogada = input("Escolha uma coluna: ").upper()
                    if jogada in self.teclas:
                        coluna = self.teclas[jogada]
                        if self.movimento_valido(coluna):
                            linha = self.proxima_linha_disponivel(coluna)
                            self.colocar_peca(linha, coluna, self.posicao_vermelha)
                            mov_valido = True
                        else:
                            print("Coluna cheia! Escolha outra.")
                    else:
                        print("Tecla inválida! Use A-G.")

                if self.checar_vitoria(self.posicao_vermelha):
                    self.mostrar_tabuleiro()
                    resultado = "Jogador Vermelho venceu!"
                    fim_de_jogo = True

            else:

                mov_valido = False
                while not mov_valido:
                    jogada = input("Escolha uma coluna: ").upper()
                    if jogada in self.teclas:
                        coluna = self.teclas[jogada]
                        if self.movimento_valido(coluna):
                            linha = self.proxima_linha_disponivel(coluna)
                            self.colocar_peca(linha, coluna, self.posicao_amarela)
                            mov_valido = True
                        else:
                            print("Coluna cheia! Escolha outra.")
                    else:
                        print("Tecla inválida! Use A-G.")

                if self.checar_vitoria(self.posicao_amarela):
                    self.mostrar_tabuleiro()
                    resultado = "Jogador Amarelo venceu!"
                    fim_de_jogo = True

            self.mostrar_tabuleiro()
            turno = 1 - turno  # alterna turno

            resultado, fim_de_jogo = self.checar_empate(resultado, fim_de_jogo)

        print(f"Resultado: {resultado}")

    def PVIA(self, dificuldade):
        fim_de_jogo = False
        turno = 0
        resultado = None
        tempo_total = 0.0

        if dificuldade == 1:
            dificuldade_escolhida = avaliar_janela_iniciante
            profundidade_max = 2
        elif dificuldade == 2:
            dificuldade_escolhida = avaliar_janela_intermediaria
            profundidade_max = 6
        elif dificuldade == 3:
            dificuldade_escolhida = avaliar_janela_avancada
            profundidade_max = 8
        else:
            dificuldade_escolhida = avaliar_janela_iniciante
            profundidade_max = 2

        self.mostrar_tabuleiro()

        while not fim_de_jogo:
            if turno == 0:
                mov_valido = False
                while not mov_valido:
                    jogada = input("Escolha uma coluna: ").upper()
                    if jogada in self.teclas:
                        coluna = self.teclas[jogada]
                        if self.movimento_valido(coluna):
                            self.colocar_peca(
                                self.proxima_linha_disponivel(coluna),
                                coluna,
                                self.posicao_vermelha,
                            )
                            mov_valido = True
                        else:
                            print("Coluna cheia! Escolha outra.")
                    else:
                        print("Tecla inválida! Use A-G.")

                if self.checar_vitoria(self.posicao_vermelha):
                    self.mostrar_tabuleiro()
                    resultado = "Jogador Vermelho venceu!"
                    fim_de_jogo = True

            else:
                coluna, valor = minimax(
                    self.tabuleiro,
                    depth=1,
                    max_depth=profundidade_max,
                    peca_ia="0",
                    heuristica=dificuldade_escolhida,
                )
                print(f"Melhor coluna: {coluna}, Valor: {valor}")
                self.colocar_peca(
                    self.proxima_linha_disponivel(coluna), coluna, self.posicao_amarela
                )

                if self.checar_vitoria(self.posicao_amarela):
                    self.mostrar_tabuleiro()
                    resultado = "Jogador Amarelo venceu!"
                    fim_de_jogo = True

            self.mostrar_tabuleiro()
            turno = 1 - turno  # alterna turno

            resultado, fim_de_jogo = self.checar_empate(resultado, fim_de_jogo)

        print(f"Resultado: {resultado}")


def jogar():
    jogo = Jogo()
    tabuleiro = jogo.tabuleiro

    print("Modos de jogo:\n1 - Player vs Player\n2 - Player vs Máquina")

    while True:
        entrada = input("Qual modo de jogo deseja jogar? ")
        if entrada.isdigit():
            modo_de_jogo = int(entrada)
            if modo_de_jogo == 1:
                jogo.PVP()
                break
            if modo_de_jogo == 2:
                while True:
                    dificuldade = int(
                        input("Qual dificuldade deseja jogar (1, 2 ou 3)?")
                    )
                    if dificuldade in [1, 2, 3]:
                        jogo.PVIA(dificuldade)
                        break
                    else:
                        print("Entrada inválida! Por favor, digite 1, 2 ou 3.")
            break
        else:
            print("Entrada inválida! Por favor, digite 1 ou 2.")


if __name__ == "__main__":
    jogar()
