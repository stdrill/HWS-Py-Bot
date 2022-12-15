from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import symbols as sm
import bot_play as bp

if __name__ == '__main__':
    updater = Updater(bp.getToken())  


    updater.dispatcher.add_handler(CommandHandler('start', bp.newGame))
    updater.dispatcher.add_handler(CommandHandler('new_game', bp.newGame))
    updater.dispatcher.add_handler(CommandHandler('help', bp.help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, bp.help_command))  
    updater.dispatcher.add_handler(CallbackQueryHandler(bp.button))  

    updater.start_polling()
    updater.idle()