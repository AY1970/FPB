from telegram import Update
from database import add_user, get_all_users, delete_user
from weather import get_weather_info

# Command handler /commands
def commands_handler(update: Update, context):
    commands_list = ['/add_contact', '/view_contacts', '/delete_contact', '/weather']
    update.message.reply_text("Available commands:\n" + "\n".join(commands_list))


# Command handler/add_contact
def add_contact_handler(update: Update, context):
    params = context.args
    if len(params) != 2:
        update.message.reply_text("Invalid command format. Enter /add contact <name> <number>")
    else:
        first_name, phone_number = params
        add_user(first_name, '', phone_number)  # Пустое поле last_name
        update.message.reply_text(f"Contact {first_name} successfully added.")


# Command handler /view_contacts
def view_contacts_handler(update: Update, context):
    users = get_all_users()
    if not users:
        update.message.reply_text("You have not saving contacts.")
    else:
        contacts = [f"{user[1]} {user[2]} - {user[3]}" for user in users]
        update.message.reply_text("Your contacts:\n" + "\n".join(contacts))


# Command handler /delete_contact
def delete_contact_handler(update: Update, context):
    params = context.args
    if len(params) != 1:
        update.message.reply_text("Invalid command format. Enter /delete_contact <name>")
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
            update.message.reply_text(f"Contact {first_name} successful removals.")
        else:
            update.message.reply_text(f"Name contact {first_name} no knowledge.")


# Command handler /weather
def weather_handler(update: Update, context):
    place_name = " ".join(context.args)
    if place_name:
        weather_info = get_weather_info(place_name)
        update.message.reply_text(weather_info)
    else:
        update.message.reply_text("Invalid command format. Enter /weather <location>")
