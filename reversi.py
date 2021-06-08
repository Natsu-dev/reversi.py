import random


def parseField(fieldInt):
    field = ""
    fieldStr = ""
    for n in fieldInt:
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
    fieldInt = [0] * 64
    fieldInt[27] = 1
    fieldInt[28] = 2
    fieldInt[36] = 1
    fieldInt[35] = 2

    return fieldInt

# int fieldInt, list (int position)


def setStone(fieldInt, position, mine, enemy):
    fieldInt[position] = mine
    dirList = [-9, -8, -7, -1, 1, 7, 8, 9]
    for dir in dirList:
        tuple = turnOver(fieldInt, position + dir, dir, mine, enemy)
        fieldInt = tuple[1]
    return fieldInt


# position:見ている座標, dir:方角, mine:自分の石のint, enemy:相手の石のint
def settablePosition(fieldInt, position, dir, mine, enemy):

    # 端まで行って空いてなかったらFalse
    if position < 0 | position >= 63:
        return -1

    # 自分の石なら置けないのでFalse
    if fieldInt[position] == mine:
        return -1
    # 敵の石ならもう1つ隣を見る
    elif fieldInt[position] == enemy:
        return settablePosition(fieldInt, position + dir, dir, mine, enemy)
    # 空いていたら置けるのでTrue
    elif fieldInt[position] == 0:
        return position


def find(fieldInt, mine, enemy):
    dirList = [-9, -8, -7, -1, 1, 7, 8, 9]
    myStone = []
    settable = []
    for p in range(64):
        if fieldInt[p] == mine:
            myStone.append(p)
    print(myStone)

    for p in myStone:
        for dir in dirList:

            if fieldInt[p + dir] == enemy:
                s = settablePosition(fieldInt, p + dir, dir, mine, enemy)
                if s >= 0:
                    settable.append(s)

    return settable


def turnOver(fieldInt, p, dir, mine, enemy):
    if fieldInt[p] == enemy:

        tuple = turnOver(fieldInt, p + dir, dir, mine, enemy)

        # Trueが戻ってきたら裏返してTrue
        if tuple[0] == True:
            fieldInt[p] = mine
            return (True, fieldInt)
        else:
            return (False, fieldInt)

    # 自分の石が見つかった場合はTrue
    elif fieldInt[p] == mine:
        return (True, fieldInt)
    else:
        return (False, fieldInt)


def main():
    fieldInt = setup()
    fieldStr = parseField(fieldInt)
    print(fieldStr)
    playerTurn = True
    mine = 1
    enemy = 2

    for turn in range(60):
        settable = find(fieldInt, mine, enemy)
        print(settable)

        if settable:
            handStr = input('Player ' + str(mine) +
                        ', Enter the position in format "x y": ')

            hand = handStr.split()
            hand = [int(n) for n in hand]
            handPos = hand[0] + 8 * hand[1]
            print(hand)

            if handPos in settable:
                fieldInt = setStone(fieldInt, handPos, mine, enemy)
                fieldStr = parseField(fieldInt)
                playerTurn = not playerTurn
                mine, enemy = enemy, mine
            else:
                print('You cannot put the stone on (' + handStr + ')!')
                turn -= 1

        else:
            print('Player ' + str(mine) +
                        '\'s turn is skipped!')
            turn -= 1
            playerTurn = not playerTurn
            mine, enemy = enemy, mine

        print(fieldStr)


if __name__ == "__main__":
    main()
