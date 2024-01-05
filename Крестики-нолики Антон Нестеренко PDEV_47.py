# Крестики-нолики Антон Нестеренко PDEV-47

pole = [1, 2, 3,  # Ячейки игрового поля
        4, 5, 6,
        7, 8, 9]

win_combo = [[0, 1, 2],  # Комбинации ячеек для победы в игре
             [3, 4, 5],
             [6, 7, 8],
             [0, 3, 6],
             [1, 4, 7],
             [2, 5, 8],
             [0, 4, 8],
             [2, 4, 6]]


def pole_vision():  # Функция для отрисовки игровой карты
    print('|  ', pole[0], '  |  ', pole[1], '  |  ', pole[2], '  |')
    print('_________________________')
    print('|  ', pole[3], '  |  ', pole[4], '  |  ', pole[5], '  |')
    print('_________________________')
    print('|  ', pole[6], '  |  ', pole[7], '  |  ', pole[8], '  |')


def win_game_result():  # Условия победы одного из игрока
    win = False

    for i in win_combo:
        if pole[i[0]] == pole[i[1]] and pole[i[1]] == pole[i[2]]:
            win = pole[i[0]]

    return win


def step_game(ind, symbol):  # Функция для исполнения шагов игры и замены символов игрового поля
    if pole[ind-1] in ('X', 'O'):
        return False
    pole[ind-1] = symbol
    return True


def start_game():  # Функция с основными циклами игры, условиями победы, ничьи и досрочного выхода из игры
    pole_vision()

    player = 'X'
    step = 1

    while step < 10 and (win_game_result() is False):
        ind = input('Ход ' + player + '.Куда пойдете (для выхода из игры - 0): ')
        while ind not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            print('Не верное значение, повторите попытку (нужно указать значение от 1 до 9)')
            ind = input('Ход ' + player + '.Куда пойдете (для выхода из игры - 0): ')

        if ind == '0':
            break

        if step_game(int(ind), player):
            if player == 'X':
                player = 'O'
            else:
                player = 'X'

            step += 1
            pole_vision()

        else:
            print('Эта ячейка уже занята, выберите другую!')

    if step == 10 and win_game_result() is False:
        print('Игра окончена! Ничья!')

    elif win_game_result() is False:
        print('Игра окончена досрочно!')

    else:
        print('Игра окончена! Выиграли ' + str(win_game_result() + '!'))


print('Добро пожаловать в Крестики-нолики!')
start_game()
