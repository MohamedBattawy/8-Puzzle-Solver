from datetime import datetime

import PySimpleGUI as sg
import search
sg.theme('TanBlue')
l = ['BFS', 'DFS', 'A* (manhaten heuristic)', 'A* (euclidean distance heuristic)']
layout = [
    [sg.Text('8_Puzzle Game', font=24)],
    [sg.Text('Enter the puzzle configuration you wish to solve\n(with a zero in place of the empty slot):')],
    [sg.Input(size=(14, 1), justification='right', key='input'), sg.Button('Enter', size=(5, 1))],
    [sg.Text('Search method: ')],
    [sg.Combo(l, key='method', default_value=l[2], size=(20, 1))],
    [sg.Button(button_text='', key=1, button_color=sg.theme_background_color(), border_width=0),
     sg.Button(button_text="1", key=2, border_width=0, ),
     sg.Button(button_text="2", key=3, border_width=0), sg.Text(key='A1')],
    [sg.Button(button_text="3", key=4, border_width=0),
     sg.Button(button_text="4", key=5, border_width=0),
     sg.Button(button_text="5", key=6, border_width=0), sg.Text(key='A2')],
    [sg.Button(button_text="6", key=7, border_width=0),
     sg.Button(button_text="7", key=8, border_width=0),
     sg.Button(button_text="8", key=9, border_width=0), sg.Text(key='A3')],
    [sg.Button(key='next', button_text='Next', visible=False, border_width=0, size=(19, 1)),
     sg.Button(key='Start', button_text='Start', disabled=True, border_width=0, size=(19, 1))],
    [sg.Text(size=(15, 1), font=('Helvetica', 18), text_color='red', key='out')]]


def update_window(window, s):
    for i in range(9):
        if s[i] == '0':
            window[i + 1].update(button_color=sg.theme_background_color(), text='')
        else:
            window[i + 1].update(text=s[i], button_color=sg.theme_button_color())


window = sg.Window('8_Puzzle', layout, default_button_element_size=(5, 2), auto_size_buttons=False)

keys_entered = ''
while True:
    event, values = window.read()  # read the window
    if event == sg.WIN_CLOSED:  # if the X button clicked, just exit
        break
    elif event == 'Enter':
        a = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
        for i in values['input']:
            if i not in a:
                sg.popup('Invalid input')
            else:
                a.remove(i)
        if len(a) != 0:
            sg.popup('Invalid input')
        else:
            window['Start'].update(visible=True)
            window['next'].update(visible=False)
            window['Start'].update(visible=True)
            window['next'].update(visible=False)
            window['A1'].update('')
            window['A2'].update('')
            window['A3'].update('')
            permutation= values['input']
            update_window(window,permutation)
            window['Start'].update(disabled=False)
    elif event == 'Start':
        window['Start'].update(disabled=True)
        start_time = datetime.now().second*1e6+datetime.now().microsecond
        if values['method'] == 'A* (manhaten heuristic)':
            pMap, depth, exp = search.Astar(int(permutation), 'm')
        elif values['method'] == 'A* (euclidean distance heuristic)':
            pMap, depth, exp = search.Astar(int(permutation), 'e')
        elif values['method'] == 'DFS':
            pMap, depth, exp = search.dfs(int(permutation))
        elif values['method'] == 'BFS':
            pMap, depth, exp = search.bfs(int(permutation))
        finish_time = datetime.now().second*1e6+datetime.now().microsecond
        total_time = int((finish_time-start_time)/1000)
        print(start_time)
        print(finish_time)
        if pMap:
            q = search.get_the_path(pMap)
            it = iter(q)
            window['Start'].update(visible=False)
            window['next'].update(visible=True)
            window['A1'].update('Analytics:')
            window['A2'].update('Cost of path= ' + str(len(q)) + '\nMax depth= ' + str(depth))
            window['A3'].update('Nodes expanded= ' + str(exp)+'\nTime taken= '+str(total_time)+' ms')
        else:
            sg.popup('Unsolvable input')
    elif event == 'next':
        s = str(next(it))
        if len(s)<9:
            s='0'+s
        if s == '012345678':
            window['Start'].update(visible=True)
            window['next'].update(visible=False)
            window['A1'].update('')
            window['A2'].update('')
            window['A3'].update('')
        update_window(window,s)
    window['input'].update(values['input'])
