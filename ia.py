import time
import random
from typing import Optional, Tuple
import numpy as np


EMPTY = ' '


def valid_moves(board: np.ndarray):
    cols = board.shape[1]
    return [c for c in range(cols) if board[0, c] == EMPTY]


def get_row_for_col(board: np.ndarray, col: int) -> Optional[int]:
    for r in range(board.shape[0]-1, -1, -1):
        if board[r, col] == EMPTY:
            return r
    return None


def winning_move(board: np.ndarray, piece: str) -> bool:
    rows, cols = board.shape
    # horizontal
    for r in range(rows):
        for c in range(cols-3):
            if all(board[r, c+i] == piece for i in range(4)):
                return True
    # vertical
    for c in range(cols):
        for r in range(rows-3):
            if all(board[r+i, c] == piece for i in range(4)):
                return True
    # diagonal /
    for r in range(3, rows):
        for c in range(cols-3):
            if all(board[r-i, c+i] == piece for i in range(4)):
                return True
    # diagonal \
    for r in range(rows-3):
        for c in range(cols-3):
            if all(board[r+i, c+i] == piece for i in range(4)):
                return True
    return False


class Heuristicas:
    """Implementação simples de heurística baseada em janelas de 4, conforme pedido.

    Pontuação simples usada apenas no nível 1:
    - +100 para vitória imediata do AI
    - -100 para vitória imediata do jogador
    - +3 por peça do AI na coluna central
    - +5 por janela com 3 do AI e 1 vazia, +2 por janela com 2 do AI e 2 vazias
    - penaliza janelas onde o adversário tem 3 e 1 vazia (-4)
    """

    @staticmethod
    def evaluate_window(window, ai_piece, player_piece):
        score = 0
        if window.count(ai_piece) == 4:
            score += 100
        elif window.count(ai_piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(ai_piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(player_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4
        return score

    @staticmethod
    def score_position(board: np.ndarray, ai_piece: str, player_piece: str) -> int:
        rows, cols = board.shape
        score = 0
        # center column preference
        center_col = cols // 2
        score += list(board[:, center_col]).count(ai_piece) * 3

        # horizontal
        for r in range(rows):
            row_array = list(board[r, :])
            for c in range(cols-3):
                window = row_array[c:c+4]
                score += Heuristicas.evaluate_window(window, ai_piece, player_piece)

        # vertical
        for c in range(cols):
            col_array = list(board[:, c])
            for r in range(rows-3):
                window = col_array[r:r+4]
                score += Heuristicas.evaluate_window(window, ai_piece, player_piece)

        # positive diagonal
        for r in range(rows-3):
            for c in range(cols-3):
                window = [board[r+i, c+i] for i in range(4)]
                score += Heuristicas.evaluate_window(window, ai_piece, player_piece)

        # negative diagonal
        for r in range(3, rows):
            for c in range(cols-3):
                window = [board[r-i, c+i] for i in range(4)]
                score += Heuristicas.evaluate_window(window, ai_piece, player_piece)

        return score


def PVIA(dificuldade: int, board: np.ndarray, player_piece: str = 'X', ai_piece: str = '0') -> Tuple[Optional[int], float]:
    """Implementa apenas a dificuldade 1 (greedy simples).

    Estratégia (nível 1):
    1) Se há movimento que faz o AI vencer imediatamente, joga nele.
    2) Se o jogador tem um movimento que vence imediatamente, bloqueia-o.
    3) Caso contrário, escolhe a coluna com maior pontuação heurística simples.
    """
    start = time.time()
    moves = valid_moves(board)
    if not moves:
        return None, 0.0

    # 1) check immediate win for AI
    for col in moves:
        row = get_row_for_col(board, col)
        if row is None:
            continue
        b = board.copy()
        b[row, col] = ai_piece
        if winning_move(b, ai_piece):
            return col, time.time() - start

    # 2) block opponent immediate win
    for col in moves:
        row = get_row_for_col(board, col)
        if row is None:
            continue
        b = board.copy()
        b[row, col] = player_piece
        if winning_move(b, player_piece):
            return col, time.time() - start

    # 3) evaluate heuristics and pick best
    best_score = -10_000
    best_col = random.choice(moves)
    for col in moves:
        row = get_row_for_col(board, col)
        if row is None:
            continue
        b = board.copy()
        b[row, col] = ai_piece
        score = Heuristicas.score_position(b, ai_piece, player_piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col, time.time() - start

    