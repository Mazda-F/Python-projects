import random
import time

#Game Board
board = [" "] * 9

def draw_board():
    print('-------------')
    print('|', board[0], '|', board[1], '|', board[2], '|')
    print('----+---+----')
    print('|', board[3], '|', board[4], '|', board[5], '|')
    print('----+---+----')
    print('|', board[6], '|', board[7], '|', board[8], '|')
    print('-------------')


#Choosing Character
def choose_char():
    global computer_char
    global player_char
    player_char = input('Choose your character (O or X): ').strip().upper()

    if player_char == 'O':
        computer_char = 'X'

    elif player_char == 'X':
        computer_char = 'O'

    else:
        print('\nPlease choose a valid character.')    
        choose_char() 


#Checks for winning (True or False)
def winning(board, char):
    return ((board[0] == char and board[1] == char and board[2] == char) or 
    (board[3] == char and board[4] == char and board[5] == char) or 
    (board[6] == char and board[7] == char and board[8] == char) or 
    (board[0] == char and board[3] == char and board[6] == char) or 
    (board[1] == char and board[4] == char and board[7] == char) or 
    (board[2] == char and board[5] == char and board[8] == char) or 
    (board[0] == char and board[4] == char and board[8] == char) or 
    (board[2] == char and board[4] == char and board[6] == char))


def num_PossibleMoves():
    possibleMoves = []
    for index, letter in enumerate(board):
        if letter == ' ':
            possibleMoves.append(index)
    return len(possibleMoves)    

#Computer's move
def comp_move():
    move = 0

    #Gets all possible moves
    possibleMoves = []
    for index, letter in enumerate(board):
        if letter == ' ':
            possibleMoves.append(index)


    #Creates a board copy, and in there, it checks if any of the possible moves results in a win, if one of them dose, it returns that move
    for i in possibleMoves:
        boardCopy = board[:]
        boardCopy[i] = computer_char
        if winning(boardCopy, computer_char):
            return i


    #Creates a board copy, and in there, it checks if it can block any of the player's moves that result in a win
    for i in possibleMoves:
        boardCopy = board[:]
        boardCopy[i] = player_char
        if winning(boardCopy, player_char):
            return i

    # If the center is empty and there is no empty corner, it moves to the center
    if 4 in possibleMoves:
        return 4

    # Moves to a random possible corner
    cornersOpen = []
    for i in possibleMoves:
        if i in [0,2,6,8]:
            cornersOpen.append(i)
    if len(cornersOpen) > 0:
        return random.choice(cornersOpen)
        
    # Moves to a random possible edge
    edgesOpen = []
    for i in possibleMoves:
        if i in [1,3,5,7]:
            edgesOpen.append(i)
    if len(edgesOpen) > 0:
        return random.choice(edgesOpen)



#Main Game Func + Loop
def main():
    while winning(board, player_char) == False and winning(board, computer_char) == False:
        draw_board()

        try:
            user_input = input('Input move (1-9): ').strip()
            user_input = int(user_input)

            #Converting position from input to the game's index
            if user_input in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if board[user_input - 1] == ' ':
                    position = user_input - 1
                    board[position] = player_char
                    if comp_move() == None:
                        break
                    else:
                        board[comp_move()] = computer_char

                else:
                    print('This postion is already occupied!\n')
                    main()
                    
            else:
                print('Please type a number within the range!\n')
                main()

        except:
            print('Invalid input!\n')
            main()
    
    final()


def final():
    if winning(board, player_char) == True:
        print("\nYou Win!")
        draw_board()
        time.sleep(3)


    elif winning(board, computer_char) == True:
        print("\nComputer Wins!")
        draw_board()
        time.sleep(3)

    else:
        print("\nTie!")
        draw_board()
        time.sleep(3)


choose_char()
main()

    
    

