#---------------------------------------------------#
#                   Antonio Pelusi                  #
#---------------------------------------------------#


#-------------------- LIBRARIES --------------------#

import time as t
import numpy as np
import PySimpleGUI as sg


#---------------------- SETUP ----------------------#

sg.theme('Gray Gray Gray')

board = np.zeros(shape=(9,9), dtype=int)

speed = 0.

#-------------------- FUNCTIONS --------------------#

def read_board(board):
    for row in range(9):
            for column in range(9):
                if window[row,column].get() == '':
                    board[row,column] = 0

                else:
                    board[row,column] = window[row,column].get()

def write_board(board):
    for row in range(9):
        for column in range(9):
            window[row,column].update(board[row,column])
            window.finalize()

def solve(board, row, column, num):
    for x in range(9):
        if board[row][x] == num:
            return False
             
    for x in range(9):
        if board[x][column] == num:
            return False
 
 
    startRow = row - row % 3
    startCol = column - column % 3
    for i in range(3):
        for j in range(3):
            if board[i + startRow][j + startCol] == num:
                return False
            
    return True
 
def sudoku(board, row, column):
    if (row == 9 - 1 and column == 9):
        return True

    if column == 9:
        row += 1
        column = 0

    if board[row][column] > 0:
        return sudoku(board, row, column + 1)

    for num in range(1, 9 + 1, 1): 
     
        if solve(board, row, column, num):
         
            board[row][column] = num

            if speed != 0.:
                window[row,column].update(num)
                window.finalize()
                t.sleep(0)

            if sudoku(board, row, column + 1):
                return True
        
        board[row][column] = 0

        if speed != 0.:
            window[row,column].update('')
            window.finalize()
            t.sleep(speed)

    return False


#------------------ PROGRAM START ------------------#

layout = [[sg.Frame('', [[sg.Input('', justification='c', font=("Arial", 11, "bold"), background_color='lightgray', size=(3,1),enable_events=True, key=(fr*3+r,fc*3+c)) for c in range(3)] for r in range(3)]) for fc in range(3)] for fr in range(3)] + \
            [[sg.Button('Solve', key='Solve')] + \
            [sg.Button('Clear')] + \
            [sg.Button('Test')] + \
            [sg.Text('   Fast')] + \
            [sg.Slider((0, 1), disable_number_display=True, enable_events=True, default_value=0, key='Speed', orientation='h', size=(7, 15))] + \
            [sg.Text('Slow')]]

window = sg.Window('Sudoku Solver\t|\tAntonio Pelusi', layout, use_default_focus=False)

while True:
    event, values = window.read()

    if event == 'Solve':
        speed = values['Speed']/1000

        read_board(board)
        
        if board.sum() != 0:
            if (sudoku(board, 0, 0)):
                window['Solve'].Widget.config(background='#8def7c')
                window.finalize()
                
                if speed == 0.:
                    write_board(board)

            else:
                window['Solve'].Widget.config(background='#f46464')
                window.finalize()

                sg.popup('This sudoku\nhas no solution', no_titlebar=True, any_key_closes=True)

    elif event == 'Clear':
        window['Solve'].Widget.config(background='lightgrey')
        window.finalize()

        for row in range(9):
                log = ''
                for column in range(9):
                    window[row,column].update('')
                    board[row,column] = 0

    elif event == 'Test':
        window['Solve'].Widget.config(background='lightgrey')
        window.finalize()

        board[0,:] = [0,9,0,0,0,0,5,7,3]
        board[1,:] = [8,0,0,0,2,0,0,0,0]
        board[2,:] = [7,0,0,9,0,0,8,1,0]
        board[3,:] = [5,8,0,7,0,6,0,0,0]
        board[4,:] = [0,0,1,8,0,0,0,6,0]
        board[5,:] = [2,3,0,0,4,0,0,0,9]
        board[6,:] = [9,1,5,0,0,0,0,0,0]
        board[7,:] = [0,0,0,0,8,0,6,0,1]
        board[8,:] = [0,0,0,0,0,0,0,4,0]

        for row in range(9):
                for column in range(9):
                    if board[row,column] == 0:
                        window[row,column].update('')
                    else:
                        window[row,column].update(board[row,column])

    elif event == 'Speed':
        speed = values[event]/1000

    elif event == sg.WIN_CLOSED:
        break

window.close()