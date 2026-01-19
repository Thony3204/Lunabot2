import telebot
from openai import OpenAI

# Tus keys reales aquí
BOT_TOKEN = "8500832493:AAFpXFpv1XxKJMlD8CxEvuO1luBVJtNVwTo"  # Del BotFather
OPENROUTER_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

# Memoria simple: diccionario {chat_id: referrer_id} – solo para este run (se pierde al reiniciar, pero sirve para bootstrap)
referrers = {}  # {chat_id: referrer_id}

@bot.message_handler(commands=['start'])
def start(message):
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    
    chat_id = message.chat.id
    if ref_id:
        referrers[chat_id] = ref_id  # Guardamos el referrer de quien la invitó
        bot.reply_to(message, f"¡Bienvenida Reina! Tu amiga te refirió con código {ref_id} – cuando invites tú ganarás comisión por ellas. Mándame lo que necesites:\n1. Ideas live\n2. Horario óptimo\n3. Respuestas viewers\n4. Motivación")
    else:
        bot.reply_to(message, "¡Bienvenida Reina! Soy LunaBot Elite. Mándame lo que necesites:\n1. Ideas live\n2. Horario óptimo\n3. Respuestas viewers\n4. Motivación\n\nEj: 'ideas live 1 hora baile'")

@bot.message_handler(func=lambda m: True)
def handle(message):
    text = message.text.lower()
    chat_id = message.chat.id

    # Prompt base para la IA (mentora empoderadora, sin cruzar líneas)
    prompt = f"""
    Eres LunaBot Elite, mentora IA empoderadora de Luna Roja Agency.
    Responde en español motivador y otro idiomas detecta el idioma de la chica, positivo, amigable  pero 100% limpio y profesional.
    Enfócate en engagement real, viralidad, horarios, edición, interacción sin contenido explícito.
    Sé útil, rápida y adictiva. Input: {text}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",  # o el que tengas más rápido
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = "¡Ups! Algo salió mal con la IA. Intenta de nuevo Reina, estoy aquí para ayudarte 🔥"

    # Mensaje final con recordatorio de referral PERSONAL (no link fijo)
    reply = f"{answer}\n\n¿Te sirvió Reina? 🔥 Comparte tu link referral personal (lo ves en tu panel Luna Roja después de registrarte y ser aprobada) con tus amigas y gana 30% comisión ilimitada cada vez que paguen suscripción. ¡Tú mandas tu reino!"

    bot.reply_to(message, reply)

print("LunaBot Elite corriendo...")
bot.polling()

