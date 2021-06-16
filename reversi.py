import random
import numpy as np
import time
import copy


def parseField(fieldInt):
    field = ""
    fieldStr = ""
    for m in range(8):
        for n in fieldInt[m, ]:
            if n == 0:
                field += '⬛'
            elif n == 1:
                field += '🔵'
            elif n == 2:
                field += '⚪'

    fieldStr += '　０１２３４５６７　\n'
    fieldStr += '０{}　\n'.format(field[0:8])
    fieldStr += '１{}　\n'.format(field[8:16])
    fieldStr += '２{}　\n'.format(field[16:24])
    fieldStr += '３{}　\n'.format(field[24:32])
    fieldStr += '４{}　\n'.format(field[32:40])
    fieldStr += '５{}　\n'.format(field[40:48])
    fieldStr += '６{}　\n'.format(field[48:56])
    fieldStr += '７{}　\n'.format(field[56:64])
    fieldStr += '　　　　　　　'
    return fieldStr


def setup():
    print('start playing reversi.')
    fieldInt = np.zeros((8, 8), dtype=np.int8)
    fieldInt[3, 3] = fieldInt[4, 4] = 1
    fieldInt[3, 4] = fieldInt[4, 3] = 2

    return fieldInt


def judge(fieldInt):

    b, w = 0, 0
    winner = 0
    
    for m in range(8):
        for n in fieldInt[m, ]:
            if n == 1:
                b += 1
            elif n == 2:
                w += 1
    
    if b > w:
        winner = 1
    elif b < w:
        winner = 2
    else:
        winner = 0

    return (winner, b, w) 


# int fieldInt, list (int position)
def setStone(fieldInt, position, mine, enemy):
    
    (px, py) = (position[0], position[1])
    fieldInt[px, py] = mine

    dirList = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1, 0), (1, 1)]
    toCount = 0
    for dir in dirList:
        (dx, dy) = (dir[0], dir[1])

        # 範囲外は見ない
        if px + dx < 0 or px + dx >= 8 or py + dy < 0 or py + dy >= 8:
            continue
        
        turnPosition = [px + dx, py + dy]
        tuple = turnOver(fieldInt, turnPosition, dir, mine, enemy)
        fieldInt = tuple[1]
        toCount += tuple[2]
    
    return (fieldInt, toCount)


# position:見ている座標, dir:方角, mine:自分の石のint, enemy:相手の石のint
def settablePosition(fieldInt, position, dir, mine, enemy):

    # 端まで行って空いてなかったらFalse
    for p in position:
        if p < 0 or p >= 8:
            return False

    (px, py) = (position[0], position[1])
    (dx, dy) = (dir[0], dir[1])

    # 自分の石なら置けないのでFalse
    if fieldInt[px, py] == mine:
        return False
    # 敵の石ならもう1つ隣を見る
    elif fieldInt[px, py] == enemy:
        nextPosition = [px + dx, py + dy]
        return settablePosition(fieldInt, nextPosition, dir, mine, enemy)
    # 空いていたら置けるのでTrue
    elif fieldInt[px, py] == 0:
        return position


def find(fieldInt, mine, enemy):
    dirList = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1, 0), (1, 1)]
    myStone = []
    settable = []
    for m in range(8):
        for n in range(8):
            if fieldInt[m, n] == mine:
                myStone.append([m, n])
    print(myStone)

    for posx, posy in myStone:
        for dirx, diry in dirList:

            # 範囲外は見ない
            if posx + dirx < 0 or posx + dirx >= 8 or posy + diry < 0 or posy + diry >= 8:
                continue

            if fieldInt[posx + dirx, posy + diry] == enemy:

                position = [posx + dirx, posy + diry]
                dir = [dirx, diry]

                s = settablePosition(fieldInt, position, dir, mine, enemy)
                if s:
                    settable.append(s)

    return settable


#return -> isTurnable, fieldInt, count
def turnOver(fieldInt, position, dir, mine, enemy):

    # 端まで行って空いてなかったらFalse
    for p in position:
        if p < 0 or p >= 8:
            return (False, fieldInt, 0)

    (px, py) = (position[0], position[1])
    (dx, dy) = (dir[0], dir[1])

    if fieldInt[px, py] == enemy:
        nextPosition = [px + dx, py + dy]
        tuple = turnOver(fieldInt, nextPosition, dir, mine, enemy)

        # Trueが戻ってきたら裏返してTrue
        if tuple[0] == True:
            fieldInt[px, py] = mine
            count = tuple[2] + 1
            return (True, fieldInt, count)
        else:
            return (False, fieldInt, 0)

    # 自分の石が見つかった場合はTrue
    elif fieldInt[px, py] == mine:
        return (True, fieldInt, 0)
    else:
        return (False, fieldInt, 0)


# return -> hand
def randomSet(settable):
    return random.choice(settable)


# return -> hand
def maximumGain(fieldInt, settable, mine, enemy):
    maximum = 0
    toc = 0
    i = 0
    
    for preHand in settable:

        fieldIntTemp = copy.deepcopy(fieldInt)

        preSet = setStone(fieldIntTemp, preHand, mine, enemy)
        if toc < preSet[1]:
            toc = preSet[1]
            maximum = i
        i += 1

    print(fieldInt)

    return settable[maximum]


def main():
    fieldInt = setup()
    fieldStr = parseField(fieldInt)
    print(fieldStr)
    playerTurn = True
    skipped = False
    mine = 1
    enemy = 2
    turn = 0

    autoPlay = True
    enemyHandPattern = 1

    while turn < 60:
        print('Turn ' + str(turn + 1) + '!')
        settable = find(fieldInt, mine, enemy)
        print(settable)

        if settable:

            skipped = False
            
            if playerTurn:
                if autoPlay == True:
                    time.sleep(0.2)
                    hand = randomSet(settable)
                else:
                    handStr = input('Player ' + str(mine) +
                            ', Enter the position in format "x y": ')
                    hand = handStr.split()
                    hand = [int(n) for n in hand]
            else:
                time.sleep(0.2)
                if enemyHandPattern == 0:
                    hand = randomSet(settable)
                elif enemyHandPattern == 1:
                    hand = maximumGain(fieldInt, settable, mine, enemy)

            print(hand)

            if hand in settable:
                setTuple = setStone(fieldInt, hand, mine, enemy)
                fieldInt = setTuple[0]
                fieldStr = parseField(fieldInt)

                cn = ""
                if setTuple[1] >= 2: cn = 's'

                print('Turned ' + str(setTuple[1]) + ' stone' + cn + '!')

                playerTurn = not playerTurn
                mine, enemy = enemy, mine
            else:
                print('You cannot put the stone on (' + handStr + ')!')
                turn -= 1

        else:
            if skipped:
                break

            print('Player ' + str(mine) +
                  '\'s turn is skipped!')
            turn -= 1
            skipped = True
            playerTurn = not playerTurn
            mine, enemy = enemy, mine

        print(fieldStr)
        turn += 1


    print('Game Set!')
    judgeTuple = judge(fieldInt)
    if judgeTuple[0] == 1:
        print('Winner is black! ({} vs {})'.format(judgeTuple[1], judgeTuple[2]))
    elif judgeTuple[0] == 2:
        print('Winner is white! ({} vs {})'.format(judgeTuple[1], judgeTuple[2]))
    else:
        print('Draw! ({} vs {})'.format(judgeTuple[1], judgeTuple[2]))


if __name__ == "__main__":
    main()
