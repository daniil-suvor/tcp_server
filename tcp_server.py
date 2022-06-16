import socket
import re

def correct_data(string):
    if (re.fullmatch("\d{4}\ [0-9a-fA-F]{2}\ \d{2}\:\d{2}\:\d{2}\.\d{3}\ \d{2}\r\n", string)):
        data = re.split('\ |\:|\.|\r\n', string)
        return (data if correct_time(data[2:4]) else False)
    else:
        return False

def correct_time(time):
    if ((0 <= int(time[0]) <= 23) and
        (0 <= int(time[1]) <= 60) and
        (0 <= int(time[1]) <= 60)):
        return True
    else:
        return False

SERVER_ADDRESS = ('', 51413)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(1)
print("server is running, please, press ctrl+c to stop")

while True:
    try:
        connection, address = server_socket.accept()
        data = str(connection.recv(25).decode("UTF-8"))
    except KeyboardInterrupt:
        print(" server stopped")
        break
    except Exception:
        connection.send(b"Error!\n")
        data = ""
    data = correct_data(data)
    if (data):
        data[5] = int(data[5])//100
        answer = "спортсмен, нагрудный номер {d[0]} прошёл отсечку {d[1]} в {d[2]}:{d[3]}:{d[4]}.{d[5]}\r\n".format(d = data)
        with open("data.txt", "a") as file:
            file.write(answer)
        if (data[6] == "00"):
            connection.send(bytes(answer, encoding = "UTF-8"))
    else:
        connection.send(b"Error format!\n")
    connection.close()
server_socket.close()
