import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '8938472378:AAEt8MbbEq2_JgChTkJUJTktc8ZOQpYMYWo'

USER_STATE = {}
USER_BALANCES = {}
USER_ORDERS = {}

# ዋናው ሜኑ (ሁሉም አዝራሮች ወደ ታች የተደረደሩ)
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛒 Items", callback_data='menu_items')],
        [InlineKeyboardButton("💰 My Balance", callback_data='menu_balance')],
        [InlineKeyboardButton("📦 My Orders", callback_data='menu_orders')],
        [InlineKeyboardButton("📢 Our Channel", url="https://t.me/zenixtopup1")],
        [InlineKeyboardButton("🎧 Contact Support", url="https://t.me/zenixtopup1")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        user_id = user.id
        
        if user_id not in USER_BALANCES:
            USER_BALANCES[user_id] = 0.0

        user_display = f"@{user.username}" if user.username else user.first_name

        welcome_text = (
            f"✨ **Welcome to Zenix Top-Up Bot, {user_display}!** ✨\n\n"
            "⚡ **Fast & Automated Game Top-Up Service**\n\n"
            "Please select an option from the menu below:"
        )
        
        reply_markup = get_main_menu_keyboard()
        
        try:
            with open('welcome.jpg', 'rb') as photo_file:
                await update.message.reply_photo(
                    photo=photo_file,
                    caption=welcome_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        except FileNotFoundError:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in start: {e}")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        user = query.from_user
        user_id = user.id
        await query.answer()

        telegram_name = f"@{user.username}" if user.username else user.first_name

        if query.data == 'menu_items':
            keyboard = [
                [InlineKeyboardButton("🔥 Free Fire", callback_data='game_ff')],
                [InlineKeyboardButton("⚡ PUBG Mobile", callback_data='game_pubg')],
                [InlineKeyboardButton("💣 Call of Duty (CP)", callback_data='game_codm')],
                [InlineKeyboardButton("🎯 Blood Strike", callback_data='game_bs')],
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]
            ]
            await query.message.reply_text("🛒 Select a game to view available packages:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif query.data == 'menu_balance':
            balance = USER_BALANCES.get(user_id, 0.0)
            balance_text = (
                f"👤 **Telegram User:**\n{telegram_name}\n\n"
                f"🆔 **Telegram ID:**\n`{user_id}`\n\n"
                f"💳 **My Balance:**\n`{balance:.2f} ETB`\n\n"
                f"─────────────────\n"
                f"To deposit funds into your account, please contact support."
            )
            keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]]
            await query.message.reply_text(balance_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

        elif query.data == 'menu_orders':
            orders = USER_ORDERS.get(user_id, [])
            if not orders:
                orders_text = f"📦 **My Orders ({telegram_name}):**\n\nYou have no previous orders yet."
            else:
                orders_text = f"📦 **Order History for {telegram_name}:**\n\n"
                for idx, order in enumerate(orders, 1):
                    orders_text += (
                        f"**{idx}. Game:** {order['game']}\n"
                        f"• **Package:** {order['package']}\n"
                        f"• **ID:** `{order['id']}`\n"
                        f"• **Status:** ⏳ Processing\n"
                        f"─────────────────\n"
                    )

            keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='main_menu')]]
            await query.message.reply_text(orders_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

        elif query.data == 'main_menu':
            welcome_text = f"✨ **Welcome to Zenix Top-Up Bot, {telegram_name}!** ✨\n\nPlease select an option below:"
            await query.message.reply_text(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode='Markdown')

        # 1. Free Fire Packages & Prices
        elif query.data == 'game_ff':
            keyboard = [
                [InlineKeyboardButton("💎 110 Diamonds - 150 ETB", callback_data='pkg_Free Fire_110 Diamonds (150 ETB)')],
                [InlineKeyboardButton("💎 231 Diamonds - 300 ETB", callback_data='pkg_Free Fire_231 Diamonds (300 ETB)')],
                [InlineKeyboardButton("💎 583 Diamonds - 750 ETB", callback_data='pkg_Free Fire_583 Diamonds (750 ETB)')],
                [InlineKeyboardButton("💎 1080 Diamonds - 1350 ETB", callback_data='pkg_Free Fire_1080 Diamonds (1350 ETB)')],
                [InlineKeyboardButton("💎 2200 Diamonds - 2650 ETB", callback_data='pkg_Free Fire_2200 Diamonds (2650 ETB)')],
                [InlineKeyboardButton("📅 Weekly Membership - 250 ETB", callback_data='pkg_Free Fire_Weekly Membership (250 ETB)')],
                [InlineKeyboardButton("📆 Monthly Membership - 1000 ETB", callback_data='pkg_Free Fire_Monthly Membership (1000 ETB)')],
                [InlineKeyboardButton("🔙 Back to Items", callback_data='menu_items')]
            ]
            await query.message.reply_text("Select your Free Fire Diamond package:", reply_markup=InlineKeyboardMarkup(keyboard))

        # 2. PUBG Mobile Packages & Prices
        elif query.data == 'game_pubg':
            keyboard = [
                [InlineKeyboardButton("⚡ 60 UC - 160 ETB", callback_data='pkg_PUBG Mobile_60 UC (160 ETB)')],
                [InlineKeyboardButton("⚡ 325 UC - 750 ETB", callback_data='pkg_PUBG Mobile_325 UC (750 ETB)')],
                [InlineKeyboardButton("⚡ 660 UC - 1450 ETB", callback_data='pkg_PUBG Mobile_660 UC (1450 ETB)')],
                [InlineKeyboardButton("🔙 Back to Items", callback_data='menu_items')]
            ]
            await query.message.reply_text("Select your PUBG Mobile UC package:", reply_markup=InlineKeyboardMarkup(keyboard))

        # 3. Call of Duty Packages & Prices
        elif query.data == 'game_codm':
            keyboard = [
                [InlineKeyboardButton("💣 80 CP - 180 ETB", callback_data='pkg_Call of Duty_80 CP (180 ETB)')],
                [InlineKeyboardButton("💣 420 CP - 850 ETB", callback_data='pkg_Call of Duty_420 CP (850 ETB)')],
                [InlineKeyboardButton("💣 880 CP - 1700 ETB", callback_data='pkg_Call of Duty_880 CP (1700 ETB)')],
                [InlineKeyboardButton("🔙 Back to Items", callback_data='menu_items')]
            ]
            await query.message.reply_text("Select your Call of Duty CP package:", reply_markup=InlineKeyboardMarkup(keyboard))

        # 4. Blood Strike Packages & Prices
        elif query.data == 'game_bs':
            keyboard = [
                [InlineKeyboardButton("🎯 100 Gold - 150 ETB", callback_data='pkg_Blood Strike_100 Gold (150 ETB)')],
                [InlineKeyboardButton("🎯 500 Gold - 700 ETB", callback_data='pkg_Blood Strike_500 Gold (700 ETB)')],
                [InlineKeyboardButton("🎯 1000 Gold - 1350 ETB", callback_data='pkg_Blood Strike_1000 Gold (1350 ETB)')],
                [InlineKeyboardButton("🔙 Back to Items", callback_data='menu_items')]
            ]
            await query.message.reply_text("Select your Blood Strike Gold package:", reply_markup=InlineKeyboardMarkup(keyboard))

        elif query.data.startswith('pkg_'):
            details = query.data.split('_')
            game_name = details[1]
            amount = details[2]
            
            if game_name == "Free Fire":
                id_type = "Free Fire Player ID (UID)"
            elif game_name == "PUBG Mobile":
                id_type = "PUBG Character ID"
            elif game_name == "Call of Duty":
                id_type = "CODM Player ID / Activision ID"
            elif game_name == "Blood Strike":
                id_type = "Blood Strike User ID"
            else:
                id_type = "Player ID"

            USER_STATE[user_id] = {
                'game': game_name,
                'package': amount,
                'id_type': id_type,
                'step': 'WAITING_FOR_PLAYER_ID'
            }
            
            await query.message.reply_text(
                f"🎮 **Game:** {game_name}\n"
                f"📦 **Package:** {amount}\n\n"
                f"Please enter your **{id_type}** (Must be between 8 and 12 digits):",
                parse_mode='Markdown'
            )
    except Exception as e:
        logging.error(f"Error in button_click: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.message.from_user
        user_id = user.id
        text_input = update.message.text.strip()
        telegram_name = f"@{user.username}" if user.username else user.first_name

        if user_id in USER_STATE and USER_STATE[user_id].get('step') == 'WAITING_FOR_PLAYER_ID':
            if not text_input.isdigit() or len(text_input) < 8 or len(text_input) > 12:
                await update.message.reply_text(
                    "❌ **Invalid Player ID!**\n\n"
                    "Please enter a valid Player ID (Only numbers, between 8 and 12 digits long):",
                    parse_mode='Markdown'
                )
                return

            player_id = text_input
            game = USER_STATE[user_id]['game']
            package = USER_STATE[user_id]['package']
            id_type = USER_STATE[user_id]['id_type']
            
            if user_id not in USER_ORDERS:
                USER_ORDERS[user_id] = []
                
            USER_ORDERS[user_id].append({
                'game': game,
                'package': package,
                'id': player_id
            })
            
            del USER_STATE[user_id]

            reply_markup = get_main_menu_keyboard()
            
            await update.message.reply_text(
                f"📥 **Order Received!**\n\n"
                f"• **User:** {telegram_name}\n"
                f"• **Game:** {game}\n"
                f"• **Package & Price:** {package}\n"
                f"• **{id_type}:** `{player_id}`\n\n"
                f"Your order is currently being processed. You can view it under **My Orders**.",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logging.error(f"Error in handle_message: {e}")

async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running successfully...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    # ቦቱ ፈፅሞ እንዳይዘጋ የሚያደርገው ጥበቃ (Infinity Loop)
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(run_bot())
    except Exception as e:
        logging.error(f"Error: {e}")
