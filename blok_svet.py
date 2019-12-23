from tabulate import tabulate
import constants as con
from random import random, seed


def init_board(n, g):
    board.clear()
    for i in range(con.ROWS):
        row = []
        for j in range(con.COLS):
            if (i, j) == con.GOAL:
                row.append(State((i, j), con.POS, g))
            elif (i, j) == con.FAIL:
                row.append(State((i, j), n, g))  # con.NEG
            elif (i, j) != con.WALL:
                row.append(State((i, j), con.NEUT, g))
            else:
                row.append(None)
        board.append(row)
    return board


def policy(S):
    return S.max_Q().a


def print_policy_table(n):
    policy_table = []
    for i in range(con.ROWS):
        row = []
        for j in range(con.COLS):
            if (i, j) == con.GOAL:
                row.append(str(con.POS))
            elif (i, j) == con.FAIL:
                row.append(str(n))  # con.NEG
            elif (i, j) != con.WALL:
                row.append(transform(policy(board[i][j])))
            else:
                row.append('W')
        policy_table.append(row)
    print(tabulate(policy_table, tablefmt='psql'))


def next_state(S, dir):
    x, y = S[0], S[1]
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
        return u'\u2191'
    elif dir == con.DOWN:
        return u'\u2193'
    elif dir == con.LEFT:
        return u'\u2190'
    else:
        return u'\u2192'


def main():
    # for n in con.NEG:
    #     print()
    #     print('NEGATIVE....................................................', n)
    #     for g in con.GAMMA:
    #         print('GAMMA: ', g, '-------------------------')
    #         init_board(n, g)
    #         for iteration in range(50):
    #             for i in range(len(board)):
    #                 if iteration == 49:
    #                     print()
    #                 for j in range(len(board[0])):
    #                     if (i, j) != con.WALL and (i, j) != con.GOAL and (i, j) != con.FAIL:
    #                         board[i][j].calc_Q()
    #                         if iteration == 49:
    #                             print(i, j, board[i][j].Q[0].next_val, board[i][j].Q[1].next_val,
    #                                   board[i][j].Q[2].next_val,
    #                                   board[i][j].Q[3].next_val)
    #             for i in range(len(board)):
    #                 for j in range(len(board[0])):
    #                     if (i, j) != con.WALL and (i, j) != con.GOAL and (i, j) != con.FAIL:
    #                         board[i][j].next_Q()
    #
    #         print_policy_table(n)
    #
    #         S_curr = board[con.START[0]][con.START[1]]
    #         while S_curr.S != con.GOAL and S_curr.S != con.FAIL:
    #             a = policy(S_curr)
    #             S_curr = next_state(S_curr.S, a)
    #             print(transform(a), S_curr.S)

    # print('###################################')
    # for i in range(len(board)):
    #     print()
    #     for j in range(len(board[0])):
    #         # S = board[i][j]
    #         # print(board)
    #         # for k in range(4):
    #         if board[i][j] is not None:
    #             print(i, j, 'Q', board[i][j].max_Q().val)

    environment, agent = Environment(0.9), Agent(0.9)
    while agent.epsilon > 0:
        a = agent.new_action()
        S, R = environment.simulator(a)
        agent.update(S, R)
        agent.print_Q()


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
            sum += self.p(dir) * next_state(self.state.S, dir).max_Q().val
        self.next_val = self.state.R + self.state.gamma * sum

    # directions = [UP, DOWN, LEFT, RIGHT]
    def p(self, dir):
        if dir == self.a:
            return con.P_HEAD
        elif dir == con.opposite[self.a]:
            return 0
        else:
            return con.P_SIDE


class Environment:

    def __init__(self, gamma):
        self.S = con.START
        self.n, self.gamma = -1, gamma
        self.board = init_board(self.n, self.gamma)
        seed(con.SEED)

    def reset(self):
        self.S = con.START

    def simulator(self, a):
        dirs = len(con.directions)
        r = random()
        if r < con.P_HEAD:
            state = next_state(self.S, a)
        elif r < con.P_HEAD + con.P_SIDE:
            state = next_state(self.S, con.directions[(a + (dirs - 1)) % dirs])
        else:
            state = next_state(self.S, con.directions[(a + 1) % dirs])
        return state.S, state.R


class Agent:

    def __init__(self, gamma):
        self.gamma, self.epsilon, self.alpha = gamma, 1, 0.1
        self.S, self.R = con.START, 0
        self.a = con.UP
        dirs = len(con.directions)
        self.q_table = []
        for i in range(con.ROWS):
            row = []
            for j in range(con.COLS):
                q = []
                for k in range(dirs):
                    q.append(0)
                row.append(q)
            self.q_table.append(row)

    @staticmethod
    def generate_action():
        r = random()
        index = int(r * 4)
        return con.directions[index]

    def max_action(self):
        x, y = self.S
        state_Q = self.q_table[x][y]
        max_Q, max_a = state_Q[0], 0
        for a in range(len(state_Q)):
            if max_Q < state_Q[a]:
                max_Q, max_a = state_Q[a], a
        return a, max_Q

    def new_action(self):
        r = random()
        if r < self.epsilon:
            self.epsilon -= con.EPSILON_DECAY
            self.a = self.generate_action()
        else:
            self.a = self.max_action()[0]
        return self.a

    def update(self, S, R):
        q = self.R + self.gamma * self.max_action()[1]
        x_old, y_old = self.S
        self.q_table[x_old][y_old][self.a] = (1 - self.alpha) * self.q_table[x_old][y_old][self.a] + self.alpha * q
        self.S, self.R = S, R

    def print_Q(self):
        print('-------------------------------')
        for i in range(len(self.q_table)):
            print()
            for j in range(len(self.q_table[0])):
                q = self.q_table[i][j]
                print('Q', i, j, '.__.__.', q[0], q[1], q[2], q[3])


if __name__ == "__main__":
    board = []
    main()
