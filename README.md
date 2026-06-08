# 🐡 Puffer Coin Community Bot

An automated Telegram community bot powered by **Google Gemini API (FREE)**.
Posts every 1–2 hours with 14 rotating content types to keep your community alive 24/7.

## What It Posts
- 🐡 Puffer Coin launch hype (every 3rd post, 14 different angles)
- 📰 Breaking crypto news
- 📊 Memecoin price updates (DOGE, SHIB, PEPE, FLOKI, BONK, WIF...)
- 😂 Funny relatable trading moments
- 🔥 Trending coins roundup
- 💬 Community engagement questions
- 🌅 GM hype posts
- 🎯 Bold market predictions
- 💡 Trading wisdom & tips
- 🤡 Degen confessions
- 🐦 Viral tweet-style posts
- 🎲 Would You Rather crypto questions
- 📅 Weekly recap posts
- 📡 Market vibe checks

---

## STEP 1 — Get Your Gemini API Key (FREE)

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key — looks like: `AIzaSy...`

---

## STEP 2 — Create Your Telegram Bot

1. Open Telegram, search for **@BotFather**
2. Send: `/newbot`
3. Give it a name: e.g. `Puffer Coin Bot`
4. Give it a username: e.g. `PufferCoinBot`
5. BotFather gives you a token like: `7123456789:AAF...`
6. Copy that token

---

## STEP 3 — Get Your Telegram Chat ID

1. Add your bot to your Telegram group as an **Admin**
2. Go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   (replace `<YOUR_TOKEN>` with your actual bot token)
3. Send any message in your group
4. Refresh that URL — find `"chat":{"id":` in the result
5. Copy that number (it will be negative for groups, e.g. `-1001234567890`)

---

## STEP 4 — Upload to GitHub

1. Create a free account at https://github.com
2. Click **"New Repository"**
3. Name it: `puffer-coin-bot`
4. Set to **Private**
5. Upload these 3 files:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`

---

## STEP 5A — Deploy on Railway (Recommended)

1. Go to https://railway.app and sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `puffer-coin-bot` repo
4. Go to **Variables** tab and add these 3 variables:

| Variable Name | Value |
|---|---|
| `TELEGRAM_TOKEN` | Your BotFather token |
| `TELEGRAM_CHAT_ID` | Your group chat ID (negative number) |
| `GEMINI_API_KEY` | Your Gemini API key |

5. Railway will auto-detect the Procfile and start the bot
6. Done! Your bot is now running 24/7 for FREE

---

## STEP 5B — Deploy on Render (Alternative)

1. Go to https://render.com and sign up with GitHub
2. Click **"New"** → **"Background Worker"**
3. Connect your `puffer-coin-bot` GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
5. Click **"Advanced"** → **"Add Environment Variable"** and add:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `GEMINI_API_KEY`
6. Click **"Create Background Worker"**
7. Done!

---

## Customizing the Bot

Open `bot.py` to customize:

- **Post frequency:** Change `random.randint(3600, 7200)` — values are in seconds
  - Every 30–60 mins: `random.randint(1800, 3600)`
  - Every 2–4 hours: `random.randint(7200, 14400)`

- **Puffer Coin name:** Search and replace `"Puffer Coin"` with your actual coin name

- **Post prompts:** Edit the `POST_PROMPTS` dictionary to change what each post type says

- **Post rotation:** Edit `POST_ROTATION` list to change the order and frequency of post types

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Bot not posting | Check all 3 environment variables are set correctly |
| "Unauthorized" error | Your TELEGRAM_TOKEN is wrong |
| "Chat not found" error | Wrong TELEGRAM_CHAT_ID or bot not added to group |
| Gemini errors | Check GEMINI_API_KEY is valid at aistudio.google.com |
| Bot stopped | Check Railway/Render logs for errors |

---

Built for the Puffer Coin community 🐡🚀
