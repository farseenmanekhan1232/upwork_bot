import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from db_manager import add_alert
from config import Config

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command to open the Web App for alert configuration."""
    url = "http://127.0.0.1:5000/set-alert"  # Replace with your actual domain
    await update.message.reply_text(
        "Please configure your job alert:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Alert Config", web_app=WebAppInfo(url=url))]])
    )

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle data sent from the Telegram Web App."""
    try:
        data = json.loads(update.message.web_app_data.data)  # Access data sent from web app
        user_id = update.effective_user.id
        # Save the alert data to the database
        add_alert(user_id, data)
        await update.message.reply_text("Your alert has been configured successfully!")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    """Main function to run the Telegram bot."""
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    application.run_polling()

if __name__ == '__main__':
    main()
