import os
import shutil
import sqlite3
import zipfile


def open_command(command_list: list, pref):
    PREFIX = pref
    connect = sqlite3.connect('../../../commands_and_costants/commands/command_db.db')
    cursor = connect.cursor()

    command_create_file = ''
    help_command_create = ''
    help_moder_command_create = ''
    help_admin_command_create = ''

    all_help = ""
    moder_help = ""
    admin_help = ""

    command_create_file += open('../../../commands_and_costants/constants/main_bot_function.py').read() + '\n'
    command_create_file += '\n\n'

    all_user_command = []
    moder_user_command = []
    admin_user_command = []

    has_help = False
    has_moder_help = False
    has_admin_help = False

    for command in command_list:
        command_permission = command.split(':')
        print(command_permission[0])

        if command_permission[1] == '0':
            all_user_command.append(command_permission[0])
        elif command_permission[1] == '1':
            moder_user_command.append(command_permission[0])
        else:
            admin_user_command.append(command_permission[0])

        if (command_permission[0] != "help") and (command_permission[0] != "help_moder") and (
                command_permission[0] != "help_admin"):
            if int(command_permission[1]) == 0:
                command_create_file += cursor.execute(
                    f"""SELECT command_file FROM command WHERE command_name='{command_permission[0]}'""").fetchone()[0]

                command_create_file += '\n\n\n'
            elif int(command_permission[1]) == 1:
                command_create_file += open(
                    '../../../commands_and_costants/constants/has_permition_moder.py').read() + '\n'
                command_create_file += cursor.execute(
                    f"""SELECT command_file FROM command WHERE command_name='{command_permission[0]}'""").fetchone()[0]

                command_create_file += '\n\n\n'
            else:
                command_create_file += open(
                    '../../../commands_and_costants/constants/has_permition_admin.py').read() + '\n'
                command_create_file += cursor.execute(
                    f"""SELECT command_file FROM command WHERE command_name='{command_permission[0]}'""").fetchone()[0]

                command_create_file += '\n\n\n'
        else:
            if command_permission[0] == "help":
                has_help = True
            elif command_permission[0] == "help_moder":
                has_moder_help = True
            elif command_permission[0] == "help_admin":
                has_admin_help = True

    # command_create_file += '\n\n'

    print(all_user_command,
          moder_user_command,
          admin_user_command)

    command_value = {"help_moder": ["", "Команды, доступные только модераторам"],
                     "help_admin": ["", "Команды, доступные только админам"],
                     "report": ["*name* *cause*", "Пожаловаться на игрока всемогущим модераторам"],
                     "bag": ["*bag*", "Отправить отчет о ошибке в работе бота"],
                     # "event_commands": [],
                     "author": ["", "Вк недоразработчиков сайта"],
                     "color": ["*R* *G* *B*", "Установить себе цвет в чате"],
                     "clear": ["*количество сообщений*", "Удалить n сообщений"],
                     "kick": ["*name*", "Проверить ссылку приглашения на работоспособность"],
                     "ban": ["*name*", "Забанить участника"],
                     "unban": ["*name*", "Разбанить участника"],
                     "mute": ["*name*", "Замутить участника"],
                     "unmute": ["*name*", "Размутить участника"],
                     "nick": ["*name* *nick*", "Поменять игроку имя"],
                     "moder": ["*name*", "Выдать модератора"],
                     "unmoder": ["*name*", "Удалить модератора"],
                     "__bot__": ["9400 *message*", "писать от имени бота"],
                     "help": ["", "Список команд"],
                     "event_commands": ["", "1"],
                     "find": ["", "Поиск по истории"],
                     "twitch_youtube_connect": ["", "1"]
                     }

    for help_command in command_list:
        help_command = help_command.split(":")
        if help_command[0] == "help":

            help_command_create += cursor.execute(
                f"""SELECT command_file FROM command WHERE command_name='{help_command[0]}'""").fetchone()[0]

            print(all_user_command)
            for help_a in all_user_command:
                print("help_a", "=", help_a)
                all_help += f"emb.add_field(name=\"{PREFIX}{help_a} {command_value[help_a][0]}\", value=\"{command_value[help_a][1]}\")" + "\n    "
            print(all_help)
            if "event_commands:0" in command_list:
                all_help += f"emb.add_field(name=\"{PREFIX}join\", value=\"Список/присоединиться к ивенту\")" + "\n    "
                all_help += f"emb.add_field(name=\"{PREFIX}leave\", value=\"Список/покинуть к ивент\")" + "\n    "

            if not all_user_command:
                all_help += "emb.add_field(name=\"Нет доступных команд\"," \
                            " value=\"В данном боте нет команд, доступных всем\")"

            help_command_create = help_command_create.replace("__help_input_command__", all_help)

            print(help_command_create)

            command_create_file += help_command_create
            command_create_file += '\n\n\n'

        elif help_command[0] == "help_moder":
            help_moder_command_create += cursor.execute(
                f"""SELECT command_file FROM command WHERE command_name='{help_command[0]}'""").fetchone()[0]

            print(moder_user_command)
            for help_a in moder_user_command:
                print("help_m", "=", help_a)
                moder_help += f"emb.add_field(name=\"{PREFIX}{help_a} {command_value[help_a][0]}\", value=\"{command_value[help_a][1]}\")" + "\n    "
            print(moder_help)
            # if has_admin_help:
            #     moder_help += \
            #         f"emb.add_field(name=\"{PREFIX}help_admin\", value=\"Команды, доступные только модераторам\")" + "\n    "

            if not moder_user_command:
                moder_help += "emb.add_field(name=\"Нет доступных команд\"," \
                              " value=\"В данном боте нет команд, доступных модераторам\")"

            help_moder_command_create = help_moder_command_create.replace("__help_moder_input_command__", moder_help)

            print(help_moder_command_create)

            command_create_file += help_moder_command_create
            command_create_file += '\n\n\n'
        elif help_command[0] == "help_admin":
            help_admin_command_create += cursor.execute(
                f"""SELECT command_file FROM command WHERE command_name='{help_command[0]}'""").fetchone()[0]

            print(admin_user_command)
            for help_a in admin_user_command:
                print("help_m", "=", help_a)
                admin_help += f"emb.add_field(name=\"{PREFIX}{help_a} {command_value[help_a][0]}\", value=\"{command_value[help_a][1]}\")" + "\n    "
            print(admin_help)

            if "event_commands:0" in command_list:
                all_help += f"emb.add_field(name=\"{PREFIX}create_event '*имя*' '*Название*' '*Условие*' " \
                            f"'*Приз*' '*Дата окончания*'\", value=\"создать ивент\")" + "\n    "
                all_help += f"emb.add_field(name=\"{PREFIX}remove_event *name*\", value=\"удалить ивент\")" + "\n    "

            if not admin_user_command:
                admin_help += "emb.add_field(name=\"Нет доступных команд\"," \
                              " value=\"В данном боте нет команд, доступных админам\")"

            help_admin_command_create = help_admin_command_create.replace("__help_admin_input_command__", admin_help)

            print(help_admin_command_create)

            command_create_file += help_admin_command_create
            command_create_file += '\n\n\n'

    command_create_file += open('../../../commands_and_costants/constants/end_bot_function.py').read() + '\n'

    # with open('test.txt', "w") as file_out:
    #     file_out.write(command_create_file)

    # return file_out

    return command_create_file


def create(user, bot_name, token, prefix, command_input_list: list, white_list_of_command: list,
           history_of_command_id: int,
           report_command_id: int, moderator_role_id: int):
    # os.rmdir(f'user_bot_project/pavel/{bot_name}')
    os.chdir('user_bot_project')

    os.makedirs(f'{user}/{bot_name}')

    os.chdir('..')

    shutil.copyfile("commands_and_costants/constants/requirements.txt",
                    f"user_bot_project/{user}/{bot_name}/requirements.txt")
    shutil.copyfile("commands_and_costants/constants/banword.txt",
                    f"user_bot_project/{user}/{bot_name}/banword.txt")
    shutil.copyfile("commands_and_costants/constants/command_message.py",
                    f"user_bot_project/{user}/{bot_name}/command_message.py")
    shutil.copyfile("commands_and_costants/constants/constants.py",
                    f"user_bot_project/{user}/{bot_name}/constants.py")
    shutil.copyfile("commands_and_costants/constants/token.txt",
                    f"user_bot_project/{user}/{bot_name}/token.txt")
    shutil.copyfile("commands_and_costants/constants/Procfile",
                    f"user_bot_project/{user}/{bot_name}/Procfile")
    shutil.copyfile("commands_and_costants/constants/data_base.db",
                    f"user_bot_project/{user}/{bot_name}/data_base.db")

    os.chdir(f'user_bot_project/{user}/{bot_name}')

    # worker: python bot.py

    with open('constants.py', encoding="utf-8") as file_in:
        constant_text = file_in.read()

    constant_text = constant_text.replace("__list_of_channel__", f"{white_list_of_command}")
    constant_text = constant_text.replace("__history_id_channel__", f"{history_of_command_id}")
    constant_text = constant_text.replace("__report_id_channel__", f"{report_command_id}")
    constant_text = constant_text.replace("__moderator_id__", f"{moderator_role_id}")
    constant_text = constant_text.replace("__predix__", f"{prefix}")

    with open("constants.py", "w", encoding="utf-8") as file_out:
        file_out.write(constant_text)

    with open('token.txt', encoding="utf-8") as file_in:
        token_text = file_in.read()

    token_text = token_text.replace("", f"{token}")

    with open("token.txt", "w", encoding="utf-8") as file_out:
        file_out.write(token_text)

    with open('Procfile', encoding="utf-8") as file_in:
        procfile_text = file_in.read()

    procfile_text = procfile_text.replace("bot.py", f"{bot_name}.py")

    with open("Procfile", "w", encoding="utf-8") as file_out:
        file_out.write(procfile_text)

    with open(f'{bot_name}.py', 'w', encoding="utf-8") as bot_file:
        bot_file.write(open_command(command_input_list, prefix))

    # shutil.make_archive(f'../{bot_name}', 'zip', f'../{bot_name}')
    os.chdir("..")
    print(os.getcwd())
    shutil.make_archive(f"{bot_name}", "zip", f"{bot_name}")


# open_command(['ban:2', 'unban:1'])
# create('vasyapupkin@gmail.com', 'abc', 'OTY0Mzg4ODc1MDg0NjU2NjQw.Ylj7IQ.it-w_17RWXIXZuFbNER6lfxWsBQ', '!',
#        ["help_moder:1", "help_admin:2", "report:0", "bag:0", "author:0", "color:0", "clear:1", "kick:1", "ban:1",
#         "unban:1", "mute:1", "unmute:1", "nick:1", "moder:2", "unmoder:2", "__bot__:2", "help:0", "event_commands:0"],
#        [0], 964392206146359338,
#        964392231505129523, 964392376011468921)

a = ["help_moder:1", "help_admin2", "report:0", "bag:0", "author:0", "color:0", "clear:1", "kick:1", "ban:1",
     "unban:1", "mute:1", "unmute:1", "nick:1", "moder:2", "unmoder:2", "__bot__:2", "help:0", "event_commands:0",
     "twitch_youtube_connect:0"]



# ['ban:2', 'unban:2', 'kick:2', 'event_commands:0', 'color:0', 'help:0', 'clear:0', 'help_moder:0',
#         'help_admin:2']
