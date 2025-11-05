from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Credenciales simples
USUARIO = "admin"
CLAVE = "admin"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    clave = request.form["clave"]

    if usuario == USUARIO and clave == CLAVE:
        session["usuario"] = usuario
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Usuario o contraseña incorrectos")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("index"))

    datos_pokemon = None

    if request.method == "POST":
        nombre = request.form["nombre"].lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            datos_pokemon = respuesta.json()
        else:
            datos_pokemon = "No se encontró el Pokémon"

    return render_template("dashboard.html", usuario=session["usuario"], datos_pokemon=datos_pokemon)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# 👇 ESTA LÍNEA ES CLAVE PARA VERCEL
app = app
