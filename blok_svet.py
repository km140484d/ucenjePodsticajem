import numpy as np
import math
import matplotlib.pyplot as plt
import constants as con


def main():
    print('a')
    for i in range(con.ROWS):
        row = []
        for j in range(con.COLS):
            if (i, j) == (0, 3):
                row.append(State((i, j), 1))
            elif (i, j) == (1, 3):
                row.append(State((i, j), -1))
            elif (i, j) != (1, 1):
                row.append(State((i, j), -0.04))
            else:
                row.append(None)
        board.append(row)
    for iter in range(100):
        print('--------------------------------------------------------')
        for i in range(len(board)):
            print()
            for j in range(len(board[0])):
                if (i, j) != con.WALL and (i, j) != con.GOAL and (i, j) != con.FAIL:
                    board[i][j].calc_Q()
                    print(i, j, board[i][j].Q_next[0].val, board[i][j].Q_next[1].val, board[i][j].Q_next[2].val,
                          board[i][j].Q_next[3].val)
        for i in range(len(board)):
            for j in range(len(board[0])):
                if (i, j) != con.WALL and (i, j) != con.GOAL and (i, j) != con.FAIL:
                    board[i][j].next_Q()
    for i in range(len(board)):
        print('--------------------------------------')
        for j in range(len(board[0])):
            # S = board[i][j]
            # print(board)
            for k in range(4):
                if board[i][j] is not None:
                    print(i, j, 'Q', k, board[i][j].Q[k], board[i][j].R)


class State:
    # S = state (x, y)
    def __init__(self, S, R):
        self.S = S
        self.R = R
        self.Q = [Q(self, count) for count in con.directions]
        self.Q_next = self.Q

    def next_Q(self):
        self.Q = self.Q_next

    def calc_Q(self):
        for q in self.Q_next: q.next_val()

    def max_Q(self):
        max_q = self.Q[0]
        for q in self.Q:
            if max_q.val < q.val:
                max_q = q
        return max_q.val


class Q:
    # a = direction: UP, DOWN, LEFT, RIGHT
    def __init__(self, state, a):
        self.state = state
        self.a = a
        self.val = 0

    def next_val(self):
        sum = 0
        for dir in con.directions:
            sum += self.p(dir) * self.next_state(dir).max_Q()
        self.val = self.state.R + con.GAMMA * sum

    # directions = [UP, DOWN, LEFT, RIGHT]
    def p(self, dir):
        if dir == self.a:
            return 0.8
        elif dir == con.opposite[self.a]:
            return 0
        else:
            return 0.1

    def next_state(self, dir):
        x, y = self.state.S[0], self.state.S[1]
        if dir == con.UP and x - 1 > 0 and (x - 1, y) != con.WALL:
            return board[x - 1][y]
        elif dir == con.DOWN and x + 1 < con.ROWS and (x + 1, y) != con.WALL:
            return board[x + 1][y]
        elif dir == con.LEFT and y - 1 > 0 and (x, y - 1) != con.WALL:
            return board[x][y - 1]
        elif dir == con.RIGHT and y + 1 < con.COLS and (x, y + 1) != con.WALL:
            return board[x][y + 1]
        else:
            return board[x][y]


if __name__ == "__main__":
    board = []
    main()
