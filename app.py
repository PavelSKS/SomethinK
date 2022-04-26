from flask import Flask, render_template, url_for, request, make_response
from flask import Flask, render_template

from create_bot_file import create
from data import db_session
from flask import redirect
from forms.user import RegisterForm, LoginForm, CreateForm
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
host = '127.0.0.1'
port = 8080

have_u_logged_in = 0
name_user = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def check_for_only_eng(text):
    only_eng = 'qwertyuiopasdfghjklzxcvbnm_QWERTYUIOPASDFGHJKLZXCVBNM'
    for i in text:
        if i not in only_eng:
            return False
    return True


def check_for_only_prefix(text):
    only_prefix = "<>,.?/\"':;}]{[|\+=_-)(*&^%$#@!"
    for i in text:
        if i not in only_prefix:
            return False
    return True


@app.route('/')
def to_main():
    return redirect('/home')


@app.route('/home')
def index():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(render_template("main.html", cond=have_u_logged_in, name=name_user))
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(render_template("main.html", cond=have_u_logged_in, name=name_user))
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365)
    if not (visits_count):
        res = make_response(render_template("main.html", cond=have_u_logged_in, name=name_user))
        res.set_cookie("is_authed", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)

    return render_template("main.html", cond=have_u_logged_in, name=name_user)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + "-" + str(id)


@app.route('/dino')
def dino():
    return render_template("dinosor.html")


@app.route('/download')
def download():
    return render_template('download_ws.html')


@app.route('/create', methods=['GET', 'POST'])
def create_url():
    create_form = CreateForm()
    if create_form.validate_on_submit():
        db_sess = db_session.create_session()
        print('начало сздания')
        command_spi = []



        if create_form.help_cb.data:
            command_spi.append(f'help:{create_form.help_rb.data}')

        if create_form.help_modder_cb.data:
            command_spi.append(f'help_moder:{create_form.help_modder_rb.data}')

        if create_form.help_admin_cb.data:
            command_spi.append(f'help_admin:{create_form.help_admin_rb.data}')

        if create_form.report_cb.data:
            command_spi.append(f'report:{create_form.report_rb.data}')

        if create_form.bug_cb.data:
            command_spi.append(f'bag:{create_form.bug_rb.data}')

        if create_form.author_cb.data:
            command_spi.append(f'author:{create_form.author_rb.data}')

        if create_form.color_cb.data:
            command_spi.append(f'color:{create_form.color_rb.data}')

        if create_form.clear_cb.data:
            command_spi.append(f'clear:{create_form.clear_rb.data}')

        if create_form.kick_cb.data:
            command_spi.append(f'kick:{create_form.kick_rb.data}')

        if create_form.ban_cb.data:
            command_spi.append(f'ban:{create_form.ban_rb.data}')

        if create_form.unban_cb.data:
            command_spi.append(f'unban:{create_form.unban_rb.data}')

        if create_form.mute_cb.data:
            command_spi.append(f'mute:{create_form.mute_rb.data}')

        if create_form.unmute_cb.data:
            command_spi.append(f'unmute:{create_form.unmute_rb.data}')

        if create_form.nick_cb.data:
            command_spi.append(f'nick:{create_form.nick_rb.data}')

        if create_form.modder_cb.data:
            command_spi.append(f'moder:{create_form.modder_rb.data}')

        if create_form.unmodder_cb.data:
            command_spi.append(f'unmoder:{create_form.unmodder_rb.data}')

        if create_form.bot_cb.data:
            command_spi.append(f'bot:{create_form.bot_rb.data}')

        if create_form.event_cb.data:
            command_spi.append(f'event_commands:{create_form.event_rb.data}')

        if create_form.ty_cb.data:
            command_spi.append(f'twitch_youtube_connect:{create_form.ty_rb.data}')

        if create_form.find_cb.data:
            command_spi.append(f'find:{create_form.find_rb.data}')
        print(command_spi)

        create(current_user.email, create_form.bots_name.data, create_form.bots_token.data, create_form.bots_prefix.data, command_spi,
               [int(create_form.id_of_channels_from_where_receive_commands.data)], int(create_form.id_of_channel_where_history_will_be_saved.data),
               int(create_form.id_of_channel_where_will_report.data), int(create_form.moderator_role_id.data))

        return redirect('/download')

    return render_template("create.html", title='Содание бота', form=create_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if len(form.name.data) > 15:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Вы ввели трындец какое большое имя")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365)
    return res


@app.route("/cookie_delete")
def cookie_delete():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Ща всё удалим, не переживай")
        res.set_cookie("visits_count", str(visits_count),
                       max_age=0)
    else:
        res = make_response(f"Гуков, которых надо удалить нету")
    return res


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=port, host=host, debug=True)


if __name__ == '__main__':
    main()
