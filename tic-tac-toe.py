from random import randrange
import os
import sys
from time import sleep
from colorama import Style, Fore
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

class EndGame(Exception):
    pass

COMPUTER_SYMBOL = "X"
USER_SYMBOL = "O"
VERDICTS = {
    'O': 'you won!',
    'X': 'the computer won!',
    'tie': "it's a tie!",
    'continue': 'continue'
}

position = {
    '1': (0,0),
    '2': (0,1),
    '3': (0,2),
    '4': (1,0),
    '5': (1,1),
    '6': (1,2),
    '7': (2,0),
    '8': (2,1),
    '9': (2,2)
}

def play_sound(sound_file, game_start=False):
    mixer.init()
    mixer.music.load(sound_file)
    mixer.music.play()
    if not game_start:
        while mixer.music.get_busy():  # wait for music to finish playing
            sleep(0.1)                 # otherwise the music.play() which is a thread gets killed 

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def color(cell):
    if cell == COMPUTER_SYMBOL:
        return Fore.RED + str(cell) + Style.RESET_ALL
    elif cell == USER_SYMBOL:
        return Fore.GREEN + str(cell) + Style.RESET_ALL
    else:
        return str(cell) + Style.RESET_ALL

def display_board(board):
    # The function accepts one parameter containing the board's current status
    # and prints it out to the console.
    p, d, t, c, p2, s, s2, o, d2 =  board[0][0], board[0][1], board[0][2],\
                                board[1][0], board[1][1], board[1][2],\
                                board[2][0], board[2][1], board[2][2]
    board_display = f"""
    computer's score = {computer_score}
    your score = {user_score}
    +-------+-------+-------+
    |       |       |       |
    |   {color(p)}   |   {color(d)}   |   {color(t)}   |
    |       |       |       |
    +-------+-------+-------+
    |       |       |       |
    |   {color(c)}   |   {color(p2)}   |   {color(s)}   |
    |       |       |       |
    +-------+-------+-------+
    |       |       |       |
    |   {color(s2)}   |   {color(o)}   |   {color(d2)}   |
    |       |       |       |
    +-------+-------+-------+
    """
    clear_screen()
    print(board_display)


def enter_move(board):
    while True:
        try:
            users_move = input("Enter a position: ")   
            int(users_move)
            board[position[users_move][0]][position[users_move][1]]    
            break
        except ValueError:
            print("You didn't input a number!")
        except KeyError:
            print("Your position is off board!")
    
    if type(board[position[users_move][0]][position[users_move][1]]) == int:
        # assign after it is available
        board[position[users_move][0]][position[users_move][1]] = USER_SYMBOL
    else:
        print("Position already taken")
        enter_move(board)

def check_free_fileds(board):
    free_fileds = []
    for row in range(3):
        for col in range(3):
            try:
                int(board[row][col])
                free_fileds.append( (row, col) )
            except ValueError:
                pass
    if free_fileds:
        pass
    else:
        print(VERDICTS['tie'])
        raise EndGame

def analyze(board):
    # The function analyzes the board's status in order to check if 
    # the player using 'O's or 'X's has won the game
    global user_score
    global computer_score
    for row in board:
        tmp = ""
        for val in row:
            tmp += str(val)
        #DEBUG
        #print(tmp)
        if tmp == COMPUTER_SYMBOL * 3:
            computer_score += 1
            display_board(board)
            print(VERDICTS[COMPUTER_SYMBOL])
            play_sound("sounds/videogame-death-sound-43894.mp3")
            raise EndGame
        elif tmp == USER_SYMBOL * 3:
            user_score += 1
            display_board(board)
            print(VERDICTS[USER_SYMBOL])
            play_sound("sounds/winsquare-6993.mp3")
            raise EndGame
        
    for row in range(3):
        tmp = ""
        for col in range(3):
            tmp += str(board[col][row])
        #DEBUG
        #print(tmp)
        if tmp == COMPUTER_SYMBOL * 3:  
            computer_score += 1
            display_board(board)
            print(VERDICTS[COMPUTER_SYMBOL])
            play_sound("sounds/videogame-death-sound-43894.mp3")
            raise EndGame
        elif tmp == USER_SYMBOL * 3:
            user_score += 1
            display_board(board)
            print(VERDICTS[USER_SYMBOL])
            play_sound("sounds/winsquare-6993.mp3")
            raise EndGame
    
    tmp = str(board[0][0]) + str(board[1][1]) + str(board[2][2])
    tmp2 = str(board[0][2]) + str(board[1][1]) + str(board[2][0])
    #DEBUG
    #print("final check")
    #print(tmp)
    #print(tmp2)
    if tmp == COMPUTER_SYMBOL*3 or tmp2 == COMPUTER_SYMBOL*3:
        computer_score += 1
        display_board(board)
        print(VERDICTS[COMPUTER_SYMBOL])
        play_sound("sounds/videogame-death-sound-43894.mp3")
        raise EndGame
    elif tmp == USER_SYMBOL*3 or tmp2 == USER_SYMBOL*3:
        user_score += 1
        display_board(board)
        print(VERDICTS[USER_SYMBOL])
        play_sound("sounds/winsquare-6993.mp3")
        raise EndGame

def draw_move(board):
    # The function draws the computer's move and updates the board.
    computers_move = randrange(1,10)
    # check if position is available
    if type(board[position[str(computers_move)][0]][position[str(computers_move)][1]]) == int:
        # assign after it is available
        board[position[str(computers_move)][0]][position[str(computers_move)][1]] = COMPUTER_SYMBOL
    else:
        #print("Computer drawing again!")
        draw_move(board)

if __name__ == "__main__":
    try:
        randomize = input("computer's first position should be random? y/n: ")
        if randomize == "n" or randomize == "N":
            randomize = False
        else:
            randomize = True
        board = [[i for i in range(j+1,j+4)] for j in range(0, 9, 3)]
        if not randomize:
            board[1][1] = COMPUTER_SYMBOL
        user_score = 0
        computer_score = 0
        again=True
        while again:
            play_sound("sounds/game-start-6104.mp3", True)
            display_board(board)
            try:
                while True:
                    # users move
                    print("users move")
                    enter_move(board)
                    display_board(board)
                    analyze(board)
                    check_free_fileds(board)
                    # computers move
                    print("computers move")
                    draw_move(board)
                    display_board(board)
                    analyze(board)
                    check_free_fileds(board)
            except EndGame:
                again = input("play again? y/n: ")
                if again == 'n' or again == 'N':
                    again = False
                    print("Exiting game.")
                else:
                    again = True
                    board = [[i for i in range(j+1,j+4)] for j in range(0, 9, 3)]
                    if not randomize:
                        board[1][1] = COMPUTER_SYMBOL
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected.")
        print("Closing game.")
        sleep(0.3)
