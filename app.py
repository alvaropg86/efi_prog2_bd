from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy #hace objetos a las tablas
from werkzeug.urls import url_parse
# IMPORTAMOS EL MANEJADOR DE MYSQL
from pymysql import * #driver o port para que python sepa como comunicarse con la base de datos

from forms import * #archivo nuestro
from models import * #archivo nuestro



login_manager = LoginManager()
# CREAMOS EL OBJETO SQLALCHEMY

app = Flask(__name__)

app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
# LE DECIMOS A LA APP DONDE SE ENCUENTRA LA BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BD2021:BD2021itec@143.198.156.171/apg_lp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)

db.create_all()


posts = [] #este ya no sirve mas porque no graba mas en memoria pero aun no lo quitamos porque hay muchas funciones que estan relacionadas

@app.route("/")
def index():
    form = LoginForm()
    return render_template("login_form.html", form=form)

# Un slug es una cadena de caracteres alfanuméricos (más el carácter ‘-‘)
# sin espacios, tildes ni signos de puntuación
@app.route("/p/<string:slug>/")
def show_post(slug):
    return render_template("post_view.html", slug_title=slug)

# Tené en cuenta que asignamos un valor por defecto al parámetro post_id 
# para el caso en que no se pase el mismo en la URL.
@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
# SI NO ESTÁS AUTENTICADO Y QUERÉS INGRESAR, LA APP TE REDIRIGE A LA PAGINA DE LOGIN
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        title_slug = form.title_slug.data
        content = form.content.data

        post = {'title': title, 'title_slug': title_slug, 'content': content}
        posts.append(post)

        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    # PRIMERO COMPROBAMOS SI EL USUARIO ESTÁ AUTENTICADO
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        # SI EXISTE UN USUARIO CON ESE EMAIL Y LA CLAVE ES CORRECTA, 
        # AUTENTICAMOS EL USUARIO USANDO EL METODO login_user
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            # COMPROBAMOS SI RECIBIMOS EL PARAMETRO NEXT. 
            # ESTO PASA CUANDO SE INTENTA INGRESAR A UNA PAGINA PROTEGIDA SIN ESTAR AUTENTICADO.
            # SI NO SE RECIBE EL NEXT, REDIRIGIMOS EL USUARIO A LA PAGINA DE INICIO
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user() #este es un metodo de FlaskLogin
    return redirect(url_for('index'))


# Un slug es una cadena de caracteres alfanuméricos (más el carácter ‘-‘)
# sin espacios, tildes ni signos de puntuación
@app.route("/")
def show_post():
    post = Sexo.get_all()
    if post is None:
        print("error")
    return render_template("public/post_view.html", post=post)    

if __name__ == '__main__':
    app.run(debug=True)