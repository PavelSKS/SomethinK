# это вспомогательный файл, он не имеет отношение к проекту и нужен только для того,
# чтобы удобно редактировать команды, которые уже находятся в бд

import sqlite3
import sys

con = sqlite3.connect("./commands_and_costants/commands/command_db.db")
cur = con.cursor()

command_name = "twitch_youtube_connect"
command = ""

command += cur.execute(f"""SELECT command_file FROM command WHERE command_name='{command_name}'""").fetchone()[0]

with open("command_to_add.py", "w", encoding="utf-8") as f:
    f.write(command)

sys.exit()
