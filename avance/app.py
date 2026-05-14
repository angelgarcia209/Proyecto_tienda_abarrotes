from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "garcia123"

def crear_db():
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        correo TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        categoria TEXT,
        precio REAL,
        stock INTEGER
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("Arroz 1kg", "Granos", 28.5, 35),
            ("Frijol 1kg", "Granos", 32, 20),
            ("Leche 1L", "Lácteos", 24, 0),
            ("Pan blanco", "Panadería", 45, 12),
            ("Azúcar 1kg", "Despensa", 27, 18)
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            productos
        )

    conn.commit()
    conn.close()

crear_db()

@app.route("/")
def inicio():
    return render_template("login.html")

@app.route("/ingresar", methods=["POST"])
def ingresar():
    correo = request.form["correo"]
    password = request.form["password"]

    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE correo=? AND password=?", (correo, password))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        session["usuario"] = usuario[1]
        return redirect("/productos")
    return "Datos incorrectos"

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]

        conn = sqlite3.connect("tienda.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
            (nombre, correo, password)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("registro.html")

@app.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    mensaje = ""
    if request.method == "POST":
        correo = request.form["correo"]

        conn = sqlite3.connect("tienda.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE correo=?", (correo,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            mensaje = "Tu contraseña es: " + resultado[0]
        else:
            mensaje = "Correo no encontrado"

    return render_template("recuperar.html", mensaje=mensaje)

@app.route("/productos")
def productos():
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, categoria, precio, stock FROM productos")
    lista = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=lista)

if __name__ == "__main__":
    app.run(debug=True)