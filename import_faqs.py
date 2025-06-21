import json
from app import db, FAQ, Chatbot, app

with app.app_context():
    with open("faqs_data.json", "r", encoding="utf-8") as f:
        faqs = json.load(f)
    
    for faq in faqs:
        bot = Chatbot.query.get(faq["bot_id"])
        if bot:
            nueva_faq = FAQ(
                pregunta=faq["pregunta"],
                respuesta=faq["respuesta"],
                chatbot=bot
            )
            db.session.add(nueva_faq)
        else:
            print(f"❌ No se encontró bot con ID {faq['bot_id']}")
    
    db.session.commit()
    print("✅ FAQs importadas exitosamente.")
