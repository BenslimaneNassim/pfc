from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, CallbackContext, MessageHandler, filters
from django.conf import settings
async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [[KeyboardButton(text="Confirmer mon numéro de télephone", request_contact=True)]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        f'Hey {update.effective_user.first_name}!\nBienvenue au robot VintagedZ!\nClickez sur le bouton en bas pour confirmer votre numéro de télephone.',
        reply_markup=markup
    )
    return phone(update, context)
    # return PHONE_NUMBER

async def phone(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    phone_number = update.message.contact.phone_number
    zeb = {'phone_confirmed': False, 'phone_number': "0552796623"}
    zebb = {'phone_confirmed': False, 'phone_number': "0791894185"}
    profile = [zeb, zebb]
    if profile:
        profil = profile[0]
        checked = profil.get("phone_confirmed")
        print(checked)
        if checked == False:
            profil["phone_confirmed"] = True
            print(profil)
            await update.message.reply_text(f'Merci, {user.first_name}! Votre numéro {phone_number} a été confirmé.\nVous êtes maintenant un utilisateur vérifié')
            return start(update, context)
        elif profile.phone_confirmed == True:
            await update.message.reply_text(f'{user.first_name} Votre numéro {phone_number} a déja été confirmé.\nVous êtes un utilisateur vérifié')
            return start(update, context)
    else:
        await update.message.reply_text(f'{user.first_name} Votre profile n\'existe pas! \nCréez un compte sur vintagedz.pythonanywhere.com/login')
        return start(update, context)

    # Do something with the phone number (e.g., store it in a database, use it for authentication, etc.)
    # await update.message.reply_text(f'Merci, {user.first_name}! Votre numéro {phone_number} a été confirmé.\nVous êtes maintenant un utilisateur vérifié')
    # return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Conversation canceled.')
    return start(update, context)

app = ApplicationBuilder().token("5751003858:AAH5ig0KiOzHnA6MacLxLe3ItTFv7On__rk").build()

# app.add_handler(conv_handler)
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.CONTACT, phone))
app.add_handler(CommandHandler('cancel', cancel))



app.run_polling()
