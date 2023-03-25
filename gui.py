import time
from datetime import datetime

import PySimpleGUI as sg
from bitarray import bitarray
import code

l = ['min-max', 'alpha-beta']
layout = [[sg.Text('Connect-4', font='Ravie', size=(28, 1), text_color='black', justification='center')],
          [sg.Button(key='new game',button_text="New Game",size=(9,1)),sg.Combo(l, key='method', default_value=l[0], size=(10, 1)), sg.Text('K=', text_color='black'),
           sg.Input(size=(5, 1), key='k', default_text='1'),sg.Text("Time Taken: ",text_color='black'),sg.Text(key='t')],
          [sg.Graph(canvas_size=(490, 420), graph_top_right=(490, 0), graph_bottom_left=(0, 420),
                    background_color='#0040ff', enable_events=True, key='graph')]
          ]

window = sg.Window('Connect4', layout, finalize=True)
graph = window['graph']
turn=0
board = []
for i in range(7):
    board.append(bitarray())

circles = [[0] * 7] * 6
for i in range(6):
    for j in range(7):
        circles[i][j] = graph.draw_circle(center_location=(70 * j + 35, 70 * i + 35), radius=30, fill_color='white')

while True:
    event, values = window.read()
    if event == "new game":
        turn = 0
        board = []
        for i in range(7):
            board.append(bitarray())

        circles = [[0] * 7] * 6
        for i in range(6):
            for j in range(7):
                circles[i][j] = graph.draw_circle(center_location=(70 * j + 35, 70 * i + 35), radius=30,
                                                  fill_color='white')
    if event == "graph":
        x, y = values["graph"]
        col = int(x / 70)
        place = len(board[col])
        if place < 6:
            row = 5 - place
            x = col * 70 + 35
            y = row * 70 + 35
            board[col].append(True)
            newcircle = graph.draw_circle((x, 0), 30, 'red')
            for i in range(y):
                time.sleep(0.001)
                graph.MoveFigure(newcircle, 0, 1)
                window.refresh()
            if values['method'] == "min-max":
                start = datetime.now().minute*60+datetime.now().second
                child,h = code.minimax(board, int(values['k']), 0)
                window['t'].update(str(datetime.now().minute*60+datetime.now().second-start)+'s')
            elif values['method'] == "alpha-beta":
                start = datetime.now().minute * 60 + datetime.now().second
                child, h = code.alpha_beta(board, int(values['k']), 0)
                window['t'].update(str(datetime.now().minute * 60 + datetime.now().second - start) + 's')
            for i in range(7):
                if len(child[i]) - len(board[i]):
                    col = i
                    break
            place = len(board[col])
            row = 5 - place
            x = col * 70 + 35
            y = row * 70 + 35
            board[col].append(False)
            newcircle = graph.draw_circle((x, 0), 30, 'green')
            for i in range(y):
                time.sleep(0.001)
                graph.MoveFigure(newcircle, 0, 1)
                window.refresh()
            turn += 1
            if turn == 21:
                Computer = code.col_h(board, False) + code.row_h(board, False) + code.d1_h(board, False) + code.d2_h(board, False)
                Player = code.col_h(board, True) + code.row_h(board, True) + code.d1_h(board, True) + code.d2_h(board, True)
                sg.popup("Game ended\nComputer score =", int(code.get_heuristic(board)/16))

    if event == sg.WIN_CLOSED:
        break

window.close()
