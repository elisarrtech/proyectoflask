from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_aqui"  # Cambia esta clave por una segura

# Datos mock para ejemplo (reemplaza luego con base de datos real)
chatbots = [
    {"id": 1, "nombre": "Chatbot Ventas", "descripcion": "Responde dudas sobre productos y promociones."},
    {"id": 2, "nombre": "Chatbot Soporte", "descripcion": "Ayuda con problemas técnicos y FAQs."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", chatbots=chatbots)

@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        new_id = max(bot["id"] for bot in chatbots) + 1 if chatbots else 1
        chatbots.append({"id": new_id, "nombre": nombre, "descripcion": descripcion})
        flash(f'Chatbot "{nombre}" creado con éxito.', "success")
        return redirect(url_for("dashboard"))
    return render_template("new_bot.html")

@app.route("/editar/<int:bot_id>", methods=["GET", "POST"])
def editar(bot_id):
    bot = next((b for b in chatbots if b["id"] == bot_id), None)
    if not bot:
        flash("Chatbot no encontrado", "warning")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        bot["nombre"] = request.form["nombre"]
        bot["descripcion"] = request.form["descripcion"]
        flash(f'Chatbot "{bot["nombre"]}" actualizado correctamente.', "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_bot.html", bot=bot)

@app.route("/borrar", methods=["POST"])
def borrar():
    bot_id = int(request.form.get("bot_id"))
    global chatbots
    chatbots = [bot for bot in chatbots if bot["id"] != bot_id]
    flash(f"Chatbot con ID {bot_id} borrado correctamente.", "danger")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

