from classes import *
from functions import *
import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.SHOWN, 32)
pygame.display.set_caption("Domino")
font = pygame.font.SysFont("monospace", 26)
font2 = pygame.font.SysFont("monospace", 46)
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
# background = pygame.Surface(screen.get_size())
background = pygame.Surface((1500,300))

background2 = pygame.Surface(screen.get_size())

imgs = [] 
for i in range(7):
    imgs.append(pygame.image.load(str(i)+".jpg"))

##setup-------------------------

all_pieces = generateAllPieces()
# print(all_pieces,len(all_pieces))
q = 7
p1_i = generateP1Indices(q,all_pieces)
p2_i = generateP2Indices(q,all_pieces,p1_i)

p1Hand = generateHand(p1_i,all_pieces)
p2Hand = generateHand(p2_i,all_pieces)

# print(p1Hand)
# print(p2Hand)

try:
    begins,beginPiece = determineWhoBegins(p1Hand,p2Hand)
except:
    print("Ningun jugador tiene fichas pares,por defecto empieza p2")
    # raise Exception

# print(begins)

remaining = determineRemainingPieces(p1Hand,p2Hand,all_pieces)

###-------------------------

#it contains the moves made, the pieces
board = []

states = []

arrayRectStates = []

#for the board part
offsetX = 0

#for the tree part
offsetY = 10

player1Turn = True
if begins == "p1":
    player1Turn = False
firstMove(begins,beginPiece,p1Hand,p2Hand,board)

addToStates(p1Hand,p2Hand,board,returnPlayer(not player1Turn),states,remaining)

addToCollisionStates(states,arrayRectStates,offsetY)

endOfGame = False

on = True

showTree = False

mouseRect = pygame.Rect(0,0,1,1)

whoWon = False

itIsADraw = 0

while on:
    
    screen.fill((50,50,50))
    mouseRect.x,mouseRect.y = pygame.mouse.get_pos()
    mouseRect.x -= 5


    if showTree == False:
        pygame.key.set_repeat(100)

        screen.blit(background,(20,350))
        background.fill((50,50,50))
        drawMouse(screen,mouseRect)
        screen.blit(font.render("a para mover a la izquierda, d para la derecha, r para hacer jugada aleatoria",True, (50,50,50), (255, 255, 255)),(20,940))
        screen.blit(font.render("h para hacer jugada con heurística, t para mostrar árbol",True, (50,50,50), (255, 255, 255)),(20,970))


        drawPiecesPlayer(p1Hand,screen,font,imgs,10,700,50)
        drawPiecesPlayer(p2Hand,screen,font,imgs,10,20,50)

        drawBoard2(board,background,font,imgs,offsetX,130,80)
        
        drawRemaining(remaining,screen,imgs,1750,100,50)

        if player1Turn:
            text2 = font.render("Turno jugador 1",True, (0,0,250), (255, 255, 255))
            pygame.draw.circle(screen,(200,200,200),(1500,900),50)
        else:
            text2 = font.render("Turno jugador 2",True, (250,0,0), (255, 255, 255))
            pygame.draw.circle(screen,(200,200,200),(1500,100),50)
        screen.blit(text2, (70,40))

    elif showTree == True:
        pygame.key.set_repeat(100)

        screen.blit(background2,(0,0))
        background2.fill((50,50,50))

        drawStates(states,screen,imgs,offsetY)
        drawCollisionStates(arrayRectStates,screen)
        col = detectCollision(arrayRectStates,mouseRect)

        #when the user hover a state it shows that state
        if col != None:
            # print("col",states[col])
            # print("col",states[col][0])#p1Hand
            # print("col",states[col][1])#p2Hand
            # print("col",states[col][2])#board
            # print("col",states[col][3])#turno
            # print("col",states[col][4])#remaining
            drawPiecesPlayer(states[col][0],screen,font,imgs,1200,700,20)
            drawPiecesPlayer(states[col][1],screen,font,imgs,1200,20,20)

            drawBoard2(states[col][2],screen,font,imgs,offsetX+1000,400,30)
        
            drawRemaining(states[col][5],screen,imgs,1850,100,20)
            drawTurn(screen,font,states[col][3],1100,700)
        screen.blit(font.render("a para mover a la izquierda, d para la derecha, r para hacer jugada aleatoria, t para volver al juego",True, (50,50,50), (255, 255, 255)),(20,940))
        screen.blit(font.render("w para mover arriba, s para mover abajo, h para hacer jugada con heurística",True, (50,50,50), (255, 255, 255)),(20,970))


    if endOfGame:
        text2 = font.render("Fin del juego",True, (0,0,0), (255, 255, 255))
        screen.blit(text2, (70,20))
        text4 = font2.render("Jugador {} ganó".format(whoWon),True, (0,0,0), (255, 255, 255))
        screen.blit(text4, (570,800))
        # states = states[:-1]
        # on = False
        # continue
        #exit

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            on = False
            break
        if e.type == pygame.KEYDOWN:

            if (e.unicode) == "q":
                on = False
                break

            #random move
            if ((e.unicode) == "r" or (e.unicode) == "h") and endOfGame == False:
                
                if player1Turn == True:

                    # print("p1Board",p1Hand)

                    if canAMoveBeMade(p1Hand,board):
                        # print(listPiecesThatCanBeUsed(p1Hand,board))
                        if (e.unicode) == "r":
                            makeRandomMove(p1Hand,board)
                        elif (e.unicode) == "h":
                            makeMaxMove(p1Hand,board)

                        # print(board)
                    else:
                        #pick a piece from the remaining

                        pickFromTheRemaining(remaining,p1Hand)


                elif player1Turn == False:
                    # print("p2Board",p2Hand)

                    if canAMoveBeMade(p2Hand,board):
                        # print(listPiecesThatCanBeUsed(p2Hand,board))
                        if (e.unicode) == "r":
                            makeRandomMove(p2Hand,board)
                        elif (e.unicode) == "h":
                            makeMaxMove(p2Hand,board)
                        # print(board)
                    else:
                        #pick a piece from the remaining
 
                        pickFromTheRemaining(remaining,p2Hand)
                        #if remaining is empty the turn is given to the other player
                whoWon = verifyIfP1AndP2HasPieces(p1Hand,p2Hand)
                addToStates2(p1Hand,p2Hand,board,player1Turn,states,remaining)
                addToCollisionStates(states,arrayRectStates,offsetY)
                player1Turn = not player1Turn

                # print(states)

                # print()

                # print(states[-1][4],len(states[-1][4]))
                # print(states[-1][4][0],len(states[-1][4][0]))

                if whoWon != False:#some player won
                    endOfGame = True
                    
                #a draw, no more pieces can be withdraw, and the users dont have a piece that fits to put in the board
                if determineIfNeitherUserCanPutApiece(remaining,states) == True:
                    endOfGame = True
                    whoWon = determineWhoWhonIfDraw(p1Hand,p2Hand)

            if (e.unicode) == "a":
                offsetX -= 10
            if (e.unicode) == "d":
                offsetX += 10
            if (e.unicode) == "t":
                showTree = not showTree
            # if (e.unicode) == "u":
            #     print(states)
            if (e.unicode) == "w":
                offsetY -= 10
                arrayRectStates = updateCollisionStates(arrayRectStates,offsetY)
            if (e.unicode) == "s":
                offsetY += 10
                arrayRectStates = updateCollisionStates(arrayRectStates,offsetY)
                
    # screen.blit(text, (70,10))

    pygame.display.update()

pygame.quit()