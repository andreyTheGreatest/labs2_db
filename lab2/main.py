import redis
import threading
from view import View
from models.worker import Worker
import random as r
import string

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(r.choice(letters) for i in range(stringLength))

def run_simulation():
    menu = View(conn)
    for _ in range(0, 3):
        new_working_thread = threading.Thread(target=Worker(conn).clearing_queue)
        new_working_thread.daemon = True
        new_working_thread.start()
    
    for _ in range(0, r.randint(20, 50)):
        usr = randomString()
        rec = randomString()
        conn.publish('online', usr)
        for _ in range(0, r.randint(1, 10)):
            menu.create_new_message(usr, rec, randomString())
        conn.publish('offline', usr)

if __name__ == "__main__":
    conn = redis.StrictRedis(host="localhost", port=6379, charset="utf-8", decode_responses=True)
    if not conn.sismember('admins', 'andrii'):
        conn.sadd('admins', 'andrii')

    while True:
        n = input('1 - run simulation\n2 - go to normal usage\n\033[94m=>\033[0m')
        if (n == '1'):
            run_simulation()
        elif (n == '2'):
            menu = View(conn)
            username = input('Enter username (\'q\' to close): ')
            menu.set_username(username)
            worker_with_queue = Worker(conn)
            new_working_thread = threading.Thread(target=worker_with_queue.clearing_queue)
            new_working_thread.daemon = True
            new_working_thread.start()
            if (conn.sismember('admins', username)):
                menu.adminUI()
            elif (conn.sismember('users', username)):
                conn.publish('online', username)
                menu.userUI()
                conn.publish('offline', username)
            elif (username == 'q'):
                break
            else:
                conn.sadd('users', username)

