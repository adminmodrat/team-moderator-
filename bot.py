import os
import asyncio
import random
import logging
from datetime import datetime
import httpx
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8576842011:AAEw80HhI1H7Do_jSHwSEQ-pE82zXJPodW4")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1003994052181")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6IKLGgqvdXQR1iSBHJnN2Jmy0lNdUwDY0sAGIniwUnw")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

POST_ROTATION = [
    "gm", "news", "puffer", "funny", "prices",
    "community", "trending", "puffer", "prediction",
    "degen", "news", "puffer", "wisdom", "viral",
    "wouldyou", "funny", "prices", "puffer", "vibe", "recap"
]

POST_PROMPTS = {
    "puffer": """You are a hype community bot for "Puffer Coin" — a brand new memecoin launching very soon on Solana.
Write ONE short, exciting Telegram community post (4-7 lines) about the upcoming Puffer Coin launch.
Use crypto slang, fire emojis, FOMO energy. Pick a DIFFERENT angle every time from: countdown hype, early holder benefits,
why Puffer Coin will 100x, whitelist reminder, tokenomics teaser, team hype, why puffer fish = future, community strength.
End the post with 4-6 relevant hashtags on a new line.
Output ONLY the post text, nothing else.""",

    "news": """You are a crypto community bot for a memecoin Telegram group.
Write ONE exciting breaking crypto news post (4-6 lines).
Cover something like: Bitcoin price action, major exchange listing news, whale wallet movement,
altcoin season signals, DeFi protocol update, or regulatory news.
Use emojis, crypto lingo, make it feel urgent and exciting.
End with 4-5 hashtags. Output ONLY the post text.""",

    "prices": """You are a crypto community bot. Write ONE price update post for a memecoin community.
Mention 4-5 memecoins from this list: DOGE, SHIB, PEPE, FLOKI, BONK, WIF, BRETT, MOG, POPCAT.
Give each coin a made-up but realistic percentage change (mix green and red, e.g. +12.4%, -3.1%).
React to the prices with energy and emojis. Make it entertaining.
End with hashtags. Output ONLY the post.""",

    "funny": """You are a crypto community bot. Write ONE relatable funny trading moment post for a memecoin Telegram group.
Pick from: panic selling right before a pump, buying the absolute top, explaining crypto to family at dinner,
sleeping through a 50x, diamond handing through a 90% dip, FOMO buying at ATH, trusting a random alpha call.
3-5 lines, very relatable humor, lots of emojis.
End with hashtags. Output ONLY the post.""",

    "trending": """You are a crypto community bot. Write ONE trending coins roundup post for a memecoin community.
List 4-5 trending memecoins or micro-cap altcoins with a one-line hype vibe about each.
Make it feel like insider alpha. Emojis throughout.
End with hashtags. Output ONLY the post.""",

    "community": """You are a crypto community bot. Write ONE spicy engagement question or poll for a memecoin Telegram group.
Options: a hot crypto debate topic, a prediction challenge, a "drop your entry price" call-out,
or a question that splits the community (bulls vs bears).
2-4 lines, fun and interactive, lots of emojis.
End with hashtags. Output ONLY the post.""",

    "gm": """You are a crypto community bot. Write ONE high-energy GM (Good Morning) hype post for a memecoin Telegram group.
Pump up the morning energy, reference diamond hands, staying bullish, the grind never stops.
3-5 lines, very energetic and motivating. Emojis.
End with hashtags. Output ONLY the post.""",

    "prediction": """You are a crypto community bot. Write ONE bold crypto market prediction post for a memecoin community.
Be daring: Bitcoin price target, a memecoin that will 10x this week, altcoin season incoming, or a broad market call.
Give a simple reason for the prediction. 3-5 lines. Emojis.
End with hashtags. Output ONLY the post.""",

    "wisdom": """You are a crypto community bot. Write ONE trading wisdom or tip post for a memecoin community.
Make it genuinely useful: risk management rules, DYOR reminder, how to spot rug pulls,
managing FOMO emotions, taking profits, position sizing.
3-5 lines. Emojis but keep it educational.
End with hashtags. Output ONLY the post.""",

    "degen": """You are a crypto community bot. Write ONE funny degen confession or story for a memecoin community.
Things degens do: putting rent money in crypto, following random alpha CT accounts, holding a -95% bag,
refreshing Dexscreener at 3am, buying a coin because the name is funny.
First-person style, very relatable, hilarious. 3-5 lines. Emojis.
End with hashtags. Output ONLY the post.""",

    "viral": """You are a crypto community bot. Write ONE viral tweet-style post about crypto culture for a Telegram group.
It should feel like something that blows up on Crypto Twitter — a hot take, a pattern observation,
or a funny-but-true statement about market psychology or degen behavior.
Short punchy lines. Emojis. Quotable.
End with hashtags. Output ONLY the post.""",

    "wouldyou": """You are a crypto community bot. Write ONE "Would You Rather" crypto question for a memecoin Telegram group.
Make both options hard to choose — e.g. "100x on a memecoin but must sell in 1 hour" vs "10x on BTC, hold 1 year".
Present option A and option B clearly. Ask the community to vote.
3-5 lines. Emojis. Fun and engaging.
End with hashtags. Output ONLY the post.""",

    "recap": """You are a crypto community bot. Write ONE weekly crypto recap post for a memecoin community.
Cover 4-5 bullet points: biggest price moves, notable news, memecoin highlights, a community win, what to watch next week.
Use emojis, make it feel like a valuable weekly digest.
End with hashtags. Output ONLY the post.""",

    "vibe": """You are a crypto community bot. Write ONE market vibe check post for a memecoin community.
Rate the current market: BULLISH / BEARISH / CRAB / CHAOS / DEGEN SZN.
Include a made-up "Community Sentiment Score" out of 100.
Give a fun 2-3 line explanation of the vibe. Emojis and energy.
End with hashtags. Output ONLY the post.""",
}

post_counter = 0


async def call_gemini(prompt: str) -> str:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 500, "temperature": 0.95}
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(GEMINI_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()


async def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        logger.info("Message sent to Telegram successfully.")


def get_next_post_type() -> str:
    global post_counter
    post_type = POST_ROTATION[post_counter % len(POST_ROTATION)]
    post_counter += 1
    return post_type


def get_delay_seconds() -> int:
    # Random delay between 30 60 mins
    return random.randint(1800, 3600)


async def run_bot():
    logger.info("🐡 Puffer Coin Community Bot started!")

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID or not GEMINI_API_KEY:
        logger.error("Missing environment variables! Check TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY")
        return

    # Send startup message
    await send_telegram(
        "🐡 <b>Puffer Coin Community Bot is now LIVE!</b>\n\n"
        "I'll be keeping the community active with crypto news, memes, "
        "market updates, and Puffer Coin hype every 1-2 hours!\n\n"
        "Let's gooo! 🚀🔥"
    )

    while True:
        try:
            post_type = get_next_post_type()
            prompt = POST_PROMPTS[post_type]

            logger.info(f"Generating post type: {post_type}")
            post_text = await call_gemini(prompt)

            logger.info(f"Sending post to Telegram:\n{post_text[:500]}...")
            await send_telegram(post_text)

            delay = get_delay_seconds()
            logger.info(f"Next post in {delay // 60} minutes.")
            await asyncio.sleep(delay)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            await asyncio.sleep(300)  # retry in 5 mins
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await asyncio.sleep(300)


if __name__ == "__main__":
    asyncio.run(run_bot())
