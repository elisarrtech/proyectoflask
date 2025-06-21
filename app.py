from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_aqui"  # Cambia por algo seguro

# Datos mock con estructura extendida
chatbots = [
    {
        "id": 1,
        "nombre": "Chatbot Ventas",
        "descripcion": "Responde dudas sobre productos y promociones.",
        "config": {
            "idioma": "es",
            "activo": True,
            "respuesta_predeterminada": "Disculpa, no entendí tu pregunta."
        },
        "faqs": [
            {"id": 1, "pregunta": "¿Cuáles son sus horarios?", "respuesta": "Estamos abiertos de 9am a 6pm."},
            {"id": 2, "pregunta": "¿Dónde están ubicados?", "respuesta": "En la calle Principal 123."}
        ]
    },
    {
        "id": 2,
        "nombre": "Chatbot Soporte",
        "descripcion": "Ayuda con problemas técnicos y FAQs.",
        "config": {
            "idioma": "es",
            "activo": True,
            "respuesta_predeterminada": "Por favor, contacta a soporte."
        },
        "faqs": []
    }
]

def get_bot(bot_id):
    return next((b for b in chatbots if b["id"] == bot_id), None)

def get_faq(bot, faq_id):
    return next((f for f in bot["faqs"] if f["id"] == faq_id), None)

@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", chatbots=chatbots)

@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        config_idioma = request.form.get("idioma", "es")
        config_activo = request.form.get("activo") == "on"
        config_resp = request.form.get("respuesta_predeterminada", "")

        new_id = max([b["id"] for b in chatbots], default=0) + 1
        chatbots.append({
            "id": new_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "config": {
                "idioma": config_idioma,
                "activo": config_activo,
                "respuesta_predeterminada": config_resp
            },
            "faqs": []
        })
        flash(f'Chatbot "{nombre}" creado con éxito.', "success")
        return redirect(url_for("dashboard"))
    return render_template("new_bot.html")

@app.route("/editar/<int:bot_id>", methods=["GET", "POST"])
def editar(bot_id):
    bot = get_bot(bot_id)
    if not bot:
        flash("Chatbot no encontrado", "warning")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        bot["nombre"] = request.form["nombre"]
        bot["descripcion"] = request.form["descripcion"]
        bot["config"]["idioma"] = request.form.get("idioma", "es")
        bot["config"]["activo"] = request.form.get("activo") == "on"
        bot["config"]["respuesta_predeterminada"] = request.form.get("respuesta_predeterminada", "")
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

# --- FAQ management ---

@app.route("/faqs/<int:bot_id>")
def faqs(bot_id):
    bot = get_bot(bot_id)
    if not bot:
        flash("Chatbot no encontrado", "warning")
        return redirect(url_for("dashboard"))
    return render_template("faqs.html", bot=bot, faqs=bot["faqs"])

@app.route("/faqs/<int:bot_id>/nuevo", methods=["GET", "POST"])
def faq_nuevo(bot_id):
    bot = get_bot(bot_id)
    if not bot:
        flash("Chatbot no encontrado", "warning")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        pregunta = request.form["pregunta"]
        respuesta = request.form["respuesta"]
        new_id = max([f["id"] for f in bot["faqs"]], default=0) + 1
        bot["faqs"].append({"id": new_id, "pregunta": pregunta, "respuesta": respuesta})
        flash("FAQ agregada correctamente.", "success")
        return redirect(url_for("faqs", bot_id=bot_id))

    return render_template("new_faq.html", bot=bot)

@app.route("/faqs/<int:bot_id>/editar/<int:faq_id>", methods=["GET", "POST"])
def faq_editar(bot_id, faq_id):
    bot = get_bot(bot_id)
    if not bot:
        flash("Chatbot no encontrado", "warning")
        return redirect(url_for("dashboard"))

    faq = get_faq(bot, faq_id)
    if not faq:
        flash("FAQ no encontrada", "warning")
        return redirect(url_for("faqs", bot_id=bot_id))

    if request.method == "POST":
        faq["pregunta"] = request.form["pregunta"]
        faq["respuesta"] = request.form["respuesta"]
        flash("FAQ actualizada correctamente.", "success")
        return redirect(url_for("faqs", bot_id=bot_id))

    return render_template("edit_faq.html", bot=bot, faq=faq)

@app.route("/faqs/<int:bot_id>/borrar/<int:faq_id>", methods=["POST"])
def faq_borrar(bot_id, faq_id):
    bot = get_bot(bot_id)
    if not bot:
        flash("Chatbot no encontrado", "warning")
        return redirect(url_for("dashboard"))
    bot["faqs"] = [f for f in bot["faqs"] if f["id"] != faq_id]
    flash("FAQ borrada correctamente.", "danger")
    return redirect(url_for("faqs", bot_id=bot_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
