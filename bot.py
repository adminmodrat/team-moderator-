import os
import asyncio
import random
import logging
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "
8576842011:AAEw80HhI1H7DojSHwSEQpE82zXJPodW4")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1001003994052181")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LXaquKpXDmtK4CzHgbK2ZsXbOFqJ3Pupm1g3YadP6lA")

# ─── MEMEGUARDIAN SYSTEM PROMPT ───────────────────────────────────────────────
SYSTEM_PROMPT = """
You are MemeGuardian, the AI community manager for the Puffer Coin memecoin community on Telegram.
Your job is to help grow, entertain, educate, and protect the community while behaving like a real, friendly, experienced crypto enthusiast.

PERSONALITY:
- Friendly and approachable.
- Speaks naturally like a human, not like a robot.
- Uses humor occasionally but does not spam jokes.
- Encourages members during losses and difficult market conditions.
- Never insults members.
- Never starts arguments.
- Confident but humble.
- Uses crypto slang moderately (GM, WAGMI, DYOR, HODL, degen, ape in, etc).
- Focuses on community growth and positive engagement.

COMMUNITY BEHAVIOR:
- Join conversations naturally when relevant.
- Do not respond to every message.
- Speak only when it adds value.
- Avoid dominating discussions.
- Encourage members to talk to each other.
- Welcome new members warmly.
- Thank active contributors occasionally.
- Congratulate community achievements.

MODERATION:
- Politely discourage excessive profanity.
- If members become aggressive, encourage respectful discussion.
- Warn members about suspicious activity or scam links.
- Discourage harassment and personal attacks.
- Keep the environment friendly and professional.

TRADING SUPPORT:
- Never guarantee profits.
- Never promise moonshots.
- Remind members about risk management.
- Encourage responsible trading.
- Help members understand market cycles.

MEMECOIN KNOWLEDGE:
- Explain market trends in simple language.
- Discuss narratives and community growth.
- Share educational insights about liquidity, volume, market cap, holders, and tokenomics.

COMMUNITY PROMOTION:
- Subtly remind members that Puffer Coin launch is being prepared.
- Never spam launch announcements.
- Examples: "The community continues to grow. Exciting things are being built behind the scenes."

MAIN OBJECTIVE:
Create a strong, active, informed, and loyal memecoin community where members feel welcomed, entertained, educated, and protected.
"""

# ─── POST ROTATION ────────────────────────────────────────────────────────────
POST_ROTATION = [
    "gm", "news", "puffer", "funny", "prices",
    "community", "trending", "puffer", "prediction",
    "degen", "news", "puffer", "wisdom", "viral",
    "wouldyou", "funny", "prices", "puffer", "vibe",
    "recap", "story", "motivation", "education", "puffer"
]

# ─── POST PROMPTS ─────────────────────────────────────────────────────────────
POST_PROMPTS = {
    "puffer": f"""{SYSTEM_PROMPT}
Write ONE short exciting Telegram post (4-7 lines) hyping the upcoming Puffer Coin launch on Solana.
Pick a DIFFERENT angle each time: countdown hype, early holder benefits, why Puffer Coin will 100x,
whitelist reminder, tokenomics teaser, team dedication, puffer fish symbolism, community strength.
Use fire emojis, FOMO energy, crypto slang. End with 4-6 hashtags. Output ONLY the post text.""",

    "news": f"""{SYSTEM_PROMPT}
Write ONE exciting breaking crypto news post (4-6 lines) for the community.
Cover: Bitcoin price action, major exchange listing, whale movement, altcoin season signals, DeFi update, or regulation news.
Use emojis, crypto lingo, make it feel urgent and exciting. End with hashtags. Output ONLY the post.""",

    "prices": f"""{SYSTEM_PROMPT}
Write ONE entertaining price update post. Mention 4-5 memecoins from: DOGE, SHIB, PEPE, FLOKI, BONK, WIF, BRETT, MOG, POPCAT.
Give each a realistic made-up percentage change (mix green and red). React with energy and humor. End with hashtags. Output ONLY the post.""",

    "funny": f"""{SYSTEM_PROMPT}
Write ONE relatable funny trading moment post (3-5 lines).
Pick from: panic selling before a pump, buying the top, explaining crypto to family, sleeping through a 50x,
diamond handing a -90% dip, FOMO buying ATH, trusting a random alpha call.
Very relatable humor, lots of emojis. End with hashtags. Output ONLY the post.""",

    "trending": f"""{SYSTEM_PROMPT}
Write ONE trending coins roundup post. List 4-5 trending memecoins with a one-line hype vibe about each.
Feel like insider alpha. Emojis throughout. End with hashtags. Output ONLY the post.""",

    "community": f"""{SYSTEM_PROMPT}
Write ONE spicy community engagement question or poll (2-4 lines).
Options: hot crypto debate, prediction challenge, "drop your entry price", bulls vs bears split.
Fun and interactive, lots of emojis. End with hashtags. Output ONLY the post.""",

    "gm": f"""{SYSTEM_PROMPT}
Write ONE high-energy GM (Good Morning) hype post (3-5 lines).
Pump up morning energy, reference diamond hands, staying bullish, the grind never stops.
Very energetic and motivating. Emojis. End with hashtags. Output ONLY the post.""",

    "prediction": f"""{SYSTEM_PROMPT}
Write ONE bold crypto market prediction post (3-5 lines).
Be daring: Bitcoin price target, a memecoin 10x this week, altcoin season incoming, broad market call.
Give a simple reason. Emojis. End with hashtags. Output ONLY the post.""",

    "wisdom": f"""{SYSTEM_PROMPT}
Write ONE trading wisdom or tip post (3-5 lines).
Genuinely useful: risk management, DYOR reminder, spot rug pulls, managing FOMO, taking profits, position sizing.
Emojis but keep it educational. End with hashtags. Output ONLY the post.""",

    "degen": f"""{SYSTEM_PROMPT}
Write ONE funny degen confession or story (3-5 lines).
Things degens do: rent money in crypto, random alpha accounts, holding -95% bag, Dexscreener at 3am, buying a coin for the name.
First-person style, relatable, hilarious. Emojis. End with hashtags. Output ONLY the post.""",

    "viral": f"""{SYSTEM_PROMPT}
Write ONE viral tweet-style post about crypto culture (3-5 short punchy lines).
Hot take, pattern observation, or funny-but-true statement about market psychology or degen behavior.
Emojis. Quotable. End with hashtags. Output ONLY the post.""",

    "wouldyou": f"""{SYSTEM_PROMPT}
Write ONE "Would You Rather" crypto question (3-5 lines).
Both options must be hard to choose. Present Option A and Option B clearly. Ask community to vote.
Emojis. Fun and engaging. End with hashtags. Output ONLY the post.""",

    "recap": f"""{SYSTEM_PROMPT}
Write ONE weekly crypto recap post. Cover 4-5 bullet points:
biggest price moves, notable news, memecoin highlights, community win, what to watch next week.
Emojis, make it feel like a valuable digest. End with hashtags. Output ONLY the post.""",

    "vibe": f"""{SYSTEM_PROMPT}
Write ONE market vibe check post. Rate the market: BULLISH / BEARISH / CRAB / CHAOS / DEGEN SZN.
Include a made-up "Community Sentiment Score" out of 100. Fun 2-3 line explanation. Emojis and energy.
End with hashtags. Output ONLY the post.""",

    "story": f"""{SYSTEM_PROMPT}
Tell ONE short crypto success or lesson story (4-7 lines).
Choose from: early Bitcoin adopter, memecoin success story, famous trading mistake, community-building win, crypto market history.
Make it engaging, human, with a lesson at the end. Emojis. End with hashtags. Output ONLY the post.""",

    "motivation": f"""{SYSTEM_PROMPT}
Write ONE motivational message for the crypto community (3-5 lines).
Encourage during market uncertainty, remind about long-term vision, celebrate the journey not just the gains.
Warm, human, uplifting tone. Emojis. End with hashtags. Output ONLY the post.""",

    "education": f"""{SYSTEM_PROMPT}
Write ONE short educational crypto post (4-6 lines). Explain ONE concept simply:
liquidity, market cap, tokenomics, volume, holders count, what makes a memecoin succeed, how to read charts basics.
Easy to understand for beginners. Emojis. End with hashtags. Output ONLY the post.""",
}

# ─── REPLY PROMPTS (for responding to member messages) ────────────────────────
REPLY_SITUATIONS = {
    "loss": f"""{SYSTEM_PROMPT}
A community member just said they lost money in crypto. Write a SHORT empathetic reply (2-3 lines max).
Be supportive, encourage learning from the loss, remind about risk management. Human and warm tone. No hashtags.""",

    "scam_warning": f"""{SYSTEM_PROMPT}
You noticed a suspicious link or potential scam in the community. Write a SHORT warning post (2-3 lines).
Warn members not to click unknown links, remind them the team never DMs first asking for funds. Firm but calm.""",

    "aggression": f"""{SYSTEM_PROMPT}
A member is being aggressive or rude in the chat. Write a SHORT polite reply (1-2 lines) encouraging respectful discussion.
Do not fight back. Stay calm and professional.""",

    "profanity": f"""{SYSTEM_PROMPT}
A member used excessive profanity. Write a SHORT polite reminder (1 line) asking to keep the chat respectful.""",

    "spam": f"""{SYSTEM_PROMPT}
A member is sending too many messages. Write a SHORT humorous and polite reply (1-2 lines) asking them to let others talk too.
Use light humor. Never insult them.""",

    "new_member": f"""{SYSTEM_PROMPT}
A new member just joined the community. Write a SHORT warm welcome message (2-3 lines).
Make them feel valued, mention the community is growing, hint at exciting things coming with Puffer Coin. Friendly emojis.""",

    "fud": f"""{SYSTEM_PROMPT}
A member is spreading FUD (Fear, Uncertainty, Doubt) about the project. Write a SHORT calm confident reply (2-3 lines).
Acknowledge their concern, provide perspective, encourage DYOR. Never be defensive or aggressive.""",
}

post_counter = 0


async def call_gemini(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 600, "temperature": 0.95}
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload)
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


async def handle_member_update(update: dict):
    """Handle incoming messages from community members."""
    try:
        message = update.get("message", {})
        text = message.get("text", "").lower()
        if not text:
            return

        # Detect situations and respond intelligently
        situation = None

        loss_keywords = ["lost", "loss", "down bad", "rekt", "rugged", "-70", "-80", "-90", "-50", "lost everything"]
        scam_keywords = ["click here", "free tokens", "dm me", "guaranteed profit", "t.me/", "bit.ly"]
        aggression_keywords = ["idiot", "stupid project", "scam team", "rug pull", "trash project", "worst coin"]
        fud_keywords = ["this is dead", "project is dead", "team abandoned", "no updates", "slow progress"]
        new_member_phrases = ["joined", "new here", "just found", "just joined", "hello everyone", "hi all"]
        spam_threshold = 5  # if same user sends many messages (simplified check)

        if any(word in text for word in loss_keywords):
            situation = "loss"
        elif any(word in text for word in scam_keywords):
            situation = "scam_warning"
        elif any(word in text for word in aggression_keywords):
            situation = "aggression"
        elif any(word in text for word in fud_keywords):
            situation = "fud"
        elif any(phrase in text for phrase in new_member_phrases):
            situation = "new_member"

        # Only reply ~40% of the time to feel human, always reply to important situations
        important = situation in ["scam_warning", "aggression", "loss"]
        should_reply = important or (situation and random.random() < 0.4)

        if situation and should_reply:
            prompt = REPLY_SITUATIONS[situation]
            reply = await call_gemini(prompt)
            await send_telegram(reply)
            logger.info(f"Replied to situation: {situation}")

    except Exception as e:
        logger.error(f"Error handling update: {e}")


async def poll_updates(offset: int = 0) -> tuple[list, int]:
    """Poll Telegram for new messages."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 10, "limit": 20}
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        updates = data.get("result", [])
        new_offset = updates[-1]["update_id"] + 1 if updates else offset
        return updates, new_offset


def get_next_post_type() -> str:
    global post_counter
    post_type = POST_ROTATION[post_counter % len(POST_ROTATION)]
    post_counter += 1
    return post_type


def get_delay_seconds() -> int:
    return random.randint(1800, 3600)


async def posting_loop():
    """Main loop that posts content every 1-2 hours."""
    # Wait 30 seconds before first post
    await asyncio.sleep(30)

    while True:
        try:
            post_type = get_next_post_type()
            prompt = POST_PROMPTS[post_type]
            logger.info(f"Generating post type: {post_type}")
            post_text = await call_gemini(prompt)
            await send_telegram(post_text)
            logger.info(f"Posted: {post_type}")
            delay = get_delay_seconds()
            logger.info(f"Next post in {delay // 60} minutes.")
            await asyncio.sleep(delay)

        except httpx.HTTPStatusError as e:
            logger.error(f"Posting HTTP error: {e.response.status_code} - {e.response.text}")
            await asyncio.sleep(300)
        except Exception as e:
            logger.error(f"Posting error: {e}")
            await asyncio.sleep(300)


async def listening_loop():
    """Listen for member messages and respond intelligently."""
    offset = 0
    logger.info("MemeGuardian listening for community messages...")

    while True:
        try:
            updates, offset = await poll_updates(offset)
            for update in updates:
                await handle_member_update(update)
            await asyncio.sleep(5)  # poll every 5 seconds

        except Exception as e:
            logger.error(f"Listening error: {e}")
            await asyncio.sleep(15)


async def run_bot():
    logger.info("🐡 Puffer Coin MemeGuardian Bot started!")

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID or not GEMINI_API_KEY:
        logger.error("Missing environment variables! Check TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, GEMINI_API_KEY")
        return

    # Startup message
    await send_telegram(
        "🐡 <b>MemeGuardian is now LIVE!</b>\n\n"
        "I'm your AI community manager — keeping the Puffer Coin community active, "
        "entertained, educated, and protected 24/7.\n\n"
        "Posting every 1-2 hours and listening to the community. WAGMI! 🚀🔥"
    )

    # Run both loops simultaneously
    await asyncio.gather(
        posting_loop(),
        listening_loop()
    )


if __name__ == "__main__":
    asyncio.run(run_bot())
