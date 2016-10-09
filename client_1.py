import socket

server_data = ''
office_message = ['Your turn', 'This word has been']
over_game = ['You have lost the game!', 'Player 1 has lost the game', 'Player 2 has lost the game']
winner = ["You're the winner!", "Player 1 wins!", "Player 2 wins!", "Drawn game"]

sock = socket.socket()

sock.connect(('127.0.0.1', 9090))

while True:
    server_data = sock.recv(1024).decode()

    if not server_data:
        print('Game has finished')
        break

    elif server_data in office_message:
        print(server_data)
        sock.send(input('Enter your word: ').encode())

    elif server_data in over_game:
        print(server_data)

    elif server_data in winner:
        print(server_data)

    else:
        print('The word from another player: ' + server_data)

sock.close()
