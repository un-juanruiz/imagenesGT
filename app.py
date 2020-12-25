
import functools
import os 
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g
import hashlib

from flask.helpers import make_response
from db import get_db, close_db
import yagmail
import utils
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.urandom( 24 ) # reemplace por esta.


#Esto hace que g.user sea definido
@app.before_request
def load_logged_in_user():
    user_id = session.get( 'id_usuario' )

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuarios WHERE id_usuario = ?', (user_id,)
        ).fetchone()

@app.route( '/' )
def index():
   if g.user:
      return redirect( url_for( 'homeRedSocial' ) )
   return redirect( url_for( 'login' ) )

@app.route( '/login/', methods=('GET', 'POST') )
def login():
   try:
      if g.user:
         return redirect( url_for( 'homeRedSocial' ) )
      if request.method == 'POST':
         db = get_db()
         error = None
         usuario = request.form['usuario']
         clave = request.form['clave']

         if not usuario:
            error = 'Debes ingresar el usuario'
            flash( error )
            return render_template( 'home.html', titulo = "Ingresa" )

         if not clave:
            error = 'Contraseña requerida'
            flash( error )
            return render_template( 'home.html', titulo = "Ingresa" )

         user = db.execute(
            'SELECT * FROM usuarios WHERE usuario = ?', (usuario,)
            ).fetchone()
         if user is None:
               error = 'Usuario o contraseña inválidos'
         else:
            if check_password_hash (user[4], clave):
               session.clear()
               session['id_usuario'] = user[0]
               resp = make_response(redirect( url_for( 'homeRedSocial' ) ))
               resp.set_cookie('username', usuario)
               return redirect( url_for( 'homeRedSocial' ) )
               #return redirect( url_for( 'homeRedSocial' ) )
            else:
               error = "Usuario o contraseña inválidos"
         flash( error )
      return render_template( 'home.html', titulo = "Ingresa" )
   except:
      return render_template( 'home.html', titulo = "Ingresa" )




    
@app.route('/registrar/', methods=('GET', 'POST'))
def registrar():
   try:
      if request.method == 'POST':
         usuario = request.form['usuario']
         nombre = request.form['nombre']
         correo = request.form['correo']
         clave = request.form['clave']
         conf_clave = request.form['conf_clave']
         error = None
         #m = hashlib.sha256(str(clave).encode('utf-8')
         db = get_db()
         if not utils.isUsernameValid( usuario ):
            error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
            flash( error )
            return render_template( 'registro.html', titulo = "Registrar")
         if ( nombre ==""):
            error = "Debe de ingresar un nombre"
            flash( error )
            return render_template( 'registro.html', titulo = "Registrar")
         if not utils.isEmailValid( correo ):
            error = 'Correo invalido'
            flash( error )
            return render_template( 'registro.html', titulo = "Registrar")

         if (not utils.isPasswordValid( clave )):
            error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número y 8 caracteres'
            flash( error )
            return render_template( 'registro.html', titulo = "Registrar")
         if (conf_clave != clave):
            error = 'Las contraseñas no coinciden'
            flash( error )
            return render_template( 'registro.html', titulo = "Registrar")
         if db.execute( 'SELECT id_usuario FROM usuarios WHERE correo = ?', (correo,) ).fetchone() is not None:
            error = 'El correo ya existe'.format( correo )
            flash( error )
            return render_template( 'registro.html', titulo = "Registrar" )
         m = generate_password_hash(clave)
         db.execute(
            "INSERT INTO usuarios (usuario, nombre, correo, contrasena) VALUES (?,?,?,?)",
            (usuario, nombre, correo, m) 
            )
         db.commit() #Esa es la confirmación en la bd y el registro en bd 
         flash("Usuario registrado con éxito")
         return render_template('home.html', titulo = "Ingresa")
      return render_template('registro.html', titulo = "Registrar")
   except:
      return render_template('registro.html', titulo = "Registrar")


@app.route('/recuperarContrasena/', methods=('GET', 'POST'))
def recuperarContrasena():
   if request.method == 'POST':
         correo = request.form['correo']
         error = None
         db = get_db()
         if not utils.isEmailValid( correo ):
                error = 'Correo invalido'
                flash( error )
                return render_template( 'recuperar.html' )
         user = db.execute(
            'SELECT * FROM usuarios WHERE correo = ? ', (correo,)
         ).fetchone()
         if user is None:
            error = 'El usuario no se encuentra registrado en la base de datos'
         else:
            session.clear()
            error ="Se ha enviado el enlace a su correo electrónico"
            return redirect( url_for( 'login' ) )
         flash( error )
   return render_template("recuperar.html")

@app.route('/nuevaContrasena/', methods=('GET', 'POST'))
def nuevaContrasena():
   return render_template("nuevaContrasena.html")

@app.route('/homeRedSocial')
def homeRedSocial():
   if g.user:
      return render_template("homeRedSocial.html")
   else:
      return redirect( url_for( 'login' ) )

@app.route('/eliminarImagen/<int:id_imagen>')
def eliminarImagen(id_imagen):
   return render_template("homeRedSocial.html")

@app.route('/descargarImagen/<int:id_imagen>')
def descargarImagen(id_imagen):
   return render_template("homeRedSocial.html")

'''@app.route('/salir/')
def salirSistema():
   return render_template("home.html")'''

@app.route( '/salir' )
def logout():
    session.clear()
    return redirect( url_for( 'login' ) )

@app.route('/nuevaImagen/', methods=('GET', 'POST'))
def nuevaImagen():
   return render_template("nuevaImagen.html")


@app.route('/actualizarImagen/', methods=('GET', 'POST'))
def actualizarImagen():
   
   if g.user:
      return render_template("actualizar.html", titulo="Actualizar imagen")
   else:
      return redirect( url_for( 'login' ) )

if __name__ == '__main__':
   app.run()

