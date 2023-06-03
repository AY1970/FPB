import requests
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
import sqlite3

TOKEN = '@AVFPB_bot:6133590615:AAHDZf0DQYEq1zUeJQkcEYcJKHoqSF78RQc'
bot = Bot(token=TOKEN)

# Функция для получения информации о погоде
def get_weather_info(place_name):
    location_url = "https://geocoding-api.open-meteo.com/v1/search"
    weather_url = "https://api.open-meteo.com/v1/forecast"

    try:
        location_params = {"name": place_name}
        location_response = requests.get(location_url, params=location_params)

        if location_response.status_code != 200:
            return f"Error getting location data for {place_name}. Status code: {location_response.status_code}"

        location_data = location_response.json()
        latitude = location_data["results"][0]["latitude"]
        longitude = location_data["results"][0]["longitude"]

    except (KeyError, IndexError):
        return "Input Error. Please enter a valid place."

    weather_params = {"latitude": latitude, "longitude": longitude, "current_weather": True}
    weather_response = requests.get(weather_url, params=weather_params)

    if weather_response.status_code != 200:
        return f"Error getting weather data for {place_name}. Status code: {weather_response.status_code}"

    weather_data = weather_response.json()
    temperature = weather_data.get("current_weather", {}).get("temperature", None)

    if temperature is None:
        return "Error getting weather data."

    return f"Current weather for {place_name}:\nTemperature: {temperature}°C"


DATABASE_FILE = 'contacts.db'


def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Создание таблицы users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT,
                      last_name TEXT,
                      phone_number TEXT)''')

    conn.commit()
    conn.close()


def add_user(first_name, last_name, phone_number):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Вставка нового пользователя в таблицу users
    cursor.execute('''INSERT INTO users (first_name, last_name, phone_number)
                      VALUES (?, ?, ?)''', (first_name, last_name, phone_number))

    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Получение всех пользователей из таблицы users
    cursor.execute('''SELECT * FROM users''')
    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_user(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Удаление пользователя из таблицы users по его id
    cursor.execute('''DELETE FROM users WHERE id = ?''', (user_id,))

    conn.commit()
    conn.close()


# Обработчик команды /commands
def commands_handler(update: Update, context):
    commands_list = ['/add_contact', '/view_contacts', '/delete_contact', '/weather']
    update.message.reply_text("Доступні команди:\n" + "\n".join(commands_list))


# Обработчик команды /add_contact
def add_contact_handler(update: Update, context):
    params = context.args
    if len(params) != 2:
        update.message.reply_text("Неправильний формат команди. Введіть /add_contact <ім'я> <номер>")
    else:
        first_name, phone_number = params
        add_user(first_name, '', phone_number)  # Пустое поле last_name
        update.message.reply_text(f"Контакт {first_name} успішно доданий.")


# Обработчик команды /view_contacts
def view_contacts_handler(update: Update, context):
    users = get_all_users()
    if not users:
        update.message.reply_text("У вас немає збережених контактів.")
    else:
        contacts = [f"{user[1]} {user[2]} - {user[3]}" for user in users]
        update.message.reply_text("Ваші контакти:\n" + "\n".join(contacts))


# Обработчик команды /delete_contact
def delete_contact_handler(update: Update, context):
    params = context.args
    if len(params) != 1:
        update.message.reply_text("Неправильний формат команди. Введіть /delete_contact <ім'я>")
    else:
        first_name = params[0]
        users = get_all_users()
        user_id = None

        for user in users:
            if user[1] == first_name:
                user_id = user[0]
                break

        if user_id is not None:
            delete_user(user_id)
            update.message.reply_text(f"Контакт {first_name} успішно видалений.")
        else:
            update.message.reply_text(f"Контакт з ім'ям {first_name} не знайдений.")


# Обработчик команды /weather
def weather_handler(update: Update, context):
    place_name = " ".join(context.args)
    if place_name:
        weather_info = get_weather_info(place_name)
        update.message.reply_text(weather_info)
    else:
        update.message.reply_text("Неправильний формат команди. Введіть /weather <місто>")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("commands", commands_handler))
    dispatcher.add_handler(CommandHandler("add_contact", add_contact_handler))
    dispatcher.add_handler(CommandHandler("view_contacts", view_contacts_handler))
    dispatcher.add_handler(CommandHandler("delete_contact", delete_contact_handler))
    dispatcher.add_handler(CommandHandler("weather", weather_handler))

    updater.start_polling()
    updater.idle()
