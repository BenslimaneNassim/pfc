# from telegram import Update
# from telegram.ext import Updater, CommandHandler


# API_KEY = '5751003858:AAH5ig0KiOzHnA6MacLxLe3ItTFv7On__rk'

# def start(update, context):
#     print(f'{update.message.chat.first_name} vient de démarrer le bot')
#     update.message.reply_text('Bienvenue sur DZVintageBot !')

# def help(update, context):
#     print(f'{update.message.chat.first_name} vient de demander de l\'aide')
#     update.message.reply_text('Je suis là pour vous aider')

# if __name__ == '__main__':
#     updater = Updater(API_KEY, use_context=True)
#     dp = updater.dispatcher

#     dp.add_handler(CommandHandler('start', start))
#     dp.add_handler(CommandHandler('help', help))

#     updater.start_polling()
#     updater.idle()


#Now we rewrite the same code but with version > 20.0 of python-telegram-bot

# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}')



# app = ApplicationBuilder().token("5751003858:AAH5ig0KiOzHnA6MacLxLe3ItTFv7On__rk").build()

# app.add_handler(CommandHandler("hello", hello))

# app.run_polling()