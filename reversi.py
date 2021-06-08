import random
import numpy as np
import time


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


# int fieldInt, list (int position)
def setStone(fieldInt, position, mine, enemy):
    
    (px, py) = (position[0], position[1])
    fieldInt[px, py] = mine

    dirList = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
               (0, 1), (1, -1), (1, 0), (1, 1)]
    for dir in dirList:
        (dx, dy) = (dir[0], dir[1])

        # 範囲外は見ない
        if px + dx < 0 or px + dx >= 8 or py + dy < 0 or py + dy >= 8:
            continue
        
        turnPosition = [px + dx, py + dy]
        tuple = turnOver(fieldInt, turnPosition, dir, mine, enemy)
        fieldInt = tuple[1]
    
    return fieldInt


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


def turnOver(fieldInt, position, dir, mine, enemy):

    # 端まで行って空いてなかったらFalse
    for p in position:
        if p < 0 or p >= 8:
            return (False, fieldInt)

    (px, py) = (position[0], position[1])
    (dx, dy) = (dir[0], dir[1])

    if fieldInt[px, py] == enemy:
        nextPosition = [px + dx, py + dy]
        tuple = turnOver(fieldInt, nextPosition, dir, mine, enemy)

        # Trueが戻ってきたら裏返してTrue
        if tuple[0] == True:
            fieldInt[px, py] = mine
            return (True, fieldInt)
        else:
            return (False, fieldInt)

    # 自分の石が見つかった場合はTrue
    elif fieldInt[px, py] == mine:
        return (True, fieldInt)
    else:
        return (False, fieldInt)


def main():
    fieldInt = setup()
    fieldStr = parseField(fieldInt)
    print(fieldStr)
    playerTurn = True
    skipped = False
    mine = 1
    enemy = 2
    turn = 0

    while turn < 60:
        print('Turn ' + str(turn + 1) + '!')
        settable = find(fieldInt, mine, enemy)
        print(settable)

        if settable:

            skipped = False
            
            if playerTurn:
                handStr = input('Player ' + str(mine) +
                            ', Enter the position in format "x y": ')
                hand = handStr.split()
            else:
                time.sleep(1)
                hand = random.choice(settable)

            hand = [int(n) for n in hand]
            print(hand)

            if hand in settable:
                fieldInt = setStone(fieldInt, hand, mine, enemy)
                fieldStr = parseField(fieldInt)
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


if __name__ == "__main__":
    main()
