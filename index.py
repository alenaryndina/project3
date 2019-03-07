import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('news.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             login VARCHAR(50),
                             name VARCHAR(50),
                             fname VARCHAR(50),
                             rieltor int(1),
                             password_hash VARCHAR(128)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, login, password_hash, fname, name, rieltor):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (login, name,fname,rieltor, password_hash) 
                          VALUES (?,?,?,?,?)''', (login, password_hash, fname, name, rieltor))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = " + str(user_id))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, login, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ? AND password_hash = ?", (login, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False, None)


class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                   title VARCHAR(100),
                                   content VARCHAR(1000),
                                   user_id INTEGER
                                   )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                            (title, content, user_id) 
                            VALUES (?,?,?)''', (title, content, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = "+ (str(news_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM news WHERE user_id = " + (str(user_id)) + " ORDER BY id DESC")
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ''' + str(news_id))
        cursor.close()
        self.connection.commit()


class PostModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
                                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                   title VARCHAR(100),
                                   content VARCHAR(1000),
                                   user_id INTEGER,
                                   image VARCHAR(200),
                                   cost VARCHAR(100),
                                   rooms VARCHAR(10),
                                   floor VARCHAR(10),
                                   type_post VARCHAR(1),
                                   address VARCHAR(1000),
                                   contact VARCHAR(100),
                                   views VARCHAR(100)
                                   )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_id,image,cost,rooms,floor,type_post,address,contact, views):
        cursor = self.connection.cursor()
        fname,ffile = image
        print(fname,ffile)
        f = open("static/img/"+fname.filename,"wb")
        f.write(ffile)
        f.close()
        cursor.execute('''INSERT INTO posts 
                            (title, content, user_id,image,cost,rooms,floor,type_post,address,contact,views) 
                            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (title, content, str(user_id),"img/"+fname.filename, cost, rooms,floor, type_post, address,contact, views))
        cursor.close()
        self.connection.commit()

    def get(self, posts_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = "+ (str(posts_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM posts WHERE user_id = " + (str(user_id)) + " ORDER BY id DESC")
        else:
            cursor.execute("SELECT * FROM posts")
        rows = cursor.fetchall()
        return rows

    def delete(self, posts_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM posts WHERE id = ''' + str(posts_id))
        cursor.close()
        self.connection.commit()

    def add_view(self, posts_id):
        data = self.get(posts_id)
        cursor = self.connection.cursor()
        cursor.execute(''' UPDATE posts SET views ='''+str(int(data[11])+1) + ''' WHERE id = ''' + str(posts_id))
        cursor.close()
        self.connection.commit()



db = DB()
user_model = UserModel(db.get_connection())
post_model = PostModel(db.get_connection())
user_model.init_table()
post_model.init_table()

from flask import Flask, redirect, render_template, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, FileField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

    password2 = PasswordField('Повторить пароль', validators=[DataRequired()])
    fname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    rieltor = RadioField('Категория', choices=[('1', 'Риелтор'), ('0', 'Покупатель')])
    submit = SubmitField('Войти')

class AddPost(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField('Описание ', validators=[DataRequired()])
    type_post = RadioField('Категория', choices=[('0', 'Дом'), ('1', 'Квартира')])
    rooms = TextAreaField('Количество комнат ', validators=[DataRequired()])
    floor = TextAreaField('Этаж', validators=[DataRequired()])
    image = FileField("Image")
    address = TextAreaField('Адрес ', validators=[DataRequired()])
    contact = TextAreaField('Номер телефона ', validators=[DataRequired()])
    cost = TextAreaField('Цена ', validators=[DataRequired()])
    submit = SubmitField('Добавить')



class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
user_id = None
user_status = False


# http://127.0.0.1:8080/login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_id, user_status
    form = LoginForm()
    user_status, user_id = user_model.exists(form.login.data, form.password.data)



    if form.validate_on_submit() and user_status:
        print(user_status, user_id )
        session["username"] = form.login.data
        print(user_model.get(user_id))
        if user_model.get(user_id)[4] == 1:
            session["rieltor"] = True
        else:
            session["rieltor"] = False
        return redirect('/index')
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global user_status
    user_status = False
    return redirect('/index')


# http://127.0.0.1:8080/
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    global user_id, user_status
    form = RegForm()
    login = form.login.data
    fname = form.fname.data
    name = form.name.data
    rieltor = form.rieltor.data
    password_hash = form.password.data
    user_model.insert(login, password_hash, fname, name, rieltor)

    if form.validate_on_submit():
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/index')
@app.route('/news')
def news():
    if user_status:
        post_list = post_model.get_all()
        if session["rieltor"]:
            return render_template('index.html', posts=post_list)
        else:
            return render_template('index0.html', posts=post_list)

    else:
        return redirect('/login')

@app.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    if user_status:

        post= post_model.get(post_id)
        post_model.add_view(post_id)
        if session["rieltor"]:
            return render_template('post.html', post=post)
        else:
            return render_template('post0.html', post=post)

    else:
        return redirect('/login')


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if not user_status:
        return redirect('/login')
    form = AddPost()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print(2)
        title = form.title.data
        content = form.content.data
        type_post = form.type_post.data
        rooms = form.rooms.data
        floor = form.floor.data
        address = form.address.data
        contact = form.contact.data
        cost = form.cost.data
        image=  (form.image.data, form.image.data.read())

        views = 0
        post_model.insert(title, content, str(user_id),image, cost, rooms,floor, type_post, address, contact, views)
        return redirect("/index")
    return render_template('add_post.html', title='Добавление новости', form=form, username=user_id)



@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    if not user_status:
        return redirect('/login')
    post_model.delete(post_id)
    return redirect("/index")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
