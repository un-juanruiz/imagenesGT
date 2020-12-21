import os # Para generar el aleatorio
#importer el modulo sqlite3
import sqlite3
#importer modulo de error de sqlite3
from sqlite3 import Error
#acede a los valores de las variables enviadas por los HTML.
from flask import Flask, request, render_template, redirect, url_for, current_app, g

def get_db():
    try:
        if 'db' not in g:
            g.db = sqlite3.connect('BaseDatos.db')
        return g.db
    except Error:
        print(Error)

def close_db():
    db = g.pop( 'db', None )

    if db is not None:
        db.close()

