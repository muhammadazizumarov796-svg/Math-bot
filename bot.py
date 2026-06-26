import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.com")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"Salom, {user.first_name}! 👋\n\n"
        "🧮 *MathAI Bot*ga xush kelibsiz!\n\n"
        "Men sizga matematik misollarni yechishda yordam beraman.\n"
        "Quyidagi bo'limlardan birini tanlang:\n\n"
        "📚 *Yo'nalish olish* — Maslahat va yechish usulini olish\n"
        "✅ *Ishlab berish* — Bosqichma-bosqich to'liq yechim\n"
        "🔍 *Xatoni topish* — Yechimingizni tekshirish"
    )
    keyboard = [
        [InlineKeyboardButton("📚 Yo'nalish olish", web_app=WebAppInfo(url=f"{WEBAPP_URL}?mode=yordam"))],
        [InlineKeyboardButton("✅ Ishlab berish", web_app=WebAppInfo(url=f"{WEBAPP_URL}?mode=yechish"))],
        [InlineKeyboardButton("🔍 Xatoni topib tushuntirish", web_app=WebAppInfo(url=f"{WEBAPP_URL}?mode=xato"))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *Yordam*\n\n"
        "Bot qanday ishlaydi:\n\n"
        "1️⃣ Quyidagi tugmalardan birini bosing\n"
        "2️⃣ Ochilgan oynada matematik misol rasmini yuklang\n"
        "3️⃣ 'Yuborish' tugmasini bosing\n"
        "4️⃣ AI natijani ko'rsatadi\n\n"
        "📚 *Yo'nalish olish* — Misol qanday yechilishini tushuntiradi\n"
        "✅ *Ishlab berish* — To'liq yechimni ko'rsatadi\n"
        "🔍 *Xato topish* — Sizning yechimingizni tekshiradi\n\n"
        "/start — Bosh menyu"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Xato: {context.error}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)
    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
