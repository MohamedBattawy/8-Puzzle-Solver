import collections
import heapq
import math
from collections import deque


def get_zero(state):  # function to get the location of the zero in the integer
    count = 1
    base = int(state % 10)
    while base:
        state = int(state / 10)
        base = int(state % 10)
        count = count + 1
    return count


def zero_shift(state, p1, p2):
    m = int((state / 10 ** p1) % 10)
    state = state + m * (10 ** p2 - 10 ** p1)
    return state


def get_neighbours(state):
    q = deque()
    location = get_zero(state)
    p2 = location - 1
    if location <= 6:
        p1 = location + 2
        q.append(zero_shift(state, p1, p2))
    if location >= 4:
        p1 = location - 4
        q.append(zero_shift(state, p1, p2))
    if location % 3 != 1:
        p1 = location - 2
        q.append(zero_shift(state, p1, p2))
    if location % 3 != 0:
        p1 = location
        q.append(zero_shift(state, p1, p2))
    return q


def manhaten(state):
    c = 1
    h = 0
    while state:
        m = int(state % 10)
        if m > 0:
            m = m + c
            if m % 3 == 0:
                x = 0
            else:
                if c % 3 == 1:
                    x = 3 - m % 3
                    m = m + x
                elif c % 3 == 2:
                    x = 1
                    if m % 3 == 1:
                        m = m - 1
                    else:
                        m = m + 1
                else:
                    x = m % 3
                    m = m - x
            y = int(abs(m - 9) / 3)
            h = int(h + (x + y))
        c = c + 1
        state = int(state / 10)
    return h


def euclid(state):
    c = 1
    h = 0
    while state > 0:
        m = int(state % 10)
        if m > 0:
            m = m + c
            if m % 3 == 0:
                x = 0
            else:
                if c % 3 == 1:
                    x = 3 - m % 3
                    m = m + x
                elif c % 3 == 2:
                    x = 1
                    if m % 3 == 1:
                        m = m - 1
                    else:
                        m = m + 1
                else:
                    x = m % 3
                    m = m - x
            y = int(abs(m - 9) / 3)
            h = h + math.sqrt((x * x) + (y * y))
        c = c + 1
        state = int(state / 10)
    return h


def heuristic(state, h):
    if h == 'e':
        return euclid(state)
    if h == 'm':
        return manhaten(state)


def bfs(state):
    explored = set()
    frontier = deque()
    frontier_set = set()
    dic = dict()
    dic[state] = state
    frontier.append(state)
    frontier_set.add(state)
    mapcost = dict()
    max = 0  # used for max depth
    mapcost[state] = 0
    while frontier_set:
        state = frontier.popleft()
        if max < mapcost[state]:
            max = mapcost[state]
        if state == 12345678:
            return dic, max,len(explored)
        frontier_set.remove(state)
        s = get_neighbours(state)
        explored.add(state)
        for neighbour in s:
            if neighbour not in explored and neighbour not in frontier_set:
                dic[neighbour] = state
                frontier_set.add(neighbour)
                frontier.append(neighbour)
                mapcost[neighbour] = mapcost[state] + 1

    return None, max, len(explored)


def dfs(state):
    explored = set()
    frontier = deque()
    frontier_set = set()
    dic = dict()
    dic[state] = state
    frontier.append(state)
    frontier_set.add(state)
    mapcost = dict()
    max = 0  # used for max depth
    mapcost[state] = 0
    while frontier_set:
        state = frontier.pop()  # could have been done without opposite get_neighbours with frontier.popleft()
        if max < mapcost[state]:
            max = mapcost[state]
        if state == 12345678:
            return dic, max, len(explored)
        frontier_set.remove(state)
        s = reversed(get_neighbours(state))
        explored.add(state)
        for neighbour in s:
            if neighbour not in explored and neighbour not in frontier_set:
                dic[neighbour] = state
                frontier_set.add(neighbour)
                frontier.append(neighbour)
                mapcost[neighbour] = mapcost[state] + 1
    print('unsolvable')
    return None, max, len(explored)


def Astar(state, h):
    max = 0  # used for getting the max depth will be compared later on
    fofn = heuristic(state, h)  # f(n)=g(n)+h(n)
    explored = set()  # unordered list
    frontier = []  # will be priority queue
    frontier_set = set()  # for quick searching
    dic = dict()  # to get parent map
    mapcost = dict()  # to get costs of each node
    dic[state] = state  # insert initial parent of the root
    heapq.heappush(frontier, (fofn, state))  # pushing in priority queue
    mapcost[state] = fofn  # insert cost of parent which is the root
    frontier_set.add(state)
    while frontier_set:
        while state in explored:
            state = heapq.heappop(frontier)[1]
        if state == 12345678:
            return dic, int(round(max)), len(explored)

        frontier_set.remove(state)
        s = get_neighbours(state)
        explored.add(state)
        if max < mapcost[state] - heuristic(state, h) + 1:  # used to get max depth
            max = mapcost[state] - heuristic(state, h) + 1
        for neighbour in s:
            if neighbour not in explored and neighbour not in frontier_set:
                dic[neighbour] = state
                newcost = heuristic(neighbour, h) + mapcost[state] + 1 - heuristic(state,
                                                                                   h)  # 1 is the movement cost per state where cost of current node = manhatten this node + cost of parent - manhatten of parent +1 because we can't get the g(neighbour) directly
                frontier_set.add(neighbour)
                heapq.heappush(frontier, (newcost, neighbour))
                mapcost[neighbour] = newcost  # add the cost (not 1's the values) of the neighbour
            elif neighbour in frontier_set:
                newcost2 = heuristic(neighbour, h) + mapcost[state] + 1 - heuristic(state, h)
                if newcost2 < mapcost[neighbour]:  # the case of finding a smaller value when the node was visited again
                    mapcost[neighbour] = newcost2
                    dic[neighbour] = state
                    heapq.heappush(frontier, (newcost2,
                                              neighbour))  # no need to overwrite the old value but it doesn't matter because we will never reach it as the new value is smaller so it will get popped first
    return None, int(round(max)), len(explored)


def get_the_path(
        parent_map):  # TAKE NOTE THIS PRINTS THE STEPS REVERSELY FROM GOAL TO PARENT NOT FROM PARENT TO GOAL INITIALLY
    q = collections.deque()
    if parent_map is None: return q
    child = 12345678  # initial state
    parent = parent_map.get(child)  # get the parent of the goal state which is child here
    q.appendleft(child)
    while parent != child:
        q.appendleft(parent)
        child = parent  # otherwise the parent will loop on itself
        parent = parent_map.get(child)  # get the parent of the goal state which is child here
    q.popleft()
    return q