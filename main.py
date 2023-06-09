# import asyncio
# from telegram.ext import Application, CommandHandler
# from handlers import commands_handler, add_contact_handler, view_contacts_handler, delete_contact_handler, weather_handler
#
# TOKEN = '6133590615:AAHDZf0DQYEq1zUeJQkcEYcJKHoqSF78RQc'
#
#
# async def start_command(update, context):
#     await update.message.reply_text('Hello! Welcome To Store!')
#
# async def main():
#     application = Application.builder().token(TOKEN).build()
#
#     # Commands
#     application.add_handler(CommandHandler('start', start_command))
#     application.add_handler(CommandHandler('add_contact', add_contact_handler))
#     application.add_handler(CommandHandler('view_contacts', view_contacts_handler))
#     application.add_handler(CommandHandler('delete_contact', delete_contact_handler))
#     application.add_handler(CommandHandler('weather', weather_handler))
#
#     try:
#         # Run bot
#         await application.initialize()
#         await application.start()
#         await application.updater.start_polling(1.0)
#
#         # Keep the main coroutine running
#         while True:
#             await asyncio.sleep(1)
#
#     except asyncio.CancelledError:
#         # This error occurs when the application is stopped
#         pass
#
#     finally:
#         # Stop bot
#         await application.stop(clean=True)
#
# if __name__ == '__main__':
#     asyncio.run(main())

import asyncio
import signal
from telegram.ext import Application, CommandHandler
from handlers import commands_handler, add_contact_handler, view_contacts_handler, delete_contact_handler, weather_handler

TOKEN = '6133590615:AAHDZf0DQYEq1zUeJQkcEYcJKHoqSF78RQc'

running = True

def signal_handler(signal, frame, application):
    global running
    running = False
    if application:
        application.stop()

# Registering a Signal Handler
signal.signal(signal.SIGINT, signal_handler)

async def start_command(update, context):
    await update.message.reply_text('Hello! Welcome To Store!')


async def main():
    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('add_contact', add_contact_handler))
    application.add_handler(CommandHandler('view_contacts', view_contacts_handler))
    application.add_handler(CommandHandler('delete_contact', delete_contact_handler))
    application.add_handler(CommandHandler('weather', weather_handler))

    try:
        # Run bot
        await application.initialize()
        await application.start()

        # Start polling task
        polling_task = asyncio.create_task(application.updater.start_polling(1.0))

        # Keep the main coroutine running
        while running:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        # This error occurs when the application is stopped
        pass

    finally:
        # Stop polling task
        polling_task.cancel()

        # Wait for the task to be cancelled
        await asyncio.gather(polling_task, return_exceptions=True)

        # Stop bot
        await application.stop(clean=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()  # Получение текущего цикла событий
    asyncio.run(main())








