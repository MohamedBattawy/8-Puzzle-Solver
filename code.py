import copy
import math
from collections import deque


def get1_h(state,player):
    h1 = 0 # column
    for i in range(7):  # column by column
        for j in range(0, 2):  # check every 4 consecutive places
            r_sum = 0  # number of red bits
            for k in range(j, j + 4):
                if k >= len(state[i]):
                    continue
                if state[i][k] == player:
                    r_sum += 1
                else:
                    r_sum = 0
                    break
            if r_sum:
                h1 += 2 ** r_sum

    h2 = 0 # row
    for j in range(6):
        for i in range(4):
            a_sum = 0
            for k in range(i, i + 4):
                if len(state[k]) < j + 1:  # revise
                    continue
                elif state[k][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
            if a_sum:
                h2 += 2 ** a_sum

    h3 = 0  # diagonal1
    for k in range(3):  # diagonal 1 part 2
        j_initial = 5
        i_initial = k + 1
        for counter in range(3 - k):  # number of 4 consecutive places in this diagonal
            i = i_initial + counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i += 1
                    j -= 1
                    continue
                elif state[i][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i += 1
                j -= 1
            if a_sum:
                h3 += 2 ** a_sum
    for k in range(3):  # diagonal 1 part 1
        j_initial = k + 3
        i_initial = 0
        for counter in range(k + 1):  # number of 4 consecutive places in this diagonal
            i = i_initial + counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i += 1
                    j -= 1
                    continue
                elif state[i][j]:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i += 1
                j -= 1
            if a_sum:
                h3 += 2 ** a_sum

    h4 = 0  # diagonal 2
    for k in range(3):  # diagonal 2 part 1
        j_initial = 3 + k
        i_initial = 6
        for counter in range(k + 1):  # num is number of 4 consecutive places in this diagonal
            i = i_initial - counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i -= 1
                    j -= 1
                    continue
                elif state[i][j] == player:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i -= 1
                j -= 1
            if a_sum:
                h4 += 2 ** a_sum
    for k in range(3):  # diagonal 2 part 2
        j_initial = 5
        i_initial = 5 - k
        for counter in range(3 - k):  # number of 4 consecutive places in this diagonal
            i = i_initial - counter  # start point
            j = j_initial - counter
            a_sum = 0
            limit = j - 4
            while j > limit:
                if len(state[i]) < j + 1:
                    i -= 1
                    j -= 1
                    continue
                elif state[i][j]:
                    a_sum += 1
                else:
                    a_sum = 0
                    break
                i -= 1
                j -= 1
            if a_sum:
                h4 += 2 ** a_sum
    return h1+h2+h3+h4


def get_heuristic(state):
    return get1_h(state, False)-get1_h(state, True)


def get_neighbours(state, player):  # player is an integer or a boolean either 0 or 1
    neighbours = deque()
    # in each column try adding a bit then add to the list and remove the bit to try in another column
    for i in range(7):
        if len(state[i]) == 6:  # column is full
            continue
        state[i].append(player)
        neighbours.append(copy.deepcopy(state))
        state[i].pop()
    return neighbours


def minimax(state, k, player):
    if k == 0 or (len(state[0]) == 6 and len(state[1]) == 6 and len(state[2]) == 6 and len(state[3]) == 6 and len(
            state[4]) == 6 and len(state[5]) == 6 and len(state[6]) == 6):
        return state, get_heuristic(state)
    neighbours = get_neighbours(state, player)
    if player == 0:
        bound = -math.inf
        for i in range(len(neighbours)):
            child, value = minimax(neighbours[i], k - 1, 1)
            if value > bound:
                bound = value
                best = neighbours[i]
        return best, bound
    elif player == 1:
        bound = math.inf
        for i in range(len(neighbours)):
            child, value = minimax(neighbours[i], k - 1, 0)
            if value < bound:
                bound = value
                best = neighbours[i]
        return best, bound


def alpha_beta(state, k, player):
    return alphabeta(state, k, player, -math.inf, math.inf)


def alphabeta(state, k, player, alpha, beta):
    if k == 0 or (len(state[0]) == 6 and len(state[1]) == 6 and len(state[2]) == 6 and len(state[3]) == 6 and len(
            state[4]) == 6 and len(state[5]) == 6 and len(state[6]) == 6):
        return state, get_heuristic(state)
    neighbours = get_neighbours(state, player)
    if player == 0:
        bound = -math.inf
        for i in range(len(neighbours)):
            child, value = alphabeta(neighbours[i], k - 1, 1, alpha, beta)
            if value > bound:
                bound = value
                best = neighbours[i]
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        return best, bound
    elif player == 1:
        bound = math.inf
        for i in range(len(neighbours)):
            child, value = alphabeta(neighbours[i], k - 1, 0, alpha, beta)
            if value < bound:
                bound = value
                best = neighbours[i]
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return best, bound
