from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ==========================
# CREAR BASE DE DATOS
# ==========================
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ==========================
# FUNCIÓN IMC
# ==========================
def evaluar_imc(peso, estatura):
    imc = peso / (estatura ** 2)

    if imc < 18.5:
        nivel = "Bajo peso"
        recomendacion = "Consumir alimentos ricos en nutrientes, aumentar proteínas y carbohidratos saludables."
        ejercicio = "Ejercicios de fuerza ligeros y caminatas."
    elif 18.5 <= imc <= 24.9:
        nivel = "Peso normal"
        recomendacion = "Mantener alimentación balanceada."
        ejercicio = "Ejercicio regular: caminar, correr, bicicleta."
    elif 25 <= imc <= 29.9:
        nivel = "Sobrepeso"
        recomendacion = "Reducir azúcares, comida procesada y grasas saturadas."
        ejercicio = "Cardio 30 minutos diarios."
    elif 30 <= imc <= 34.9:
        nivel = "Obesidad grado I"
        recomendacion = "Dieta supervisada y control médico."
        ejercicio = "Ejercicio moderado y caminatas."
    elif 35 <= imc <= 39.9:
        nivel = "Obesidad grado II"
        recomendacion = "Consulta médica y plan nutricional."
        ejercicio = "Rutina supervisada por especialista."
    else:
        nivel = "Obesidad grado III"
        recomendacion = "Atención médica especializada."
        ejercicio = "Actividad física bajo control médico."

    return round(imc, 2), nivel, recomendacion, ejercicio

# ==========================
# RUTAS
# ==========================
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
                           (nombre, correo, password))
            conn.commit()
        except:
            conn.close()
            return "El correo ya está registrado"

        conn.close()
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE correo=? AND password=?", (correo, password))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            return redirect(url_for("imc"))
        else:
            return "Datos incorrectos"

    return render_template("login.html")


@app.route("/imc", methods=["GET", "POST"])
def imc():
    resultado = None

    if request.method == "POST":
        peso = float(request.form["peso"])
        estatura = float(request.form["estatura"])

        imc_valor, nivel, recomendacion, ejercicio = evaluar_imc(peso, estatura)

        resultado = {
            "imc": imc_valor,
            "nivel": nivel,
            "recomendacion": recomendacion,
            "ejercicio": ejercicio
        }

    return render_template("imc.html", resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)