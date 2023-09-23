import itertools
import random
import pygame
import copy

def generateAllPieces():
    all_pieces = list(itertools.combinations('0123456', 2))

    for i in range(7):
        all_pieces.append((str(i),str(i)))

    for i in range(len(all_pieces)):
        all_pieces[i] = [int(all_pieces[i][0]),int(all_pieces[i][1])]

    return all_pieces

def generateNRandomIndices(quantity,all_pieces):
    visited = []
    while quantity>0:
        x = random.randint(0,len(all_pieces)-1)
        if x not in visited:
            quantity -= 1
            visited.append(x)
    return visited
    # print(visited)

def generateP1Indices(quantity,all_pieces):
    return generateNRandomIndices(quantity,all_pieces)
    
def generateP2Indices(quantity,all_pieces,p1_i):
    visited = []
    while quantity>0:
        x = random.randint(0,len(all_pieces)-1)
        if x not in visited and x not in p1_i:
            quantity -= 1
            visited.append(x)
    return visited

def generateHand(arrayIndices,all_pieces):
    arr = []
    for i in arrayIndices:
        arr.append(all_pieces[i])
    return arr

def determineWhoBegins(p1Hand,p2Hand):
    max_p1 = [0,0]
    max_p2 = [0,0]
    for i in p1Hand:
        if i[0] > max_p1[0] and i[1] > max_p1[1] and i[0] == i[1]:
            max_p1 = [i[0],i[1]] 
    for i in p2Hand:
        if i[0] > max_p2[0] and i[1] > max_p2[1] and i[0] == i[1]:
            max_p2 = [i[0],i[1]] 
    
    # print(max_p1,max_p2)
    if max_p1[0] > max_p2[0]:
        return "p1",max_p1
    elif max_p1[0] < max_p2[0]:
        return "p2",max_p2
    else:
        # print("no se encontraron valores iguales para iniciar el juego")
        # raise Exception
        return "p2"

def determineRemainingPieces(p1Hand,p2Hand,all_pieces):
    arr = []
    for i in range(len(all_pieces)):
        if all_pieces[i] in p1Hand or all_pieces[i] in p2Hand:
            continue
        else:
            arr.append(all_pieces[i])
    # print("remaining",arr)
    return arr


#------------------

def drawPiecesPlayer(p1Orp2Hand,screen,font,imgs,offsetX=0,offsetY=0,width=50):
    height = width*2
    margin = 10
    color = (100,200,200)
    for i in range(len(p1Orp2Hand)):
        pygame.draw.rect(screen,color,((i*(width+margin))+offsetX,offsetY+(height+margin),width,height),3)
        # pygame.draw.rect(screen,color,(((i+5) * offsetX),offsetY,50,100),3)
        
        screen.blit(pygame.transform.scale(imgs[p1Orp2Hand[i][0]],(width,width)),((i*(width+margin))+offsetX,offsetY+(height+margin)))
        screen.blit(pygame.transform.scale(imgs[p1Orp2Hand[i][1]],(width,width)),((i*(width+margin))+offsetX,offsetY+(height//2)+(height+margin)))
        # screen.blit(font.render(str(p1Orp2Hand[i][0]),True, (0,0,0), (255, 255, 255)),(((i+5) * offsetX),offsetY))
        # screen.blit(font.render(str(p1Orp2Hand[i][1]),True, (0,0,0), (255, 255, 255)),(((i+5) * offsetX),offsetY+50))
        pygame.draw.rect(screen,(50,50,50),((i*(width+margin))+offsetX,offsetY+(height//2)+(height+margin),50,1))
#modifies p1Hand or p2Hand and board
def firstMove(begins,piece,p1Hand,p2Hand,board):
    #!
    board.append(piece)
    try:
        if begins == "p1":
            p1Hand.remove(piece)
        else:
            p2Hand.remove(piece)
    except:
        raise Exception

def drawBoard(board,screen,font,imgs,offsetX=0,offsetY=0):
    width = 100
    height = 50
    for i in range(len(board)):
        # if board[i][0] != board[i][1] : 
        screen.blit(pygame.transform.rotate (imgs[board[i][0]],90),(offsetX+(width*(i+1)),offsetY))

        screen.blit(pygame.transform.rotate(imgs[board[i][1]],90),(offsetX+(width*(i+1))+(width//2),offsetY))
        pygame.draw.rect(screen,(50,50,50),(offsetX+(width*(i+1))+(width//2),offsetY,1,height))

        pygame.draw.rect(screen,(50,50,50),(offsetX+((width*(i+1))),offsetY,width,height),2)
        # screen.blit(font.render(str(board[i][0]),True, (0,0,0), (255, 255, 255)),(offsetX+((width*(i+1))),offsetY))
        # screen.blit(font.render(str(board[i][1]),True, (0,0,0), (255, 255, 255)),(offsetX+(width*(i+1))+(width//2),offsetY))
        # else:
        #     pygame.draw.rect(screen,color,(((i+1)*(width)),offsetY-(height//2),height,width),3)
            # pygame.draw.rect(screen,color,(((i+5) * offsetX),offsetY,50,100),3)
            
            # screen.blit(imgs[board[i][0]],((i*(width))+offsetX,offsetY+(height)))
            # screen.blit(imgs[board[i][1]],((i*(width))+offsetX,offsetY+(height//2)+(height)))
            # # screen.blit(font.render(str(p1Orp2Hand[i][0]),True, (0,0,0), (255, 255, 255)),(((i+5) * offsetX),offsetY))
            # # screen.blit(font.render(str(p1Orp2Hand[i][1]),True, (0,0,0), (255, 255, 255)),(((i+5) * offsetX),offsetY+50))
            # pygame.draw.rect(screen,(50,50,50),((i*(width))+offsetX,offsetY+(height//2)+(height),50,1))

#it is used ot determine wheter the player has a piece to play or if it has to withraw a piece

def verifyLeftMove(piece,board):
    if piece[0] == board[0][0] or piece[1] == board[0][0]:
        return True
    return False

def verifyRightMove(piece,board):
    if piece[0] == board[-1][1] or piece[1] == board[-1][1]:
        return True
    return False

def canAMoveBeMade(p1Orp2Hand,board):
    for i in p1Orp2Hand:
        ##verify this
        if verifyLeftMove(i,board) == True or verifyRightMove(i,board) == True:
            #at least a move can be made
            return True
    return False

def listPiecesThatCanBeUsed(p1Orp2Hand,board):
    arr = []
    for i in p1Orp2Hand:
        if verifyLeftMove(i,board) == True or verifyRightMove(i,board) == True:
            arr.append(i)
    return arr

def addToTheLeft(piece,board):
    if piece[0] == board[0][0]:
        board.insert(0,([piece[1],piece[0]]))
    elif piece[1] == board[0][0]:
        board.insert(0,(piece))

def addToTheRight(piece,board):
    if piece[0] == board[-1][1]:
        board.append(piece)
    elif piece[1] == board[-1][1]:
        board.append([piece[1],piece[0]])

#it uses the functions above
def makeRandomMove(p1Orp2Hand,board):
    arr = listPiecesThatCanBeUsed(p1Orp2Hand,board)
    r = random.randint(0,len(arr)-1)
    if verifyLeftMove(arr[r],board) == True:
        p1Orp2Hand.remove(arr[r])
        addToTheLeft(arr[r],board)
        return
    elif verifyRightMove(arr[r],board) == True:
        p1Orp2Hand.remove(arr[r])
        addToTheRight(arr[r],board)
        return
    
def makeMaxMove(p1Orp2Hand,board):
    arr = listPiecesThatCanBeUsed(p1Orp2Hand,board)
    maxim = 0
    index_of_major = 0
    for i in range(len(arr)):
        if arr[i][0] + arr[i][1] > maxim:
            maxim = arr[i][0] + arr[i][1]
            index_of_major = i
    r = index_of_major
    if verifyLeftMove(arr[r],board) == True:
        p1Orp2Hand.remove(arr[r])
        addToTheLeft(arr[r],board)
        return
    elif verifyRightMove(arr[r],board) == True:
        p1Orp2Hand.remove(arr[r])
        addToTheRight(arr[r],board)
        return

def makeMinMove(p1Orp2Hand,board):
    arr = listPiecesThatCanBeUsed(p1Orp2Hand,board)
    minim = 15
    index_of_minor = 0
    for i in range(len(arr)):
        if arr[i][0] + arr[i][1] < minim:
            minim = arr[i][0] + arr[i][1]
            index_of_minor = i
    r = index_of_minor
    if verifyLeftMove(arr[r],board) == True:
        p1Orp2Hand.remove(arr[r])
        addToTheLeft(arr[r],board)
        return
    elif verifyRightMove(arr[r],board) == True:
        p1Orp2Hand.remove(arr[r])
        addToTheRight(arr[r],board)
        return

def remainingPiecesIsEmpty(remaining):
    if len(remaining)<=0:
        return True
    return False

def pickFromTheRemaining(remaining,p1Orp2Hand):
    if remainingPiecesIsEmpty(remaining) == False:
        r = random.randint(0,len(remaining)-1)
        p1Orp2Hand.append(remaining[r])
        remaining.remove(remaining[r])
    # print("remaining is empty")
    # print("the turn is for the other player")
    return False

def drawRemaining(remaining,screen,imgs,offsetX=0,offsetY=0,width=50):
    height = width*2
    color = (150,250,0)
    margin = 10
    count = -1
    aux = 0
    for i in range(len(remaining)):
        count += 1
        pygame.draw.rect(screen,color,((count*(width+margin))+offsetX,offsetY+(aux*(height+margin)),width,height),3)
        screen.blit(pygame.transform.scale(imgs[remaining[i][0]],(width,width)),((count*(width+margin))+offsetX,offsetY+(aux*(height+margin))))
        screen.blit(pygame.transform.scale(imgs[remaining[i][1]],(width,width)),((count*(width+margin))+offsetX,offsetY+(height//2)+(aux*(height+margin))))
        pygame.draw.rect(screen,(50,50,50),((count*(width+margin))+offsetX,offsetY+(height//2)+(aux*(height+margin)),50,1))
        if count >0:
            count = -1
            aux += 1
        # screen.blit(font.render(str(p1Orp2Hand[i][0]),True, (0,0,0), (255, 255, 255)),(((i+5) * offsetX),offsetY))
        # screen.blit(font.render(str(p1Orp2Hand[i][1]),True, (0,0,0), (255, 255, 255)),(((i+5) * offsetX),offsetY+50))

#it draws the equal pieces as vertical the other horizaontal
def drawBoard2(board,screen,font,imgs,offsetX=0,offsetY=0,width=100):
    color = (100,200,200)
    height = width//2
    aux = height//2
    color = (50,50,50)
    varX = 0
    margin = 5
    for i in range(len(board)):
        #
        # pygame.draw.rect(screen,(0,250,0),((offsetX+((i+1)*(width))),offsetY+100,width,height),3)
        # screen.blit(font.render(str(board[i][0]),True, (0,0,0), (255, 255, 255)),((offsetX+((i+1)*(width))),offsetY+100))
        # screen.blit(font.render(str(board[i][1]),True, (0,0,0), (255, 255, 255)),((offsetX+((i+1)*(width)))+(width//2),offsetY+100))

        if board[i][0] != board[i][1]:
            #horizontal
            # pygame.draw.rect(screen,color,((varX*(width//2))-(offsetX+(width*(i+1)))+(width//2),offsetY,1,height))
            # pygame.draw.rect(screen,color,((varX*(width//2))-(offsetX+((width*(i+1)))),offsetY,width,height),2)
            # pygame.draw.rect(screen,(0,250,0),(offsetX+(((i+1)*(width+margin))-(varX*(width//2))),offsetY-100,width,height))
            screen.blit(pygame.transform.scale(pygame.transform.rotate (imgs[board[i][0]],90),(height,height)),(offsetX+(((i+1)*(width+margin))-(varX*(width//2))),offsetY))
            screen.blit(pygame.transform.scale(pygame.transform.rotate(imgs[board[i][1]],90),(height,height)),((width//2)+offsetX+(((i+1)*(width+margin))-(varX*(width//2))),offsetY))
            pygame.draw.rect(screen,color,(offsetX+(((i+1)*(width+margin))-(varX*(width//2)))+(width//2),offsetY,2,height),3)
        # screen.blit(font.render(str(board[i][0]),True, (0,0,0), (255, 255, 255)),(offsetX+((width*(i+1))),offsetY))
        # screen.blit(font.render(str(board[i][1]),True, (0,0,0), (255, 255, 255)),(offsetX+(width*(i+1))+(width//2),offsetY))
        else:
            #vertical

            pygame.draw.rect(screen,color,(offsetX+(((i+1)*(width+margin))-(varX*(width//2))),offsetY-(height//2),height,width),3)
            # screen.blit(imgs[board[i][0]],(offsetX+(((i+1)*(width+margin))-(varX*(width//2))),offsetY-(height//2)))
            screen.blit(pygame.transform.scale(imgs[board[i][0]],(height,height)),(offsetX+(((i+1)*(width+margin))-(varX*(width//2))),offsetY-(height//2)))
            screen.blit(pygame.transform.scale(imgs[board[i][1]],(height,height)),(offsetX+(((i+1)*(width+margin))-(varX*(width//2))),(width//2)+offsetY-(height//2)))

            pygame.draw.rect(screen,color,(offsetX+(((i+1)*(width+margin))-(varX*(width//2))),offsetY-(height//2)+height,height,2),3)
            varX += 1
            
            # screen.blit(imgs[board[i][1]],((i*(width))+offsetX,offsetY+(height//2)+(height)))
            # # screen.blit(font.render(str(p1Orp2Hand[i][1]),True, (0,0,0), (255, 255, 255)),(((i+5) * offsetX),offsetY+50))
            # pygame.draw.rect(screen,color,((i*(width))+offsetX,offsetY+(height//2)+(height),50,1))

def returnPlayer(player1Turn):
    if player1Turn == True:
        return 1
    elif player1Turn == False:
        return 2

def generatePossibleStates(p1Hand,p2Hand,board,whichPlayerHasToDoTheMove):
    possibleMoves = []
    if whichPlayerHasToDoTheMove == 1:
        if canAMoveBeMade(p1Hand,board) == True:
            possibleMoves.append(listPiecesThatCanBeUsed(p1Hand,board))
        else:
            arr = []
            possibleMoves.append(arr)
    elif whichPlayerHasToDoTheMove == 2:
        if canAMoveBeMade(p2Hand,board) == True:
            possibleMoves.append(listPiecesThatCanBeUsed(p2Hand,board))
        else:
            arr = []
            possibleMoves.append(arr)
    return possibleMoves

def addToStates(p1Hand,p2Hand,board,whichPlayerDidTheMove,states,remaining):

    if whichPlayerDidTheMove == 1:
        p = 2
    else:
        p = 1
    possibleMoves = generatePossibleStates(p1Hand,p2Hand,board,p)
    arr = [p1Hand,p2Hand,board,whichPlayerDidTheMove,possibleMoves,remaining]
    arr2 = copy.deepcopy(arr)
    states.append(arr2)
    # print()
    # print(states[0])
    # print()
    # print("p1Hand",states[0][0])
    # print()
    # print("p2Hand",states[0][1])
    # print()
    # print("board",states[0][2])
    # print()
    # print("whichPlayerDidTheMove",states[0][3])
    # print()
    # print("PossibleMoves for the other player",states[0][4])

def addToStates2(p1Hand,p2Hand,board,player1Turn,states,remaining):
    p = 1
    if returnPlayer(player1Turn) == 1:
        p = 2

    possibleMoves = generatePossibleStates(p1Hand,p2Hand,board,p)

    arr = [p1Hand,p2Hand,board,returnPlayer(player1Turn),possibleMoves,remaining]
    arr2 = copy.deepcopy(arr)
    states.append(arr2)
    # print()
    # print(states[0])
    # print()
    # print("p1Hand",states[0][0])
    # print()
    # print("p2Hand",states[0][1])
    # print()
    # print("board",states[0][2])
    # print()
    # print("whichPlayerDidTheMove",states[0][3])
    # print()
    # print("PossibleMoves for the other player",states[0][4])

def drawStates(states,screen,imgs,offsetY=150):
    color1 = [200,200,200]
    color2 = [50,50,50]
    width = 20
    val = 150
    for i in range(len(states)):
        pygame.draw.circle(screen,color1,(500,((i+1)*val)+offsetY),width)
        for j in range(len(states[i][4][0])):
            pygame.draw.aaline(screen,color1,(500,((i+1)*val)+offsetY),(300+((j+1)*(100)),offsetY+80+((i+1)*val)))
            pygame.draw.circle(screen,color2,(300+((j+1)*(100)),offsetY+80+((i+1)*val)),width)
            screen.blit(pygame.transform.scale(imgs[states[i][4][0][j][0]],(25,25)),(300-12+((j+1)*(100)),offsetY+80-10+((i+1)*val)))
            screen.blit(pygame.transform.scale(imgs[states[i][4][0][j][1]],(25,25)),(300-12+((j+1)*(100)),offsetY+80+26-10+((i+1)*val)))

#every time a state is added
def addToCollisionStates(states,arrayRectStates,offsetY):
    width = 36
    val = 150
    i = len(states)-1
    arrayRectStates.append(pygame.Rect(500-17,((i+1)*val)+offsetY-17,width,width))

def drawCollisionStates(arrayRectStates,screen):
    pass
    # for i in arrayRectStates:
        # pygame.draw.rect(screen,(100,0,200),i,1)

def updateCollisionStates(arrayRectStates,offsetY=150):
    val = 150
    arrayRectStates2 = []
    width = 36
    for i in range(len(arrayRectStates)):
        arrayRectStates2.append(pygame.Rect(500-17,((i+1)*val)+offsetY-17,width,width))
    return arrayRectStates2

def drawMouse(screen,mouseRect):
    pygame.draw.rect(screen,(100,0,200),mouseRect)

def detectCollision(arrayRectStates,mouseRect):
    for i in range(len(arrayRectStates)):
        if arrayRectStates[i].colliderect(mouseRect):
            return i
    return None

def drawTurn(screen,font,player,X,Y):
    if player == 1:
        screen.blit(font.render("El jugador "+str(player)+" hizo la jugada",True, (0,0,0), (255, 255, 255)),(X,Y))
    else:
        screen.blit(font.render("El jugador "+str(player)+" hizo la jugada",True, (0,0,0), (255, 255, 255)),(X,Y-550))

def verifyIfP1AndP2HasPieces(p1Hand,p2Hand):
    if len(p1Hand)<=0:
        return "p1" #p1 wins
    elif len(p2Hand)<=0:
        return "p2"
    return False #both players have pieces to play

def determineIfNeitherUserCanPutApiece(remaining,states):#it is a draw
    if len(remaining)<=0:
        if len(states[len(states)-1][4][0]) == 0 and len(states[len(states)-2][4][0]) == 0:
            return True
    return False

def determineWhoWhonIfDraw(p1Hand,p2Hand):
    p1Sum = 0
    p2Sum = 0
    for i in range(len(p1Hand)):
        p1Sum += p1Hand[i][0] + p1Hand[i][1]
    for i in range(len(p2Hand)):
        p2Sum += p2Hand[i][0] + p2Hand[i][1]
    
    if p1Sum>p2Sum:
        return "p2"
    elif p2Sum>p1Sum:
        return "p1"
    else:
        return "None"

if __name__ == "__main__":
    all_pieces = generateAllPieces()
    # print(all_pieces,len(all_pieces))
    q = 7
    p1_i = generateP1Indices(q,all_pieces)
    p2_i = generateP2Indices(q,all_pieces,p1_i)

    p1 = generateHand(p1_i,all_pieces)
    p2 = generateHand(p2_i,all_pieces)

    print(p1)
    print(p2)

    begins = determineWhoBegins(p1,p2)

    remaining = determineRemainingPieces(p1,p2,all_pieces)
