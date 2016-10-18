import socket
import random

wordlist = []
player_priority = random.choice([1, 2])
game_points = {'First player': 0, 'Second player': 0}
number_of_fouls = {'First player': 0, 'Second player': 0}
message = 'Your turn'
error_message = ['This word has been', 'Your word not composed from symbol of previous word']
flag = False


def exchange_data(player_priority, message):
    if player_priority == 1:
        client1.send(message.encode())
        player_word = client1.recv(1024).decode()

    elif player_priority == 2:
        client2.send(message.encode())
        player_word = client2.recv(1024).decode()

    return player_word


def send_answer_player(player_priority, player_word):
    if player_priority == 1:
        client2.send(player_word.encode())
    elif player_priority == 2:
        client1.send(player_word.encode())


def check_similar_sym(word, wordlist):
    previous_word = list(wordlist[-1])
    current_word = list(word)
    previous_word.sort()
    current_word.sort()
    res = len(previous_word) - len(current_word)

    for sym in current_word:
        if sym in previous_word:
            previous_word.remove(sym)
            if len(previous_word) == res:
                return 'Ok'


def toggle_player_priority(player_priority):
    if player_priority == 1:
        player_priority = 2
    elif player_priority == 2:
        player_priority = 1

    return player_priority


def counter_game_points(player_priority, game_points):
    if player_priority == 1:
        game_points['First player'] += 1
    elif player_priority == 2:
        game_points['Second player'] += 1

    return game_points


def determine_winner(game_points):
    message = ["You're the winner!", "Player 1 wins!", "Player 2 wins!", "Drawn game"]

    if game_points['First player'] > game_points['Second player']:
        client1.send(message[0].encode())
        client2.send(message[1].encode())

    elif game_points['First player'] < game_points['Second player']:
        client1.send(message[2].encode())
        client2.send(message[0].encode())

    elif game_points['First player'] == game_points['Second player']:
        client1.send(message[3].encode())
        client2.send(message[3].encode())


def counter_fouls(player_priority, number_of_fouls):
    if player_priority == 1:
        number_of_fouls['First player'] += 1
    elif player_priority == 2:
        number_of_fouls['Second player'] += 1

    return number_of_fouls


def is_player_lose_game(number_of_fouls):
    message = ['You have lost the game!', 'Player 1 has lost the game', 'Player 2 has lost the game']

    if number_of_fouls['First player'] == 3:
        client1.send(message[0].encode())
        client2.send(message[1].encode())
        return 'Game over'

    elif number_of_fouls['Second player'] == 3:
        client2.send(message[0].encode())
        client1.send(message[2].encode())
        return 'Game over'


def is_empty_wordlist(wordlist):
    if len(wordlist) == 0:
        return True
    else:
        return False


def turn_handler(wordlist, player_priority, player_word):
    wordlist.append(player_word)
    send_answer_player(player_priority, player_word)
    player_priority = toggle_player_priority(player_priority)

    return wordlist, player_priority


def close_game():
    client1.close()
    client2.close()
    sock.close()


sock = socket.socket()

sock.bind(('127.0.0.1', 9090))
sock.listen(2)

client1, addr1 = sock.accept()
client2, addr2 = sock.accept()

print('Player 1 has connected', addr1)
print('Player 2 has connected', addr2)

while True:
    player_word = exchange_data(player_priority, message)

    if player_word in '-ex':
        determine_winner(game_points)
        close_game()
        break

    elif is_empty_wordlist(wordlist):
        wordlist, player_priority = turn_handler(wordlist, player_priority, player_word)

    elif player_word in wordlist:
        while player_word in wordlist:
            number_of_fouls = counter_fouls(player_priority, number_of_fouls)
            if is_player_lose_game(number_of_fouls) == 'Game over':
                close_game()
                flag = True
                break
            player_word = exchange_data(player_priority, error_message[0])

        if flag:
            break

        wordlist, player_priority = turn_handler(wordlist, player_priority, player_word)
        game_points = counter_game_points(player_priority, game_points)

    else:
        while check_similar_sym(player_word, wordlist) != 'Ok':
            number_of_fouls = counter_fouls(player_priority, number_of_fouls)
            if is_player_lose_game(number_of_fouls) == 'Game over':
                close_game()
                flag = True
                break
            player_word = exchange_data(player_priority, error_message[1])

        if flag:
            break

        wordlist, player_priority = turn_handler(wordlist, player_priority, player_word)
        game_points = counter_game_points(player_priority, game_points)
