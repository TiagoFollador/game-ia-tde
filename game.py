import numpy as np
import random
#from ia import PVIA_optins(dificuldade)


class Jogo():
    def __init__(self):
        self.linhas = 6
        self.colunas = 7

        self.posicao_vazia = ' '
        self.posicao_vermelha = 'X'  
        self.posicao_amarela = '0' 

        self.teclas = {
            'A': 0,
            'S': 1,
            'D': 2,
            'F': 3,
            'G': 4,
            'H': 5,
            'J': 6
        }

        self.tabuleiro = self.criar_tabuleiro()

    def criar_tabuleiro(self):
        return np.full((self.linhas, self.colunas), self.posicao_vazia)

    def mostrar_tabuleiro(self):
        print("\n   A S D F G H J")
        for n, linha in enumerate(self.tabuleiro):
            print(f'{n} ', ' '.join(linha), f' {n}')
        print("\n   A S D F G H J")
        print()

    def movimento_valido(self, coluna):
        return self.tabuleiro[0, coluna] == self.posicao_vazia

    def proxima_linha_disponivel(self, coluna):
        for l in range(self.linhas-1, -1, -1):
            if self.tabuleiro[l, coluna] == self.posicao_vazia:
                return l
        return None

    def colocar_peca(self, linha, coluna, peca):
        self.tabuleiro[linha, coluna] = peca

    def checar_vitoria(self, peca):
        # Checar horizontal
        for l in range(self.linhas):
            for c in range(self.colunas-3):
                if all(self.tabuleiro[l, c+i] == peca for i in range(4)):
                    return True

        # Checar vertical
        for c in range(self.colunas):
            for l in range(self.linhas-3):
                if all(self.tabuleiro[l+i, c] == peca for i in range(4)):
                    return True

        # Checar diagonal /
        for l in range(3, self.linhas):
            for c in range(self.colunas-3):
                if all(self.tabuleiro[l-i, c+i] == peca for i in range(4)):
                    return True

        # Checar diagonal \
        for l in range(self.linhas-3):
            for c in range(self.colunas-3):
                if all(self.tabuleiro[l+i, c+i] == peca for i in range(4)):
                    return True

        return False

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
                            linha = self.proxima_linha_disponivel( coluna)
                            self.colocar_peca( linha, coluna, self.posicao_vermelha)
                            mov_valido = True
                        else:
                            print("Coluna cheia! Escolha outra.")
                    else:
                        print("Tecla inválida! Use A-G.")

                if self.checar_vitoria(self.posicao_vermelha):
                    self.mostrar_tabuleiro()
                    resultado = 'Jogador Vermelho venceu!'
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
                    resultado = 'Jogador Amarelo venceu!'
                    fim_de_jogo = True

            self.mostrar_tabuleiro()
            turno = 1 - turno  # alterna turno

            # Checar empate
            if not any(self.movimento_valido(c) for c in range(self.colunas)):
                resultado = 'Empate!'
                fim_de_jogo = True

        return resultado        
    
    def PVIA(self, dificuldade):
        #PVIA_optins(dificuldade)  
        #faz a lógica aqui dai
        pass


def jogar():
    jogo = Jogo()
    tabuleiro = jogo.tabuleiro

    print("Modos de jogo:\n1 - Player vs Player\n2 - Player vs Máquina")

    while True:
        entrada = input("Qual modo de jogo deseja jogar? ")
        if entrada.isdigit():
            modo_de_jogo = int(entrada)
            if modo_de_jogo == 1: 
                resultado = jogo.PVP()
                break
            if  modo_de_jogo == 2:
                while True:
                    dificuldade = input("Qual dificuldade deseja jogar?")
                    if dificuldade in [1,2,3]:
                        resultado, tempo = jogo.PVIA(dificuldade)
                        break
                    print("Entrada inválida! Por favor, digite 1, 2 ou 3.")

        print("Entrada inválida! Por favor, digite 1 ou 2.")


    print(f"{resultado}")

if __name__ == "__main__":
    jogar()

