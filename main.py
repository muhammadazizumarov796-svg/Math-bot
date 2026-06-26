import os
import asyncio
import threading
import base64
import io
import google.generativeai as genai

from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes


# ── CONFIG ──
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://math-bot-production.up.railway.app")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# ── FASTAPI ──
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# NOTE: keep your original HTML_CONTENT unchanged and paste it here
HTML_CONTENT = """PASTE_YOUR_EXISTING_HTML_CONTENT_HERE"""

SYSTEM_PROMPTS = {
    "yordam": """Siz tajribali o'zbek matematik o'qituvchisiz. Faqat yo'nalish bering, to'liq yechim bermang.""",
    "yechish": """Misolni bosqichma-bosqich to'liq yeching.""",
    "xato": """Xatolarni toping va tushuntiring."""
}


class AnalyzeRequest(BaseModel):
    image_base64: str
    mode: str
    user_solution: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT


@app.post("/api/analyze")
async def analyze_image(request: AnalyzeRequest):
    if request.mode not in SYSTEM_PROMPTS:
        raise HTTPException(status_code=400, detail="Noto'g'ri rejim")

    try:
        image_data = request.image_base64
        if "," in image_data:
            image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        prompt = {
            "yordam": "Maslahat ber.",
            "yechish": "To'liq yech.",
            "xato": f"Xatolarni top. {request.user_solution or ''}"
        }[request.mode]

        response = model.generate_content([
            SYSTEM_PROMPTS[request.mode],
            image,
            prompt
        ])

        return {"success": True, "result": response.text, "mode": request.mode}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Yo'nalish", web_app=WebAppInfo(url=f"{WEBAPP_URL}?mode=yordam"))],
        [InlineKeyboardButton("✅ Yechish", web_app=WebAppInfo(url=f"{WEBAPP_URL}?mode=yechish"))],
        [InlineKeyboardButton("🔍 Xato", web_app=WebAppInfo(url=f"{WEBAPP_URL}?mode=xato"))],
    ]

    await update.message.reply_text(
        "Salom! 🧮 Math bot",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def run_bot():
    async def _run():
        bot_app = Application.builder().token(BOT_TOKEN).build()
        bot_app.add_handler(CommandHandler("start", start))
        await bot_app.initialize()
        await bot_app.start()
        await bot_app.updater.start_polling()
        await asyncio.Event().wait()

    asyncio.run(_run())


@app.on_event("startup")
async def startup():
    if BOT_TOKEN:
        threading.Thread(target=run_bot, daemon=True).start()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
