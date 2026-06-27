# 🚀 GitHub'ga joylash — oddiy yo'riqnoma

Bu loyihani GitHub'ga yuklash juda oson. Quyidagi qadamlarni ketma-ket bajaring.

## 1. GitHub'da bo'sh repository yarating

1. https://github.com/new ga kiring
2. Repository nomini kiriting, masalan: `test-bot`
3. **"Add a README"** belgisini QO'YMANG (bizda allaqachon bor)
4. **Create repository** tugmasini bosing
5. Ochilgan sahifadan repo manzilini ko'chirib oling, masalan:
   `https://github.com/USERNAME/test-bot.git`

## 2. Loyihani kompyuteringizga oching

`testbot.zip` faylini istalgan papkaga ochib oling (masalan, ish stoliga),
so'ng terminal/buyruqlar qatorini shu papka ichida oching.

## 3. Quyidagi buyruqlarni ketma-ket bajaring

```bash
cd testbot

git init
git add .
git commit -m "Birinchi commit: Test Bot loyihasi"
git branch -M main
git remote add origin https://github.com/USERNAME/test-bot.git
git push -u origin main
```

> ⚠️ `USERNAME/test-bot` o'rniga o'zingizning GitHub manzilingizni yozing.

Shu bilan loyiha GitHub'da tayyor bo'ladi ✅

## 4. ⚠️ MUHIM — maxfiy ma'lumotlarni hech qachon yuklamang

`.env` fayli (BOT_TOKEN, DATABASE_URL kabi maxfiy ma'lumotlar) `.gitignore`
fayli orqali avtomatik chiqarib tashlanadi — u GitHub'ga yuklanmaydi.

Repo'da faqat `.env.example` (namuna, bo'sh qiymatlar bilan) qoladi — bu xavfsiz.

Tekshirish uchun:
```bash
git status
```
Bu yerda `.env` fayli ko'rinmasligi kerak. Agar ko'rinsa — `push` qilishdan
oldin albatta to'xtatib, `.gitignore` faylini tekshiring.

## 5. Keyinchalik yangilik kiritsangiz

```bash
git add .
git commit -m "O'zgartirish tavsifi"
git push
```

## 6. Serverga (production) joylash

Server (VPS) ga GitHub orqali yuklash uchun serverda:

```bash
git clone https://github.com/USERNAME/test-bot.git
cd test-bot
cp .env.example .env
nano .env          # haqiqiy BOT_TOKEN, ADMIN_IDS, DATABASE_URL kiritiladi
pip install -r requirements.txt
```

Keyin botni va serverni doimiy ishlashi uchun `systemd` yoki `screen`/`tmux`
yoki `pm2`/`supervisor` orqali ishga tushirish tavsiya etiladi:

```bash
# Bot
python -m app.bot.main

# Web App backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 7. (Ixtiyoriy) GitHub Actions bilan avtomatik deploy

Agar xohlasangiz, push qilingan har safar serverga avtomatik joylashtiruvchi
CI/CD (`.github/workflows/deploy.yml`) ham yozib berishim mumkin — shunda
`git push` qilganingizda sayt/bot o'zi yangilanadi. Aytsangiz, shuni ham
qo'shib beraman.
