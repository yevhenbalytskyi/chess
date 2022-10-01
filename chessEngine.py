# Main driver file, responsible for user input and displaying current game state

import pygame as p

class GameState():
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
    ]
    whiteToMove = True
    moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def ifLegal(self):
        # General rules
        if self.pieceMoved == "--":
            return False
        if self.pieceMoved[0] == self.pieceCaptured[0]:
            return False

        if pathBlocked(self):
            return False

        #White pawn move logic
        if self.pieceMoved == "wp" and self.pieceCaptured[0] == "b" and self.startCol == self.endCol:
            return False
        if self.pieceMoved == "wp" and self.pieceCaptured[0] == "b" and abs(self.startCol - self.endCol) == 1 \
                and self.startRow - self.endRow == 1:
            return True
        if self.pieceMoved == "wp" and self.startCol == self.endCol and self.startRow - self.endRow == 1:
            return True

        # Black pawn move logic
        if self.pieceMoved == "bp" and self.pieceCaptured[0] == "w" and self.startCol == self.endCol:
            return False
        if self.pieceMoved == "bp" and self.pieceCaptured[0] == "w" and abs(self.startCol - self.endCol) == 1 \
                and self.startRow - self.endRow == -1:
            return True
        if self.pieceMoved == "bp" and self.startCol == self.endCol and self.startRow - self.endRow == -1:
            return True

        # Rook move logic
        if self.pieceMoved[1] == "R" and (self.startRow == self.endRow or self.startCol == self.endCol):
            return True

        # Bishop move logic
        if self.pieceMoved[1] == "B":
            diagonal1 = self.startRow - self.startCol  # left to right diagonal
            diagonal2 = self.startRow + self.startCol  # right to left diagonal
            if self.endRow - self.endCol == diagonal1:
                return True
            if self.endRow + self.endCol == diagonal2:
                return True

        # Knight move logic
        if self.pieceMoved[1] == "N":
            if abs(self.startRow - self.endRow) + abs(self.startCol - self.endCol) == 3\
                    and not (self.startRow == self.endRow or self.startCol == self.endCol):
                return True

        # King move logic
        if self.pieceMoved[1] == "K":
            if abs(self.startRow - self.endRow) + abs(self.startCol - self.endCol) == 1:
                return True
            if abs(self.startRow - self.endRow) + abs(self.startCol - self.endCol) == 2\
                    and not (self.startRow == self.endRow or self.startCol == self.endCol):
                return True

        # Queen move logic
        if self.pieceMoved[1] == "Q":
            if self.startRow == self.endRow or self.startCol == self.endCol:
                return True
            diagonal1 = self.startRow - self.startCol  # left to right diagonal
            diagonal2 = self.startRow + self.startCol  # right to left diagonal
            if self.endRow - self.endCol == diagonal1:
                return True
            if self.endRow + self.endCol == diagonal2:
                return True

    def legalMoves(self):
        legal = []
        for r in range(8):
            for c in range(8):
                if self.pieceMoved[1] == "R" and (self.startRow == r or self.startCol == c):
                    legal.append([r,c])
        return legal

    def getChessNotation(self):
        takes = ""
        if self.pieceCaptured != "--":
            takes = "x"
        piece = self.pieceMoved
        return piece + takes + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


def pathBlocked(self):
    if self.endCol == self.startCol:
        col = self.startCol
        start = self.startRow
        end = self.endRow - 1
        while end > start :
            if GameState.board[end][col] != "--":
                return True
            else:
                end = end - 1
    return False