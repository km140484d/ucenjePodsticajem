import numpy as np
import math
import matplotlib.pyplot as plt
import constants as con


def policy(S):
    return S.max_Q().a


def next_state(state, dir):
    x, y = state.S[0], state.S[1]
    if dir == con.UP and x - 1 >= 0 and (x - 1, y) != con.WALL:
        return board[x - 1][y]
    elif dir == con.DOWN and x + 1 < con.ROWS and (x + 1, y) != con.WALL:
        return board[x + 1][y]
    elif dir == con.LEFT and y - 1 >= 0 and (x, y - 1) != con.WALL:
        return board[x][y - 1]
    elif dir == con.RIGHT and y + 1 < con.COLS and (x, y + 1) != con.WALL:
        return board[x][y + 1]
    else:
        return board[x][y]


def transform(dir):
    if dir == con.UP:
        return 'UP'
    elif dir == con.DOWN:
        return 'DOWN'
    elif dir == con.LEFT:
        return 'LEFT'
    else:
        return 'RIGHT'


def main():
    for g in con.GAMMA:
        print('GAMMA: ', g, '-------------------------')
        board.clear()
        for i in range(con.ROWS):
            row = []
            for j in range(con.COLS):
                if (i, j) == con.GOAL:
                    row.append(State((i, j), 1, g))
                elif (i, j) == con.FAIL:
                    row.append(State((i, j), -1, g))
                elif (i, j) != con.WALL:
                    row.append(State((i, j), -0.04, g))
                else:
                    row.append(None)
            board.append(row)
        for iter in range(50):
            for i in range(len(board)):
                if iter == 49:
                    print()
                for j in range(len(board[0])):
                    if (i, j) != con.WALL and (i, j) != con.GOAL and (i, j) != con.FAIL:
                        board[i][j].calc_Q()
                        if iter == 49:
                            print(i, j, board[i][j].Q[0].next_val, board[i][j].Q[1].next_val, board[i][j].Q[2].next_val,
                                  board[i][j].Q[3].next_val)
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if (i, j) != con.WALL and (i, j) != con.GOAL and (i, j) != con.FAIL:
                        board[i][j].next_Q()

        S_curr = board[2][0]
        while S_curr.S != con.GOAL and S_curr.S != con.FAIL:
            a = policy(S_curr)
            S_curr = next_state(S_curr, a)
            print(transform(a), S_curr.S)

    # print('###################################')
    # for i in range(len(board)):
    #     print()
    #     for j in range(len(board[0])):
    #         # S = board[i][j]
    #         # print(board)
    #         # for k in range(4):
    #         if board[i][j] is not None:
    #             print(i, j, 'Q', board[i][j].max_Q().val)


class State:
    # S = state (x, y)
    def __init__(self, S, R, gamma):
        self.S = S
        self.R = R
        self.gamma = gamma
        self.Q = [Q(self, count, self.R) for count in con.directions]

    def next_Q(self):
        Q = self.Q
        for i in range(len(Q)):
            Q[i].val = Q[i].next_val

    def calc_Q(self):
        for q in self.Q: q.calc_next_val()

    def max_Q(self):
        max_q = self.Q[0]
        for q in self.Q:
            if max_q.val < q.val:
                max_q = q
        return max_q


class Q:
    # a = direction: UP, DOWN, LEFT, RIGHT
    def __init__(self, state, a, R):
        self.state = state
        self.a = a
        self.val = R
        self.next_val = R

    def calc_next_val(self):
        sum = 0
        for dir in con.directions:
            sum += self.p(dir) * next_state(self.state, dir).max_Q().val
        self.next_val = self.state.R + self.state.gamma * sum
        self.next_val

    # directions = [UP, DOWN, LEFT, RIGHT]
    def p(self, dir):
        if dir == self.a:
            return 0.8
        elif dir == con.opposite[self.a]:
            return 0
        else:
            return 0.1


if __name__ == "__main__":
    board = []
    main()
