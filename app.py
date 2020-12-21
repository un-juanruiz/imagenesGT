
import os 
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db, close_db
import yagmail
import utils

app = Flask(__name__)

app.secret_key = os.urandom( 24 ) # reemplace por esta.


@app.route( '/' )
def index():
    #if g.user:
     #   return redirect( url_for( 'homeRedSocial' ) )
    return render_template( 'home.html' )

@app.route( '/login', methods=('GET', 'POST') )
def login():
    try:
      #  if g.user:
       #     return redirect( url_for( 'homeRedSocial' ) )
        if request.method == 'POST':
            db = get_db()
            error = None
            usuario = request.form['usuario']
            clave = request.form['clave']
            m = hashlib.sha256(b"clave")
            

            if not usuario:
                error = 'Debes ingresar el usuario'
                flash( error )
                return render_template( 'home.html' )

            if not clave:
                error = 'Contraseña requerida'
                flash( error )
                return render_template( 'home.html' )

            user = db.execute(
                'SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?', (usuario, m.digest()) #m.digest()
            ).fetchone()

            if user is None:
                error = 'Usuario o contraseña inválidos'
            else:
                session.clear()
                session['id_usuario'] = user[0]
                return redirect( url_for( 'homeRedSocial' ) )
            flash( error )
        return render_template( 'home.html' )
    except:
        return render_template( 'home.html' )

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
         m = generate_password_hash(clave)
         db = get_db()
         if not utils.isUsernameValid( usuario ):
            error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
            flash( error )
            return render_template( 'registro.html')
         if ( nombre ==""):
            error = "Debe de ingresar un nombre"
            flash( error )
            return render_template( 'registro.html' )
         if not utils.isEmailValid( correo ):
            error = 'Correo invalido'
            flash( error )
            return render_template( 'registro.html' )

         if (not utils.isPasswordValid( clave )):
            error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número y 8 caracteres'
            flash( error )
            return render_template( 'registro.html' )
         if (conf_clave != clave):
            error = 'Las contraseñas no coinciden'
            flash( error )
            return render_template( 'registro.html' )
         if db.execute( 'SELECT id_usuario FROM usuarios WHERE correo = ?', (correo,) ).fetchone() is not None:
            error = 'El correo ya existe'.format( correo )
            flash( error )
            return render_template( 'registro.html' )

         db.execute(
            "INSERT INTO usuarios (usuario, nombre, correo, contrasena) VALUES (?,?,?,?)",
            (usuario, nombre, correo, check_password_hash(m)) #m.digest()
            )
         db.commit() #Esa es la confirmación en la bd y el registro en bd 
         flash("Usuario registrado con éxito")
         return render_template('home.html')
      return render_template('registro.html')
   except:
      return render_template('registro.html')

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
            'SELECT * FROM usuario WHERE correo = ? ', (correo)
         ).fetchone()
         if user is None:
            error = 'El usuario no se encuentra en la base de datos'
         else:
            session.clear()
            session['user_id'] = user[0]
            error ="Se ha enviado el enlace a su correo electrónico"
            return redirect( url_for( 'recuperar' ) )
         flash( error )
   return render_template("recuperar.html")

@app.route('/nuevaContrasena/', methods=('GET', 'POST'))
def nuevaContrasena():
   return render_template("nuevaContrasena.html")

@app.route('/homeRedSocial/')
def homeRedSocial():
 return render_template("homeRedSocial.html")

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
    return redirect( url_for( 'home' ) )

@app.route('/nuevaImagen/', methods=('GET', 'POST'))
def nuevaImagen():
   return render_template("nuevaImagen.html")


@app.route('/actualizarImagen/', methods=('GET', 'POST'))
def actualizarImagen():
   return render_template("actualizarImagen.html")




#Cada una de las rutas que requiera información de un usuario, entra a la url "/login"
#Comprobando así que lo datos entregados sean de tipo  "POST" o "GET"

