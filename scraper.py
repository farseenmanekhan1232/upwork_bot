from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from db_manager import add_alert, list_alerts, delete_alert
from config import TELEGRAM_TOKEN
import logging

logging.basicConfig(level=logging.INFO)
user_alerts = {}

# Categories mapping
categories = {
    "531770282584862721": "Accounting & Consulting",
    "531770282580668416": "Admin Support",
    "531770282580668417": "Customer Service",
    "531770282580668420": "Data Science & Analytics",
    "531770282580668421": "Design & Creative",
    "531770282584862722": "Engineering & Architecture",
    "531770282580668419": "IT & Networking",
    "531770282584862723": "Legal",
    "531770282580668422": "Sales & Marketing",
    "531770282584862720": "Translation",
    "531770282580668418": "Web, Mobile & Software Dev",
    "531770282580668423": "Writing",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    print(f"User {update.message.chat_id} started the bot")
    await show_main_menu(update)

async def show_main_menu(update: Update) -> None:
    """Display the main menu"""
    print("Displaying main menu")
    keyboard = [
        [InlineKeyboardButton("Create New Alert", callback_data='menu_new_alert')],
        [InlineKeyboardButton("List Alerts", callback_data='menu_list_alerts')],
        [InlineKeyboardButton("Delete Alert", callback_data='menu_delete_alert')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Main Menu:", reply_markup=reply_markup)

async def handle_main_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle selections from the main menu"""
    query = update.callback_query
    await query.answer()
    print(f"Main menu selection by user {query.message.chat_id}: {query.data}")

    if query.data == 'menu_new_alert':
        await setup_new_alert(query)
    elif query.data == 'menu_list_alerts':
        await list_user_alerts(query)
    elif query.data == 'menu_delete_alert':
        await delete_alert_selection(query)

async def setup_new_alert(query) -> None:
    """Initialize a new alert setup"""
    user_id = query.message.chat_id
    print(f"User {user_id} is setting up a new alert")
    user_alerts[user_id] = {'data': {}}
    await show_alert_menu(query)

async def show_alert_menu(query) -> None:
    """Show the alert setup menu"""
    user_id = query.message.chat_id
    print(f"Showing alert setup menu to user {user_id}")
    keyboard = [
        [InlineKeyboardButton("Experience Level", callback_data='set_experience')],
        [InlineKeyboardButton("Category", callback_data='set_category')],
        [InlineKeyboardButton("Job Type", callback_data='set_job_type')],
        [InlineKeyboardButton("Hourly Rate / Fixed Price", callback_data='set_amount')],
        [InlineKeyboardButton("Client History", callback_data='set_client_history')],
        [InlineKeyboardButton("Contract-to-Hire", callback_data='set_contract_to_hire')],
        [InlineKeyboardButton("Payment Verification", callback_data='set_payment_verified')],
        [InlineKeyboardButton("Proposals Range", callback_data='set_proposals')],
        [InlineKeyboardButton("Search Keywords", callback_data='set_keywords')],
        [InlineKeyboardButton("Confirm & Save", callback_data='confirm_alert')],
        [InlineKeyboardButton("Cancel Alert Setup", callback_data='cancel_alert')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Choose an option to configure your alert:", reply_markup=reply_markup)

async def handle_alert_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle selections from the alert setup menu"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    selection = query.data
    print(f"User {user_id} selected alert menu option: {selection}")

    # Handle each selection
    if selection == 'set_experience':
        await ask_experience_level(query)
    elif selection == 'set_category':
        await ask_category(query)
    elif selection == 'set_job_type':
        await ask_job_type(query)
    elif selection == 'set_amount':
        await ask_amount(query)
    elif selection == 'set_client_history':
        await ask_client_history(query)
    elif selection == 'set_contract_to_hire':
        await ask_contract_to_hire(query)
    elif selection == 'set_payment_verified':
        await ask_payment_verification(query)
    elif selection == 'set_proposals':
        await ask_proposals_range(query)
    elif selection == 'set_keywords':
        await ask_keywords(query)
    elif selection == 'confirm_alert':
        await confirm_alert(query)
    elif selection == 'cancel_alert':
        user_alerts.pop(user_id, None)
        await query.message.edit_text("Alert setup has been canceled.")
    elif selection == 'back_to_main_menu':
        await show_main_menu(update)

# Function to ask for experience level
async def ask_experience_level(query) -> None:
    print(f"Asking user {query.message.chat_id} for experience level")
    keyboard = [
        [InlineKeyboardButton("Entry Level", callback_data='experience_1')],
        [InlineKeyboardButton("Intermediate", callback_data='experience_2')],
        [InlineKeyboardButton("Expert", callback_data='experience_3')],
        [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Select experience level (choose multiple):", reply_markup=reply_markup)

async def handle_experience_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle selection of experience levels"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        experience_level = query.data.split('_')[1]
        user_alerts[user_id]['data'].setdefault('contractor_tier', []).append(experience_level)
        print(f"User {user_id} added experience level {experience_level}")

async def ask_category(query) -> None:
    """Ask user to select a category"""
    print(f"Asking user {query.message.chat_id} for category")
    keyboard = [[InlineKeyboardButton(name, callback_data=f'category_{key}')] for key, name in categories.items()]
    keyboard.append([InlineKeyboardButton("Back to Menu", callback_data='alert_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Select a category:", reply_markup=reply_markup)

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle category selection"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        category_id = query.data.split('_')[1]
        user_alerts[user_id]['data']['category'] = category_id
        print(f"User {user_id} selected category {category_id}")

async def ask_job_type(query) -> None:
    """Ask user to select job type"""
    print(f"Asking user {query.message.chat_id} for job type")
    keyboard = [
        [InlineKeyboardButton("Hourly", callback_data='jobtype_hourly')],
        [InlineKeyboardButton("Fixed Price", callback_data='jobtype_fixed')],
        [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Select job type:", reply_markup=reply_markup)

async def handle_job_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle job type selection"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        job_type = query.data.split('_')[1]
        user_alerts[user_id]['data']['t'] = 0 if job_type == 'hourly' else 1
        print(f"User {user_id} selected job type: {job_type}")
        await ask_amount(query)

async def ask_amount(query) -> None:
    """Ask for hourly rate or fixed-price amount"""
    user_id = query.message.chat_id
    if user_alerts[user_id]['data'].get('t') == 0:  # Hourly
        await query.message.edit_text("Enter hourly rate range in format 'min-max' (e.g., 10-20):")
    else:  # Fixed price
        keyboard = [
            [InlineKeyboardButton("Less than $100", callback_data='amount_0-99')],
            [InlineKeyboardButton("$100 to $500", callback_data='amount_100-499')],
            [InlineKeyboardButton("$500 - $1K", callback_data='amount_500-999')],
            [InlineKeyboardButton("$1K - $5K", callback_data='amount_1000-4999')],
            [InlineKeyboardButton("$5K+", callback_data='amount_5000-')],
            [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Select fixed-price range:", reply_markup=reply_markup)

async def handle_amount_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle amount selection"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        amount_range = query.data.split('_')[1]
        user_alerts[user_id]['data']['amount'] = amount_range
        print(f"User {user_id} selected amount range {amount_range}")

async def ask_client_history(query) -> None:
    """Ask user for client history"""
    print(f"Asking user {query.message.chat_id} for client history")
    keyboard = [
        [InlineKeyboardButton("No hires", callback_data='client_hires_0')],
        [InlineKeyboardButton("1 to 9 hires", callback_data='client_hires_1-9')],
        [InlineKeyboardButton("10+ hires", callback_data='client_hires_10+')],
        [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Select client history:", reply_markup=reply_markup)

async def handle_client_history_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle client history selection"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        client_hires = query.data.split('_')[1]
        user_alerts[user_id]['data']['client_hires'] = client_hires
        print(f"User {user_id} selected client hires {client_hires}")

async def ask_contract_to_hire(query) -> None:
    """Ask user if the job is contract-to-hire"""
    print(f"Asking user {query.message.chat_id} if contract-to-hire")
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='contract_to_hire_1')],
        [InlineKeyboardButton("No", callback_data='contract_to_hire_0')],
        [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Is this a contract-to-hire role?", reply_markup=reply_markup)

async def handle_contract_to_hire(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle contract-to-hire selection"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        contract_to_hire = query.data.split('_')[1]
        user_alerts[user_id]['data']['contract_to_hire'] = contract_to_hire
        print(f"User {user_id} selected contract-to-hire: {contract_to_hire}")

async def ask_payment_verification(query) -> None:
    """Ask user if payment verification is required"""
    print(f"Asking user {query.message.chat_id} for payment verification requirement")
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='payment_verified_1')],
        [InlineKeyboardButton("No", callback_data='payment_verified_0')],
        [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Require payment verification?", reply_markup=reply_markup)

async def handle_payment_verification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle payment verification selection"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        payment_verified = query.data.split('_')[1]
        user_alerts[user_id]['data']['payment_verified'] = payment_verified
        print(f"User {user_id} selected payment verification: {payment_verified}")

async def ask_proposals_range(query) -> None:
    """Ask user for proposals range"""
    print(f"Asking user {query.message.chat_id} for proposal range")
    keyboard = [
        [InlineKeyboardButton("0-4", callback_data='proposals_0-4')],
        [InlineKeyboardButton("5-9", callback_data='proposals_5-9')],
        [InlineKeyboardButton("10+", callback_data='proposals_10+')],
        [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text("Select proposal range:", reply_markup=reply_markup)

async def handle_proposals_range_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle proposals range selection"""
    query = update.callback_query
    await query.answer()
    user_id = query.message.chat_id
    if query.data == 'alert_menu':
        await show_alert_menu(query)
    else:
        proposals = query.data.split('_')[1]
        user_alerts[user_id]['data']['proposals'] = proposals
        print(f"User {user_id} selected proposals range: {proposals}")

async def ask_keywords(query) -> None:
    """Ask user for search keywords"""
    print(f"Asking user {query.message.chat_id} for search keywords")
    await query.message.edit_text("Enter search keywords (optional):")

async def confirm_alert(query) -> None:
    """Confirm alert settings before saving"""
    user_id = query.message.chat_id
    alert_data = user_alerts.get(user_id, {}).get('data', {})
    summary = f"Your alert settings:\n{alert_data}"
    keyboard = [
        [InlineKeyboardButton("Confirm", callback_data='save_alert')],
        [InlineKeyboardButton("Back to Menu", callback_data='alert_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(summary, reply_markup=reply_markup)

async def handle_save_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save the alert"""
    query = update.callback_query
    user_id = query.message.chat_id
    alert_data = user_alerts.get(user_id, {}).get('data', {})
    add_alert(user_id, alert_data)
    user_alerts.pop(user_id, None)
    await query.message.edit_text("Alert saved successfully!")

async def list_user_alerts(query) -> None:
    """List all alerts for the user"""
    user_id = query.message.chat_id
    alerts = list_alerts(user_id)
    if alerts:
        alert_messages = "\n".join([f"ID: {alert['id']}, Filters: {alert['filters']}" for alert in alerts])
        await query.message.edit_text(f"Your alerts:\n{alert_messages}")
    else:
        await query.message.edit_text("You have no saved alerts.")

async def delete_alert_selection(query) -> None:
    """Delete an alert"""
    user_id = query.message.chat_id
    alerts = list_alerts(user_id)
    if alerts:
        keyboard = [[InlineKeyboardButton(f"Delete ID {alert['id']}", callback_data=f'delete_{alert["id"]}')] for alert in alerts]
        keyboard.append([InlineKeyboardButton("Back to Menu", callback_data='alert_menu')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Select an alert to delete:", reply_markup=reply_markup)
    else:
        await query.message.edit_text("You have no alerts to delete.")

async def handle_delete_alert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle alert deletion"""
    query = update.callback_query
    await query.answer()
    alert_id = query.data.split('_')[1]
    delete_alert(alert_id)
    await query.message.edit_text(f"Alert ID {alert_id} has been deleted.")

def main():
    """Main function to run the bot"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", show_main_menu))
    application.add_handler(CallbackQueryHandler(handle_main_menu_selection, pattern='^menu_'))
    application.add_handler(CallbackQueryHandler(handle_alert_menu_selection, pattern='^set_'))
    application.add_handler(CallbackQueryHandler(handle_experience_selection, pattern='^experience_|alert_menu'))
    application.add_handler(CallbackQueryHandler(handle_category_selection, pattern='^category_|alert_menu'))
    application.add_handler(CallbackQueryHandler(handle_job_type_selection, pattern='^jobtype_|alert_menu'))
    application.add_handler(CallbackQueryHandler(handle_amount_selection, pattern='^amount_|alert_menu'))
    application.add_handler(CallbackQueryHandler(handle_client_history_selection, pattern='^client_hires_|alert_menu'))
    application.add_handler(CallbackQueryHandler(handle_delete_alert, pattern='^delete_'))
    
    application.run_polling()

if __name__ == '__main__':
    main()
