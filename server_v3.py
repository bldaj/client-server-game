import socket
import random

archive = []
order = random.choice([1, 2])
game_points = {'First player': 0, 'Second player': 0}
foul = {'First player': 0, 'Second player': 0}
message = 'Your turn'
error = ['This word has been', 'Your word not composed from symbol previous word']
flag = False


def exchange_data(order, message):
    if order == 1:
        client1.send(message.encode())
        data = client1.recv(1024).decode()

    elif order == 2:
        client2.send(message.encode())
        data = client2.recv(1024).decode()

    return data


def send_answer(order, data):
    if order == 1:
        client2.send(data.encode())
    elif order == 2:
        client1.send(data.encode())


def check_similar_sym(word, archive):
    previous_word = list(archive[-1])
    curr_word = list(word)
    previous_word.sort()
    curr_word.sort()
    res = len(previous_word) - len(curr_word)

    for sym in curr_word:
        if sym in previous_word:
            previous_word.remove(sym)
            if len(previous_word) == res:
                return 'Ok'


def toggle_order(order):
    if order == 1:
        order = 2

    elif order == 2:
        order = 1

    return order


def counter_point(order, game_points):
    if order == 1:
        game_points['First player'] += 1
    elif order == 2:
        game_points['Second player'] += 1

    return game_points


def check_winner(game_points):
    winner = ["You're the winner!", "Player 1 wins!", "Player 2 wins!", "Drawn game"]

    if game_points['First player'] > game_points['Second player']:
        client1.send(winner[0].encode())
        client2.send(winner[1].encode())

    elif game_points['First player'] < game_points['Second player']:
        client1.send(winner[2].encode())
        client2.send(winner[0].encode())

    elif game_points['First player'] == game_points['Second player']:
        client1.send(winner[3].encode())
        client2.send(winner[3].encode())


def count_foul(order, foul):
    if order == 1:
       foul['First player'] += 1
    elif order == 2:
        foul['Second player'] += 1

    return foul


def check_foul(foul):
    message = ['You have lost the game!', 'Player 1 has lost the game', 'Player 2 has lost the game']

    if foul['First player'] == 3:
        client1.send(message[0].encode())
        client2.send(message[1].encode())
        return 'Game over'

    elif foul['Second player'] == 3:
        client2.send(message[0].encode())
        client1.send(message[2].encode())
        return 'Game over'


def close_game():
    client1.close()
    client2.close()
    sock.close()


sock = socket.socket()

sock.bind(('127.0.0.1', 9090))
sock.listen(2)

client1, addr1 = sock.accept()
client2, addr2 = sock.accept()

print('Player_1 has connected', addr1)
print('Player_2 has connected', addr2)

while True:
    data = exchange_data(order, message)

    if data in '-ex':
        check_winner(game_points)
        close_game()
        break

    elif len(archive) == 0:
        archive.append(data)
        send_answer(order, data)
        order = toggle_order(order)

    elif data in archive:
        while data in archive:
            foul = count_foul(order, foul)
            if check_foul(foul) == 'Game over':
                close_game()
                flag = True
                break
            data = exchange_data(order, error[0])

        if flag:
            break

        archive.append(data)
        send_answer(order, data)
        game_points = counter_point(order, game_points)
        order = toggle_order(order)

    else:
        while check_similar_sym(data, archive) != 'Ok':
            foul = count_foul(order, foul)
            if check_foul(foul) == 'Game over':
                close_game()
                flag = True
                break
            data = exchange_data(order, error[1])

        if flag:
            break

        archive.append(data)
        send_answer(order, data)
        game_points = counter_point(order, game_points)
        order = toggle_order(order)
