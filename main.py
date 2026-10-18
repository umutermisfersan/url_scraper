import http.client
import json
import queue
import threading
import time
import sys
import webbrowser
from pathlib import Path
from string import whitespace
from sys import path
from tabnanny import check
from queue import Queue, Empty
import threading

from colorama import Fore, Style, init

init(autoreset=True)

logo = r"""
 _     ____  _       ____  ____  ____  ____  ____  _____ ____ 
/ \ /\/  __\/ \     / ___\/   _\/  __\/  _ \/  __\/  __//  __\
| | |||  \/|| |     |    \|  /  |  \/|| / \||  \/||  \  |  \/|
| \_/||    /| |_/\  \___ ||  \__|    /| |-|||  __/|  /_ |    /
\____/\_/\_\\____/  \____/\____/\_/\_\\_/ \|\_/   \____\\_/\_\
"""

print(Fore.CYAN + Style.BRIGHT + logo)
print(Fore.GREEN + Style.BRIGHT + "       Made by Umut!")
print(Fore.YELLOW + "       [ Please Wait... ]")


file_input = input(Fore.LIGHTRED_EX+"\nKeyword file path (without extension)" + Fore.WHITE + " : ")
file_input_splitted = file_input.split(".txt")[0]
check_path = Path(file_input_splitted + ".txt")

print("\nFile name : ", check_path)

github_url = "https://github.com/umutermisfersan"
api_key = 'HERE' # Api key here / Api key buraya giriniz.. via serper.dev
threads = []
keywords = ""
kw_list = ""
payload = ""
kw_queue = []
url_count = 0
url_lock = threading.Lock()

def check_amount():
    global amount

    try:
        amount = int(amount)
    except ValueError:
        print(Fore.WHITE + "\nAmount must contain numbers only! | Sadece numara/sayı giriniz..")
        exit()





def scraper(kw, amount):
    global url_count

    conn = http.client.HTTPSConnection("google.serper.dev")

    payload = json.dumps({
        "q": kw,
        "gl": country_input,
        "num": 10
    })

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    conn.close()

    with open("links.txt", "a", encoding="utf-8") as f:
        for item in data.get("organic", []):
            url = item.get("link")
            if not url:
                continue

            with url_lock:
                if url_count >= amount:
                    return

                f.write(url + "\n")
                url_count += 1

            print(f"\n[{url_count}/{amount}] {url}")





def task():
    kw_list = keywords.split("\n")
    q = Queue()

    for kw in kw_list:
        q.put(kw)

    def worker():
        while True:
            try:
                kw = q.get_nowait()
            except Empty:
                break

            try:
                scraper(kw, amount)
            finally:
                q.task_done()

    threads = []

    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def init_keywords():
        try:
            with open(check_path, "r") as f:
                global keywords
                keywords = f.read()
                task()
                # print("\n" + keywords)
        except FileNotFoundError:
            print("\nDosya bulunamadı")
            sys.exit()




if (file_input.isalnum() == False):
    print("\nGeçersiz ifade")
    sys.exit()


country_input = input(Fore.LIGHTRED_EX + "\nCountry (ISO Format)" + Fore.WHITE + " : ")
print("\nCountry : ", country_input)

amount = input(Fore.LIGHTRED_EX+"\nAmount (numbers only)" + Fore.WHITE + " : ")
check_amount()
print("\nAmount : ", amount)

if (file_input.isalnum()):
    if (country_input.isalpha() == False):
        print("\nGeçersiz ifade")
        sys.exit()

if (file_input.isalnum()):
    if (country_input.isalpha()):
        init_keywords()


print(f"\nAmount : {url_count} | saved to links.txt file" + Fore.CYAN + " Made By Umut <3")
print(f"Github : " + f"{github_url} " + Fore.CYAN + "Support me please :)")
print("Thanks for using my program :) <3" + Fore.CYAN + " URL SCRAPER VIA SERPER.DEV API")
time.sleep(3)
webbrowser.open(github_url)
