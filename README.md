# ════════════════════════════════════════
#  MathAI Bot — O'rnatish va Ishga Tushurish
# ════════════════════════════════════════

## 📁 Fayl tuzilmasi
```
math-bot/
├── bot.py           ← Telegram bot
├── server.py        ← FastAPI backend
├── requirements.txt ← Python kutubxonalari
├── .env             ← Sozlamalar (o'zingiz yaratasiz)
└── static/
    └── index.html   ← Telegram Web App frontend
```

## ⚙️ 1-qadam: .env fayli yarating
```env
BOT_TOKEN=7xxxxxxxxx:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx
WEBAPP_URL=https://sizning-domeningiz.com
```

## 📦 2-qadam: Kutubxonalarni o'rnating
```bash
pip install -r requirements.txt
```

## 🤖 3-qadam: Telegram botni sozlang

### BotFather orqali:
1. @BotFather ga yozing → /newbot
2. Bot nomini bering (masalan: MathAI_uz_bot)
3. Token oling → .env ga qo'ying
4. /setmenubutton → Web App URL ni bering (ixtiyoriy)

## 🌐 4-qadam: Serverni ishga tushiring

### Variant A — Localhost (test uchun)
```bash
# ngrok orqali HTTPS tunnel (test uchun)
pip install pyngrok
# Yoki: ngrok http 8000

# Serverni ishga tushiring
python server.py
```

### Variant B — Production (render.com / railway.app)
```bash
# Render.com da:
# 1. GitHub ga push qiling
# 2. render.com da "New Web Service" yarating
# 3. Environment variables ga BOT_TOKEN va ANTHROPIC_API_KEY qo'ying
# 4. Start command: uvicorn server:app --host 0.0.0.0 --port $PORT

# Railway.app da:
# railway up
```

## 🚀 5-qadam: Botni ishga tushiring
```bash
# Alohida terminal oynasida:
python bot.py
```

## 🔧 Tekshirish

Server ishlaydimi:
```
GET https://sizning-domeningiz.com/health
→ {"status":"ok","message":"MathAI API ishlayapti"}
```

Web App ochilish:
```
https://sizning-domeningiz.com/?mode=yordam
https://sizning-domeningiz.com/?mode=yechish
https://sizning-domeningiz.com/?mode=xato
```

## 🐛 Keng tarqalgan muammolar

| Muammo | Yechim |
|--------|--------|
| Web App ochilmaydi | WEBAPP_URL HTTPS bo'lishi kerak |
| Bot javob bermaydi | BOT_TOKEN to'g'ri ekanini tekshiring |
| AI xato qaytaradi | ANTHROPIC_API_KEY ni tekshiring |
| Rasm yuklanmaydi | Rasm 10MB dan kichik bo'lsin |
