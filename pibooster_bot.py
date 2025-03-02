import telebot
import time
import requests
import schedule
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# 🔹 Configuration du bot
TOKEN = "8074251004:AAGqzwjTnj8Uc5aD1QyTFYHpGO0Zy4nhOyM"
CHANNEL_USERNAME = "@pibooster"
WEB_APP_URL = "https://pibooster.onrender.com"

bot = telebot.TeleBot(TOKEN)
user_stats = {}

# 🔹 Fonction pour vérifier l'abonnement
def check_subscription(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

# 🔹 Fonction pour afficher le menu persistant (clavier personnalisé)
def show_persistent_menu(user_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔗 Lien d'affiliation"), KeyboardButton("📊 Mes Statistiques"))
    keyboard.add(KeyboardButton("🌐 Accéder au site"), KeyboardButton("📢 Support"))

    bot.send_message(user_id, "📌 *Menu Principal Pi Booster* 📌\n"
                              "Utilise les boutons ci-dessous 👇",
                     parse_mode="Markdown", reply_markup=keyboard)

# 🔹 Fonction pour afficher le menu inline
def show_inline_menu(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔗 Lien d'affiliation", callback_data="invite"),
               InlineKeyboardButton("📊 Mes Statistiques", callback_data="stats"))
    markup.add(InlineKeyboardButton("🌐 Accéder au site", callback_data="access"),
               InlineKeyboardButton("📢 Support", callback_data="support"))

    bot.send_message(user_id, "📌 *Menu Principal Pi Booster* 📌\n"
                              "Clique sur un bouton ci-dessous 👇", 
                     parse_mode="Markdown", reply_markup=markup)

# 🔹 Commande /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id

    if user_id not in user_stats:
        user_stats[user_id] = {"affiliates": 0, "mining_speed": 1.0}  

    bot.send_message(user_id, "🚀 Bienvenue sur *Pi Booster* !\n\n"
                              "Pi Booster (πb) est conçu pour accélérer ton minage et "
                              "récompenser ton engagement dans l'écosystème Pi Network.\n"
                              "📢 Plus tu invites d’amis, plus ta vitesse de minage augmente !",
                     parse_mode="Markdown")

    show_persistent_menu(user_id)  # Afficher le menu persistant
    show_inline_menu(user_id)  # Afficher le menu inline

# 🔹 Gestion des boutons du menu inline
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(call.id)  # Évite le message "loading..."
    
    user_id = call.message.chat.id
    if call.data == "invite":
        referral_link = f"https://t.me/pibooster_bot?start={user_id}"
        bot.send_message(user_id, f"🚀 Rejoins-moi sur Pi Booster et booste ton minage !\n\n"
                                  f"📲 Inscris-toi via mon lien :\n{referral_link}\n\n"
                                  "✅ Invite tes amis pour augmenter ta vitesse de minage !")
    elif call.data == "stats":
        stats = user_stats.get(user_id, {"affiliates": 0, "mining_speed": 1.0})
        bot.send_message(user_id, f"📊 *Statistiques de minage :*\n\n"
                                  f"👥 Affiliés recrutés : *{stats['affiliates']}*\n"
                                  f"⚡ Vitesse de minage : *{stats['mining_speed']} πb/h*",
                         parse_mode="Markdown")
    elif call.data == "access":
        if check_subscription(user_id):
            bot.send_message(user_id, f"✅ Tu es bien abonné à Pi Booster 🎉\n"
                                      f"🌐 Accède à la Web App ici : [Pi Booster Web App]({WEB_APP_URL})",
                             parse_mode="Markdown")
        else:
            bot.send_message(user_id, "❌ Tu n'es pas encore abonné au canal !\n"
                                      "Rejoins-nous ici : 👉 [Pi Booster](https://t.me/pibooster)", parse_mode="Markdown")
    elif call.data == "support":
        bot.send_message(user_id, "📩 Besoin d'aide ? Rejoins notre groupe de support :\n"
                                  "👉 [Support Pi Booster](https://t.me/pibooster_support)",
                         parse_mode="Markdown")

# 🔹 Gestion des commandes du menu persistant
@bot.message_handler(func=lambda message: message.text in ["🔗 Lien d'affiliation", "📊 Mes Statistiques", 
                                                           "🌐 Accéder au site", "📢 Support"])
def handle_persistent_menu(message):
    user_id = message.chat.id
    text = message.text

    if text == "🔗 Lien d'affiliation":
        referral_link = f"https://t.me/pibooster_bot?start={user_id}"
        bot.send_message(user_id, f"🚀 Rejoins-moi sur Pi Booster et booste ton minage !\n\n"
                                  f"📲 Inscris-toi via mon lien :\n{referral_link}\n\n"
                                  "✅ Invite tes amis pour augmenter ta vitesse de minage !")
    
    elif text == "📊 Mes Statistiques":
        stats = user_stats.get(user_id, {"affiliates": 0, "mining_speed": 1.0})
        bot.send_message(user_id, f"📊 *Statistiques de minage :*\n\n"
                                  f"👥 Affiliés recrutés : *{stats['affiliates']}*\n"
                                  f"⚡ Vitesse de minage : *{stats['mining_speed']} πb/h*",
                         parse_mode="Markdown")

    elif text == "🌐 Accéder au site":
        if check_subscription(user_id):
            bot.send_message(user_id, f"✅ Tu es bien abonné à Pi Booster 🎉\n"
                                      f"🌐 Accède à la Web App ici : [Pi Booster Web App]({WEB_APP_URL})",
                             parse_mode="Markdown")
        else:
            bot.send_message(user_id, "❌ Tu n'es pas encore abonné au canal !\n"
                                      "Rejoins-nous ici : 👉 [Pi Booster](https://t.me/pibooster)", parse_mode="Markdown")

    elif text == "📢 Support":
        bot.send_message(user_id, "📩 Besoin d'aide ? Rejoins notre groupe de support :\n"
                                  "👉 [Support Pi Booster](https://t.me/pibooster_support)",
                         parse_mode="Markdown")

# 🔹 Planifier un rappel quotidien
def send_mining_reminder():
    for user_id in user_stats.keys():
        bot.send_message(user_id, "⏳ N'oublie pas de miner aujourd'hui !\n"
                                  f"🌐 Accède à la Web App ici : [Pi Booster Web App]({WEB_APP_URL})",
                         parse_mode="Markdown")

schedule.every().day.at("12:00").do(send_mining_reminder)

# 🔹 Thread pour exécuter les tâches planifiées
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(60)

# 🔹 Lancer le thread
threading.Thread(target=schedule_checker, daemon=True).start()

# 🔹 Lancer le bot
print("🚀 Bot en cours d'exécution...")
bot.polling(none_stop=True)
    
