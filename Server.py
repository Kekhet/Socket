import socket
import json


class statVal:
    statID = 0


def add_task(buff2, buff3):
    with open('tasks.txt', 'r') as outfile:
        data = outfile.read()
        tasks = json.loads(data)

    with open('tasks.txt', 'w') as outfile:
        task = {'ID': statVal.statID, 'Title': buff2, 'Priority': buff3}
        tasks['tasks'].append(task)
        outfile.write(json.dumps(tasks))
        statVal.statID += 1
        print("Object added.")


def send_tasks():
    with open('tasks.txt', 'r') as outfile:
        data = outfile.read()
    c.send(data.encode())


def send_chosen_tasks(priority):
    with open('tasks.txt', 'r') as outfile:
        data = outfile.read()
        tasks = json.loads(data)
    tasks_to_send = {'tasks': []}
    for t in tasks['tasks']:
        if t['Priority'] == priority:
            tasks_to_send['tasks'].append(t)
    sends = json.dumps(tasks_to_send)
    c.send(sends.encode())


def remove_task(t_id):
    with open('tasks.txt', 'r') as outfile:
        data = outfile.read()
        tasks = json.loads(data)
    new_tasks = {'tasks': []}
    for t in tasks['tasks']:
        if t["ID"] != int(t_id):
            new_tasks['tasks'].append(t)
    with open('tasks.txt', 'w') as outfile:
        outfile.write(json.dumps(new_tasks))
        print("Object removed.")
        c.send("Object removed.".encode())


def reset_json_file():
    fh = open("tasks.txt", "w")
    string = '{"tasks": []}'
    fh.write(string)
    fh.close()


s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))
s.listen(5)
reset_json_file()
c, addr = s.accept()

while True:
    user_input = c.recv(1024).decode()
    buff1, buff2, buff3 = user_input.split("/")
    if buff1 == "show":
        if buff2 == "":
            send_tasks()
        elif buff2 == "1":
            send_chosen_tasks("1")
        elif buff2 == "2":
            send_chosen_tasks("2")
        elif buff2 == "3":
            send_chosen_tasks("3")
    elif buff1 == "add":
        add_task(buff2, buff3)
    elif buff1 == "remove":
        remove_task(buff2)

