from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#imports nuevos:
from flask import url_for
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from app import db


users = []
# LA FUNCION get_user LA VAMOS A UTILIZAR MOMENTANEAMENTE PARA BUSCAR UN USUARIO POR SU MAIL 
# DE LA LISTA DE USUARIOS
def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None


# nullable = false significa que no admite nulos
# cuando esta tildado no admite nulos
class Sexo(db.Model):
    # DEFINIMOS LA CLAVE PRIMARIA
    id = db.Column(db.Integer(11), primary_key=True)
    # SE FIJA LA RELACION ENTRE LA CLASE POST Y LA CLASE USER MEDIANTE EL ATRIBUTO user_id. 
    # ESTE ATRIBUTO ES UNA CLAVE FORANEA, QUE NOS SIRVE PARA REFERENCIAR AL USUARIO QUE ESCRIBIÓ EL POST.
    inicial = db.Column(db.String(1), nullable=False)
    descripcion = db.Column(db.String(25), nullable=False)

    def __repr__(self): #preguntar a agu
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.title_slug = f'{self.title_slug}-{count}'

    # DEFINIMOS EL METODO public_url() PARA OBTENER LA URL DEL POST A PARTIR DEL SLUG DEL TITULO.
    def public_url(self):
        return url_for('public.show_post', slug=self.title_slug)

    @staticmethod
    def get_by_slug(slug):
        return Sexo.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_all():
        return Sexo.query.all()
