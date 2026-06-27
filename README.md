# 📚 Test Bot — Telegram Test Ishlash Tizimi

Matematika (va kelajakda boshqa fanlar) bo'yicha test ishlash imkonini beruvchi
Telegram bot. Barcha menyu, fan, bo'lim va testlar **admin panel orqali**
boshqariladi — kodga hech narsa qattiq yozilmagan.

## 🧱 Arxitektura

```
testbot/
├── app/
│   ├── core/
│   │   ├── config.py        # .env dan sozlamalar
│   │   ├── database.py      # Async SQLAlchemy engine/session
│   │   └── models.py        # Barcha jadvallar (User, Section, Test, ...)
│   ├── bot/
│   │   ├── main.py          # Botni ishga tushiruvchi fayl
│   │   ├── keyboards.py     # Dinamik inline klaviaturalar
│   │   ├── middlewares.py   # Har bir update'ga DB session ulash
│   │   └── handlers/
│   │       ├── user.py      # /start, menyu navigatsiyasi
│   │       └── admin.py     # Fanlar/bo'limlar CRUD, statistika, xabarnoma
│   ├── webapp/
│   │   ├── api.py           # Test ishlash API (start/submit/leaderboard)
│   │   ├── admin_api.py     # Test/savol CRUD API (admin uchun)
│   │   ├── security.py      # Telegram initData tekshiruvi (HMAC)
│   │   ├── schemas.py       # Pydantic sxemalari
│   │   └── static/index.html # Web App frontend (vanilla JS)
│   └── main.py              # FastAPI ilovasi
├── requirements.txt
└── .env.example
```

## ⚙️ O'rnatish

1. **PostgreSQL** o'rnating va bo'sh baza yarating:
   ```bash
   createdb testbot_db
   ```

2. **.env** faylini yarating:
   ```bash
   cp .env.example .env
   # BOT_TOKEN, ADMIN_IDS, DATABASE_URL, WEBAPP_URL ni to'ldiring
   ```

3. **Kutubxonalarni o'rnatish:**
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Web App uchun HTTPS domen kerak** (Telegram talabi). Lokal test uchun
   [ngrok](https://ngrok.com) yoki shunga o'xshash tunnel ishlatish mumkin:
   ```bash
   ngrok http 8000
   # chiqqan https:// manzilni .env dagi WEBAPP_URL ga yozing
   ```

5. **Ishga tushirish** (ikkita alohida jarayon):
   ```bash
   # 1-terminal: FastAPI (Web App backend)
   uvicorn app.main:app --host 0.0.0.0 --port 8000

   # 2-terminal: Telegram bot
   python -m app.bot.main
   ```

## 🛠 Admin bilan ishlash (Telegram orqali)

| Buyruq | Vazifasi |
|---|---|
| `/admin` | Admin panel menyusi |
| `/add_section` | Yangi fan qo'shish (nom + ikonka so'raladi) |
| `/list_sections` | Fanlarni ko'rish, yoqish/o'chirish, tartibini almashtirish |
| `/add_subsection` | Fanga ichki bo'lim qo'shish (Algebra, DTM, ...) |
| `/broadcast` | Barcha foydalanuvchilarga xabar (matn/rasm/video/hujjat) — fon rejimida yuboriladi |
| `/stats` | To'liq statistika |

**Testlar va savollar** esa `app/webapp/admin_api.py` orqali (masalan, alohida
admin web sahifasi yoki Postman/skript yordamida) qo'shiladi — chunki bir nechta
variant, rasm va izoh kiritish uchun shakl interfeysi ancha qulayroq. Misol:

```bash
curl -X POST https://yourdomain.com/api/admin/tests \
  -H "X-Telegram-Init-Data: <admin_telegram_initdata>" \
  -H "Content-Type: application/json" \
  -d '{
    "sub_section_id": 1,
    "title": "Algebra — 1-mavzu",
    "time_limit_minutes": 10,
    "questions": [
      {
        "text": "2 + 2 = ?",
        "explanation": "Oddiy qo'shish amali.",
        "options": [
          {"text": "3", "is_correct": false},
          {"text": "4", "is_correct": true},
          {"text": "5", "is_correct": false},
          {"text": "6", "is_correct": false}
        ]
      }
    ]
  }'
```

> 💡 Keyinroq shu API ustiga to'liq grafik admin-panel (masalan, React yoki
> oddiy HTML forma) qo'shish juda oson — backend allaqachon tayyor.

## 🔐 Xavfsizlik

- Web App'dan kelgan har bir so'rov `X-Telegram-Init-Data` header orqali
  HMAC-SHA256 imzosi bilan tekshiriladi (`security.py`) — soxta foydalanuvchi
  nomidan test yechib bo'lmaydi.
- To'g'ri javoblar hech qachon frontendga test boshlanishida yuborilmaydi —
  faqat test tugagandan keyin qaytariladi.
- Vaqt serverda qattiq nazorat qilinadi — frontend taymerini "hack" qilib
  ko'proq vaqt olib bo'lmaydi.
- Admin endpointlari `ADMIN_IDS` ro'yxati bilan cheklangan.

## ➕ Yangi fan qo'shish qanchalik oson?

Hech qanday kod o'zgartirilmaydi:
1. Botda `/add_section` → nom va ikonka kiritiladi.
2. `/add_subsection` → shu fanga ichki bo'limlar qo'shiladi.
3. Admin API orqali testlar/savollar kiritiladi.

Bot menyusi avtomatik yangilanadi, chunki klaviaturalar har doim
bazadan (`keyboards.py`) dinamik tarzda quriladi.

## 🧩 Kengaytirish g'oyalari

- Savollarni Excel'dan import qilish uchun `/import_questions` buyrug'i.
- Telegram orqali rasm yuklash va uni statik serverga saqlash (`image_url`).
- Redis orqali tezroq leaderboard keshlash (foydalanuvchi soni ortganda).
- Alembic migratsiyalarini ulash (`init_models()` o'rniga production uchun).
