# ott.py - Updated with Nord VPN and IPVanish
import logging
import json
import os
import asyncio
import sys
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import random

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

# Configuration
BOT_TOKEN = "8967290644:AAEAdZHAm16nIuXbPJ6mD8xDiEC6Q6JPh_Q"

# Admin IDs
ADMIN_IDS = [6299808404]

# ==================== PREMIUM EMOJIS ====================

PREMIUM_EMOJI_IDS = {
    "diamond": "5039670412733055750",
    "fire": "5039670412733055750",
    "star": "6282793227057632654",
    "crown": "5039727497143387500",
    "rocket": "6235403472741603087",
    "coin": "5201873447554145566",
    "vault": "5238132025323444613",
    "gift": "5307905813451397794",
    "lightning": "6237654950432742406",
    "trophy": "5188344996356448758",
    "medal": "5188344996356448758",
    "sparkles": "6267117038808870117",
    "party": "6267117038808870117",
    "money": "5201873447554145566",
    "chart": "5461009483314517035",
    "time": "5377336227533969892",
    "done": "6267117038808870117",
    "hit": "5039670412733055750",
    "moon": "6235403472741603087",
    "sun": "6267117038808870117",
    "heart": "5377336227533969892",
    "boom": "6237654950432742406",
    "warning": "6267237615720731788",
    "error": "6282641460093260838",
    "info": "5042306247047513767",
    "success": "5039670412733055750",
    "stop": "5042167377869932162",
    "back": "5255703720078879038",
    "menu": "5427168083074628963",
    "settings": "6230927657257668107",
    "stats": "5028746137645876535",
    "users": "5869573060030683138",
    "server": "6002386288612653951",
    "lock": "5197288647275071607",
    "globe": "5447410659077661506",
    "target": "5249244862359812334",
    "flash": "5397857289216484878",
    "skull": "5042167377869932162",
    "document": "6267229004311303657",
    "clock": "5262540380301191210",
    "id": "5307905813451397794",
    "approved": "6266787022111773140",
    "declined": "6267039884016358504",
    "card": "5472250091332993630",
    "bank": "5332455502917949981",
    "bin": "5226929552319594190",
    "paypal": "5039670412733055750",
    "shopify": "5041796412954641308",
    "razorpay": "5377336227533969892",
    "stripe": "5368324170671202286",
    "autosopi": "5869573060030683138",
    "payflow": "6230927657257668107",
    "braintree": "5041796412954641308",
    "b3charged": "6002386288612653951",
    "progress": "5039670412733055750"
}

def premium_emoji(emoji_id: str, fallback: str = "•") -> str:
    """Returns a formatted premium emoji string for Telegram"""
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

def get_premium_emoji(emoji_name: str) -> str:
    """Get premium emoji by name"""
    if emoji_name in PREMIUM_EMOJI_IDS:
        fallback = {
            "diamond": "💎", "fire": "🔥", "star": "⭐", "crown": "👑",
            "rocket": "🚀", "coin": "🪙", "vault": "🏦", "gift": "🎁",
            "lightning": "⚡", "trophy": "🏆", "medal": "🎖️", "sparkles": "✨",
            "party": "🎉", "money": "💰", "chart": "📈", "time": "🔄",
            "done": "✅", "hit": "💎", "moon": "🌙", "sun": "☀️",
            "heart": "❤️", "boom": "💥", "warning": "⚠️", "error": "❌",
            "info": "ℹ️", "success": "💎", "stop": "🛑", "back": "🔙",
            "menu": "📋", "settings": "⚙️", "stats": "📊", "users": "👥",
            "server": "💻", "lock": "🔐", "globe": "🌐", "target": "🎯",
            "flash": "⚡", "skull": "💀", "document": "📄", "clock": "🕐",
            "id": "🆔", "approved": "✅", "declined": "❌", "card": "💳",
            "bank": "🏦", "bin": "🔢", "paypal": "🔥", "shopify": "💎",
            "razorpay": "🎯", "stripe": "💳", "autosopi": "👾", "payflow": "💸",
            "braintree": "🔷", "b3charged": "💰", "progress": "🔥"
        }.get(emoji_name, "•")
        return premium_emoji(PREMIUM_EMOJI_IDS[emoji_name], fallback)
    return "•"

# ==================== BOT FUNCTIONS ====================

CHANNELS = [
    {"name": "Channel 1", "username": "@channel1", "link": "https://t.me/+a-_7PTkBTe81MGY1"},
    {"name": "Channel 2", "username": "@channel2", "link": "https://t.me/+6he76BJJp3o5Y2I1"},
]

COINS_PER_REFERRAL = 2
REFERRAL_BONUS = 1
OTT_COST = 2

# OTT Platforms - Added Nord VPN and IPVanish
OTT_PLATFORMS = [
    {"id": "netflix", "name": "Netflix", "emoji": "🎬"},
    {"id": "prime", "name": "Prime Video", "emoji": "📦"},
    {"id": "hotstar", "name": "Hotstar", "emoji": "⭐"},
    {"id": "sony", "name": "Sony LIV", "emoji": "🎮"},
    {"id": "crunchyroll", "name": "Crunchyroll", "emoji": "🌸"},
    {"id": "spotify", "name": "Spotify", "emoji": "🎵"},
    {"id": "hbomax", "name": "HBO MAX", "emoji": "🎬"},
    {"id": "nordvpn", "name": "Nord VPN", "emoji": "🛡️"},
    {"id": "ipvanish", "name": "IPVanish", "emoji": "🔒"},
    {"id": "chatgpt", "name": "ChatGPT Plus", "emoji": "🤖"},
    {"id": "claude", "name": "Claude AI", "emoji": "🧠"},
    {"id": "midjourney", "name": "Midjourney", "emoji": "🎨"},
    {"id": "gemini", "name": "Google Gemini", "emoji": "🌐"},
    {"id": "perplexity", "name": "Perplexity AI", "emoji": "🔍"},
]

# OTT Accounts Database
OTT_ACCOUNTS_FILE = "ott_accounts.json"

def load_ott_accounts():
    if os.path.exists(OTT_ACCOUNTS_FILE):
        try:
            with open(OTT_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    accounts = {}
    for platform in OTT_PLATFORMS:
        accounts[platform["id"]] = []
    return accounts

def save_ott_accounts(accounts):
    with open(OTT_ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=4, ensure_ascii=False)

OTT_ACCOUNTS = load_ott_accounts()

# User data file
USER_DATA_FILE = "user_data.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

user_data = load_user_data()

def get_user(user_id):
    user_id = str(user_id)
    if user_id not in user_data:
        user_data[user_id] = {
            "coins": 0,
            "referral_code": generate_referral_code(),
            "referred_by": None,
            "referrals": [],
            "joined_channels": [],
            "redeemed_ott": [],
            "is_admin": user_id in [str(admin_id) for admin_id in ADMIN_IDS]
        }
        save_user_data(user_data)
    return user_data[user_id]

def generate_referral_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

def is_admin(user_id):
    return str(user_id) in [str(admin_id) for admin_id in ADMIN_IDS]

def format_account_details(platform, details):
    """Format account details based on platform"""
    if platform == "netflix":
        lines = details.split('\n')
        formatted = []
        for line in lines:
            if 'Desktop Link:' in line:
                link = line.replace('Desktop Link:', '').strip()
                formatted.append(f"🖥️ Desktop: {link}")
            elif 'Phone Link:' in line:
                link = line.replace('Phone Link:', '').strip()
                formatted.append(f"📱 Phone: {link}")
            elif 'TV Link:' in line:
                link = line.replace('TV Link:', '').strip()
                formatted.append(f"📺 TV: {link}")
            elif '🕐' in line:
                link = line.replace('🕐', '').replace('Desktop Link:', '').strip()
                if link:
                    formatted.append(f"🖥️ Desktop: {link}")
            elif '💎' in line and 'Phone' in line:
                link = line.replace('💎', '').replace('Phone Link:', '').strip()
                if link:
                    formatted.append(f"📱 Phone: {link}")
            elif '📊' in line:
                link = line.replace('📊', '').replace('TV Link:', '').strip()
                if link:
                    formatted.append(f"📺 TV: {link}")
            elif line.strip() and not line.startswith('💎') and not line.startswith('🕐') and not line.startswith('📊'):
                if 'http' in line.lower():
                    formatted.append(f"🔗 Link: {line.strip()}")
        return '\n'.join(formatted) if formatted else details
    
    elif platform in ["nordvpn", "ipvanish"]:
        # Format for VPN accounts
        if ':' in details:
            parts = details.split(':', 1)
            if len(parts) == 2:
                return f"📧 Email: <code>{parts[0].strip()}</code>\n🔑 Password: <code>{parts[1].strip()}</code>"
        return f"📝 Details: {details}"
    
    else:
        if ':' in details:
            parts = details.split(':', 1)
            if len(parts) == 2:
                return f"📧 Email: <code>{parts[0].strip()}</code>\n🔑 Password: <code>{parts[1].strip()}</code>"
        return f"📝 Details: {details}"

async def notify_all_users(context, platform_name, platform_emoji, count=1):
    """Send notification to all users about new stock"""
    notification_text = f"""
{get_premium_emoji('diamond')} <b>NEW STOCK ADDED</b> {get_premium_emoji('diamond')}

{platform_emoji} <b>{platform_name}</b>

{get_premium_emoji('approved')} {count} new account(s) added!

{get_premium_emoji('fire')} <b>Redeem now before they're gone!</b>
{get_premium_emoji('coin')} Cost: {OTT_COST} coins per account

👉 Go to <b>Redeem OTT</b> in the main menu!
    """
    
    keyboard = [
        [InlineKeyboardButton("🎁 Redeem Now", callback_data="redeem_ott")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    sent_count = 0
    failed_count = 0
    
    for user_id in user_data.keys():
        try:
            await context.bot.send_message(
                int(user_id),
                notification_text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            sent_count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            failed_count += 1
            logger.warning(f"Could not send notification to {user_id}: {e}")
    
    logger.info(f"Notification sent to {sent_count} users, failed: {failed_count}")
    return sent_count, failed_count

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    args = context.args
    if args and args[0].startswith('ref_'):
        referral_code = args[0][4:]
        referrer_id = None
        
        for uid, data in user_data.items():
            if data.get("referral_code") == referral_code:
                referrer_id = uid
                break
        
        if referrer_id and str(user_id) != referrer_id:
            user_info = get_user(user_id)
            if not user_info.get("referred_by"):
                user_info["referred_by"] = referrer_id
                user_info["coins"] += REFERRAL_BONUS
                save_user_data(user_data)
                
                referrer_data = get_user(referrer_id)
                if user_id not in referrer_data["referrals"]:
                    referrer_data["referrals"].append(user_id)
                    referrer_data["coins"] += COINS_PER_REFERRAL
                    save_user_data(user_data)
                    
                    await context.bot.send_message(
                        referrer_id,
                        f"{get_premium_emoji('party')} New referral! {username} joined using your link!\n"
                        f"You earned {COINS_PER_REFERRAL} {get_premium_emoji('coin')} coins!",
                        parse_mode='HTML'
                    )
    
    await show_channel_join(update, context)

async def show_channel_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for channel in CHANNELS:
        keyboard.append([InlineKeyboardButton(f"★ Join {channel['name']}", url=channel['link'])])
    
    keyboard.append([InlineKeyboardButton("✅ I've Joined", callback_data="check_joined")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('diamond')} <b>ACCESS LOCKED</b> {get_premium_emoji('diamond')}\n\n"
        f"To UNLOCK ALL FEATURES, PLEASE JOIN OUR OFFICIAL CHANNELS\n"
        f"{get_premium_emoji('sparkles')} <b>Join all channels below to access the bot:</b>\n"
    )
    
    if update.message:
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
    elif update.callback_query:
        await update.callback_query.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')

async def check_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    user_info["joined_channels"] = [c['username'] for c in CHANNELS]
    save_user_data(user_data)
    
    try:
        await query.message.delete()
    except Exception as e:
        logger.warning(f"Could not delete message: {e}")
    
    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_info = get_user(user_id)
    
    keyboard = [
        [
            InlineKeyboardButton("💰 ACCOUNT", callback_data="account"),
            InlineKeyboardButton("🎁 REFER", callback_data="refer")
        ],
        [
            InlineKeyboardButton("🎁 REDEEM OTT", callback_data="redeem_ott"),
            InlineKeyboardButton("📈 STATISTICS", callback_data="statistics")
        ],
        [
            InlineKeyboardButton("🚀 STOCK", callback_data="stock"),
            InlineKeyboardButton("🎵 SPOTIFY", callback_data="spotify")
        ],
    ]
    
    if is_admin(user_id):
        keyboard.append([
            InlineKeyboardButton("👑 ADMIN", callback_data="admin_panel"),
            InlineKeyboardButton("🛡️ VPN", callback_data="vpn_menu")
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"🏠 <b>MAIN MENU</b>\n\n"
        f"{get_premium_emoji('crown')} Welcome {update.effective_user.first_name}!\n"
        f"{get_premium_emoji('coin')} Coins: {user_info['coins']}\n"
        f"{get_premium_emoji('star')} Referrals: {len(user_info['referrals'])}\n\n"
        f"<b>EARN · REFER · WIN</b> {get_premium_emoji('fire')}\n"
        f"SELECT YOUR NEXT ACTION"
        f"OWNER @lencax "
    )
    
    if update.callback_query:
        try:
            await update.callback_query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
        except Exception as e:
            logger.warning(f"Could not edit message: {e}")
            await update.callback_query.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')
    elif update.message:
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='HTML')

async def account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    keyboard = [
        [
            InlineKeyboardButton("🪙 Balance", callback_data="balance"),
            InlineKeyboardButton("⭐ Referrals", callback_data="my_referrals")
        ],
        [
            InlineKeyboardButton("✨ Premium", callback_data="premium_status"),
            InlineKeyboardButton("🔙 Back", callback_data="main_menu")
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('money')} <b>ACCOUNT</b> {get_premium_emoji('money')}\n\n"
        f"{get_premium_emoji('crown')} User: {query.from_user.first_name}\n"
        f"{get_premium_emoji('coin')} Coins: {user_info['coins']}\n"
        f"{get_premium_emoji('star')} Referrals: {len(user_info['referrals'])}\n"
        f"{get_premium_emoji('trophy')} Total Earned: {len(user_info.get('referrals', [])) * COINS_PER_REFERRAL} coins\n\n"
        f"<b>Select an option below:</b>"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in account: {e}")

async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="account")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('coin')} <b>Coin Balance</b> {get_premium_emoji('coin')}\n\n"
        f"Available Coins: {user_info['coins']}\n"
        f"Total Earned: {len(user_info.get('referrals', [])) * COINS_PER_REFERRAL}\n\n"
        f"{get_premium_emoji('flash')} <b>Refer friends to earn more coins!</b>"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in balance: {e}")

async def premium_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="account")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    is_premium = hasattr(update.effective_user, 'is_premium') and update.effective_user.is_premium
    status = "✅ Premium" if is_premium else "❌ Free"
    
    message = (
        f"{get_premium_emoji('crown')} <b>Premium Status</b> {get_premium_emoji('crown')}\n\n"
        f"Status: {status}\n\n"
        f"{get_premium_emoji('sparkles')} <b>Premium Features:</b>\n"
        f"• Exclusive premium emojis\n"
        f"• Higher referral bonuses\n"
        f"• Priority support\n"
        f"• Early access to new features"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in premium status: {e}")

async def show_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="account")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    referrals = user_info.get("referrals", [])
    referral_text = ""
    
    if referrals:
        for i, ref_id in enumerate(referrals[:10], 1):
            try:
                user = await context.bot.get_chat(ref_id)
                name = user.username or user.first_name or f"User {ref_id}"
                referral_text += f"{i}. @{name if user.username else name}\n"
            except:
                referral_text += f"{i}. User {ref_id}\n"
    else:
        referral_text = "No referrals yet. Share your referral link!"
    
    message = (
        f"{get_premium_emoji('star')} <b>My Referrals</b> {get_premium_emoji('star')}\n\n"
        f"Total Referrals: {len(referrals)}\n"
        f"Coins per Referral: {COINS_PER_REFERRAL}\n\n"
        f"{referral_text}"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in referrals: {e}")

# VPN Menu Handler
async def vpn_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    keyboard = [
        [InlineKeyboardButton("🛡️ Nord VPN", callback_data="ott_nordvpn")],
        [InlineKeyboardButton("🔒 IPVanish", callback_data="ott_ipvanish")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('lock')} <b>VPN SERVICES</b> {get_premium_emoji('lock')}\n\n"
        f"{get_premium_emoji('coin')} Coins: {user_info['coins']}\n"
        f"Cost: {OTT_COST} coins per account\n\n"
        f"Select a VPN service to redeem:"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in vpn menu: {e}")

async def redeem_ott(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    keyboard = []
    row = []
    for platform in OTT_PLATFORMS:
        platform_id = platform["id"]
        if platform_id in OTT_ACCOUNTS and OTT_ACCOUNTS[platform_id]:
            available = any(not acc.get("redeemed", False) for acc in OTT_ACCOUNTS[platform_id])
            if available:
                row.append(InlineKeyboardButton(
                    f"{platform['emoji']} {platform['name']}", 
                    callback_data=f"ott_{platform_id}"
                ))
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
    
    if row:
        keyboard.append(row)
    
    if not keyboard:
        keyboard.append([InlineKeyboardButton("❌ No accounts available", callback_data="no_accounts")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('gift')} <b>REDEEM OTT</b> {get_premium_emoji('gift')}\n\n"
        f"Select a platform to redeem:\n"
        f"{get_premium_emoji('coin')} <b>Coins Required:</b> {OTT_COST} per account\n"
        f"💰 Your Balance: {user_info['coins']} coins"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in redeem OTT: {e}")

async def show_ott_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    platform_id = query.data.replace("ott_", "")
    platform = next((p for p in OTT_PLATFORMS if p["id"] == platform_id), None)
    
    if not platform:
        await query.message.edit_text("❌ Platform not found.")
        return
    
    accounts = OTT_ACCOUNTS.get(platform_id, [])
    
    if not accounts:
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="redeem_ott")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            f"❌ No accounts available for {platform['name']}",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        return
    
    keyboard = []
    row = []
    for i, account in enumerate(accounts):
        if not account.get("redeemed", False):
            button_text = f"{platform['emoji']} Account {i+1} - {OTT_COST} coins"
            row.append(InlineKeyboardButton(button_text, callback_data=f"redeem_{platform_id}_{i}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
    
    if row:
        keyboard.append(row)
    
    if not keyboard:
        keyboard.append([InlineKeyboardButton("❌ All accounts redeemed", callback_data="no_accounts")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="redeem_ott")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('sparkles')} <b>{platform['name']} Accounts</b> {get_premium_emoji('sparkles')}\n\n"
        f"Select an account to redeem:\n"
        f"{get_premium_emoji('coin')} <b>Cost:</b> {OTT_COST} coins per account\n"
        f"💰 Your Balance: {get_user(query.from_user.id)['coins']} coins"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in show OTT accounts: {e}")

async def process_redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    _, platform_id, account_index = query.data.split("_")
    account_index = int(account_index)
    
    user_info = get_user(user_id)
    
    if user_info['coins'] < OTT_COST:
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=f"ott_{platform_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            f"{get_premium_emoji('error')} <b>Insufficient Coins</b>\n\nRequired: {OTT_COST} coins\nYour Balance: {user_info['coins']} coins\n\n{get_premium_emoji('flash')} <b>Refer friends to earn more coins!</b>",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        return
    
    accounts = OTT_ACCOUNTS.get(platform_id, [])
    if account_index >= len(accounts) or accounts[account_index].get("redeemed", False):
        await query.message.edit_text("❌ Account not available. Please try again.")
        return
    
    account = accounts[account_index]
    platform = next((p for p in OTT_PLATFORMS if p["id"] == platform_id), None)
    
    if not platform:
        await query.message.edit_text("❌ Platform not found.")
        return
    
    user_info['coins'] -= OTT_COST
    if "redeemed_ott" not in user_info:
        user_info["redeemed_ott"] = []
    
    redemption = {
        "platform": platform_id,
        "account_index": account_index,
        "date": datetime.now().isoformat()
    }
    user_info["redeemed_ott"].append(redemption)
    
    accounts[account_index]["redeemed"] = True
    accounts[account_index]["redeemed_by"] = str(user_id)
    accounts[account_index]["redeemed_date"] = datetime.now().isoformat()
    save_ott_accounts(OTT_ACCOUNTS)
    save_user_data(user_data)
    
    formatted_details = format_account_details(platform_id, account['details'])
    
    credentials = f"""
{get_premium_emoji('party')} <b>Redemption Successful!</b> {get_premium_emoji('party')}

Platform: {platform['name']} {platform['emoji']}
{formatted_details}

{get_premium_emoji('coin')} Coins Deducted: {OTT_COST}
{get_premium_emoji('coin')} Remaining Balance: {user_info['coins']}

{get_premium_emoji('medal')} <b>Note: Please save these credentials securely.</b>
    """
    
    keyboard = [[InlineKeyboardButton(f"{get_premium_emoji('diamond')} Main Menu", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.message.edit_text(credentials, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in process redeem: {e}")

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    bot_username = context.bot.username
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_info['referral_code']}"
    
    keyboard = [
        [
            InlineKeyboardButton(f"{get_premium_emoji('rocket')} Share", url=f"https://t.me/share/url?url={referral_link}&text=Join this bot and earn {COINS_PER_REFERRAL} coins per referral!"),
            InlineKeyboardButton(f"{get_premium_emoji('diamond')} Copy", callback_data="copy_code")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('gift')} <b>REFER & EARN</b> {get_premium_emoji('gift')}\n\n"
        f"📋 <b>Your Referral Code:</b>\n"
        f"<code>{user_info['referral_code']}</code>\n\n"
        f"🔗 <b>Your Referral Link:</b>\n"
        f"<code>{referral_link}</code>\n\n"
        f"{get_premium_emoji('coin')} <b>Rewards:</b>\n"
        f"• You earn <b>{COINS_PER_REFERRAL} coins</b> per referral\n"
        f"• Your friend earns <b>{REFERRAL_BONUS} bonus coins</b>\n\n"
        f"{get_premium_emoji('star')} <b>Total Referrals:</b> {len(user_info['referrals'])}\n"
        f"{get_premium_emoji('coin')} <b>Coins Earned:</b> {len(user_info['referrals']) * COINS_PER_REFERRAL}\n\n"
        f"{get_premium_emoji('fire')} <b>Share your referral link with friends and start earning!</b>"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in refer: {e}")

async def copy_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    await query.message.reply_text(
        f"{get_premium_emoji('diamond')} <b>Your Referral Code:</b>\n<code>{user_info['referral_code']}</code>\n\nShare it with your friends! {get_premium_emoji('fire')}",
        parse_mode='HTML'
    )

async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    total_users = len(user_data)
    total_referrals = sum(len(data.get("referrals", [])) for data in user_data.values())
    total_redeemed = sum(len(data.get("redeemed_ott", [])) for data in user_data.values())
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('stats')} <b>Statistics</b> {get_premium_emoji('stats')}\n\n"
        f"{get_premium_emoji('crown')} <b>Your Stats:</b>\n"
        f"• Coins: {user_info['coins']}\n"
        f"• Referrals: {len(user_info['referrals'])}\n"
        f"• OTT Redeemed: {len(user_info.get('redeemed_ott', []))}\n\n"
        f"{get_premium_emoji('trophy')} <b>Global Stats:</b>\n"
        f"• Total Users: {total_users}\n"
        f"• Total Referrals: {total_referrals}\n"
        f"• Total OTT Redeemed: {total_redeemed}\n\n"
        f"{get_premium_emoji('medal')} <b>Top Referrers:</b>\nComing soon..."
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in statistics: {e}")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    stock_data = {"BTC": 45000, "ETH": 3200, "DOGE": 0.15, "SHIB": 0.00002, "SOL": 150}
    
    message = f"{get_premium_emoji('chart')} <b>Stock Market</b> {get_premium_emoji('chart')}\n\n"
    for asset, price in stock_data.items():
        change = random.uniform(-5, 5)
        emoji_symbol = "🟢" if change > 0 else "🔴"
        message += f"{emoji_symbol} {asset}: ${price:.2f} ({change:+.2f}%)\n"
    
    message += f"\n{get_premium_emoji('flash')} <b>Coming Soon:</b> Trade coins for stocks!"
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in stock: {e}")

async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    keyboard = [
        [InlineKeyboardButton("🎵 Redeem Spotify", callback_data="ott_spotify")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('target')} <b>SPOTIFY</b> {get_premium_emoji('target')}\n\n"
        f"{get_premium_emoji('coin')} Coins: {user_info['coins']}\n"
        f"Cost: {OTT_COST} coins per account\n\n"
        f"Click below to redeem a Spotify account!"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in spotify: {e}")

async def hbomax(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_info = get_user(user_id)
    
    keyboard = [
        [InlineKeyboardButton("🎬 Redeem HBO MAX", callback_data="ott_hbomax")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"{get_premium_emoji('target')} <b>HBO MAX</b> {get_premium_emoji('target')}\n\n"
        f"{get_premium_emoji('coin')} Coins: {user_info['coins']}\n"
        f"Cost: {OTT_COST} coins per account\n\n"
        f"Click below to redeem an HBO MAX account!"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in hbomax: {e}")

# Admin Commands
async def add_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(f"{get_premium_emoji('error')} You are not authorized to use this command.", parse_mode='HTML')
        return
    
    if len(context.args) != 2:
        await update.message.reply_text(
            f"{get_premium_emoji('info')} Usage: /add <user_id> <amount>\n"
            f"Example: /add 123456789 100",
            parse_mode='HTML'
        )
        return
    
    try:
        target_user = int(context.args[0])
        amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text(f"{get_premium_emoji('error')} Invalid user ID or amount. Please use numbers only.", parse_mode='HTML')
        return
    
    if amount <= 0:
        await update.message.reply_text(f"{get_premium_emoji('error')} Amount must be greater than 0.", parse_mode='HTML')
        return
    
    user_info = get_user(target_user)
    user_info["coins"] += amount
    save_user_data(user_data)
    
    try:
        await context.bot.send_message(
            target_user,
            f"{get_premium_emoji('party')} Admin has added {amount} coins to your account!\n"
            f"{get_premium_emoji('coin')} New Balance: {user_info['coins']} coins",
            parse_mode='HTML'
        )
    except:
        pass
    
    await update.message.reply_text(
        f"{get_premium_emoji('approved')} Added {amount} coins to user {target_user}\n"
        f"{get_premium_emoji('coin')} New balance: {user_info['coins']} coins",
        parse_mode='HTML'
    )

async def remove_coins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(f"{get_premium_emoji('error')} You are not authorized to use this command.", parse_mode='HTML')
        return
    
    if len(context.args) != 2:
        await update.message.reply_text(
            f"{get_premium_emoji('info')} Usage: /remove <user_id> <amount>\n"
            f"Example: /remove 123456789 50",
            parse_mode='HTML'
        )
        return
    
    try:
        target_user = int(context.args[0])
        amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text(f"{get_premium_emoji('error')} Invalid user ID or amount. Please use numbers only.", parse_mode='HTML')
        return
    
    if amount <= 0:
        await update.message.reply_text(f"{get_premium_emoji('error')} Amount must be greater than 0.", parse_mode='HTML')
        return
    
    user_info = get_user(target_user)
    if user_info["coins"] < amount:
        await update.message.reply_text(f"{get_premium_emoji('error')} User only has {user_info['coins']} coins.", parse_mode='HTML')
        return
    
    user_info["coins"] -= amount
    save_user_data(user_data)
    
    try:
        await context.bot.send_message(
            target_user,
            f"{get_premium_emoji('flash')} Admin has removed {amount} coins from your account.\n"
            f"{get_premium_emoji('coin')} New Balance: {user_info['coins']} coins",
            parse_mode='HTML'
        )
    except:
        pass
    
    await update.message.reply_text(
        f"{get_premium_emoji('approved')} Removed {amount} coins from user {target_user}\n"
        f"{get_premium_emoji('coin')} New balance: {user_info['coins']} coins",
        parse_mode='HTML'
    )

async def remove_ott_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(f"{get_premium_emoji('error')} You are not authorized to use this command.", parse_mode='HTML')
        return
    
    command = update.message.text[1:].lower()
    platform_id = command.replace('r', '')
    
    platform = next((p for p in OTT_PLATFORMS if p["id"] == platform_id), None)
    if not platform:
        await update.message.reply_text(
            f"{get_premium_emoji('error')} Invalid platform. Available: {', '.join(['r' + p['id'] for p in OTT_PLATFORMS])}",
            parse_mode='HTML'
        )
        return
    
    if platform_id not in OTT_ACCOUNTS or not OTT_ACCOUNTS[platform_id]:
        await update.message.reply_text(f"{get_premium_emoji('error')} No accounts found for {platform['name']}.", parse_mode='HTML')
        return
    
    accounts = OTT_ACCOUNTS[platform_id]
    removed = 0
    for acc in accounts[:]:
        if not acc.get("redeemed", False):
            accounts.remove(acc)
            removed += 1
    
    if removed > 0:
        save_ott_accounts(OTT_ACCOUNTS)
        await update.message.reply_text(
            f"{get_premium_emoji('approved')} Removed {removed} unredeemed {platform['name']} accounts from stock.",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            f"{get_premium_emoji('info')} No unredeemed {platform['name']} accounts found.",
            parse_mode='HTML'
        )

async def add_ott_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(f"{get_premium_emoji('error')} You are not authorized to use this command.", parse_mode='HTML')
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            f"{get_premium_emoji('info')} Usage: /addott <platform> <details>\n"
            f"Example: /addott netflix email:password\n"
            f"Platforms: {', '.join([p['id'] for p in OTT_PLATFORMS])}",
            parse_mode='HTML'
        )
        return
    
    platform = context.args[0].lower()
    details = ' '.join(context.args[1:])
    
    platform_exists = any(p['id'] == platform for p in OTT_PLATFORMS)
    if not platform_exists:
        await update.message.reply_text(
            f"{get_premium_emoji('error')} Invalid platform. Available platforms:\n"
            f"{', '.join([p['id'] for p in OTT_PLATFORMS])}",
            parse_mode='HTML'
        )
        return
    
    new_account = {
        "details": details,
        "redeemed": False,
        "added_by": str(user_id),
        "added_date": datetime.now().isoformat()
    }
    
    if platform not in OTT_ACCOUNTS:
        OTT_ACCOUNTS[platform] = []
    
    OTT_ACCOUNTS[platform].append(new_account)
    save_ott_accounts(OTT_ACCOUNTS)
    
    platform_obj = next((p for p in OTT_PLATFORMS if p["id"] == platform), None)
    if platform_obj:
        sent, failed = await notify_all_users(context, platform_obj['name'], platform_obj['emoji'])
        await update.message.reply_text(
            f"{get_premium_emoji('approved')} Added {platform.upper()} account:\n"
            f"<code>{details}</code>\n\n"
            f"{get_premium_emoji('users')} Notification sent to {sent} users!\n"
            f"{get_premium_emoji('error')} Failed: {failed} users",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            f"{get_premium_emoji('approved')} Added {platform.upper()} account:\n"
            f"<code>{details}</code>\n\n"
            f"Available for users to redeem for {OTT_COST} coins!",
            parse_mode='HTML'
        )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if not is_admin(user_id):
        await query.message.edit_text(f"{get_premium_emoji('error')} You are not authorized to use this panel.", parse_mode='HTML')
        return
    
    keyboard = [
        [InlineKeyboardButton("📝 Add OTT Account", callback_data="admin_add_ott")],
        [InlineKeyboardButton("📊 View All OTT Accounts", callback_data="admin_view_ott")],
        [InlineKeyboardButton("👥 View Users", callback_data="admin_view_users")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    total_accounts = sum(len(accounts) for accounts in OTT_ACCOUNTS.values())
    redeemed_accounts = sum(sum(1 for acc in accounts if acc.get("redeemed", False)) for accounts in OTT_ACCOUNTS.values())
    
    message = (
        f"{get_premium_emoji('crown')} <b>ADMIN PANEL</b> {get_premium_emoji('crown')}\n\n"
        f"Welcome Admin!\n"
        f"Total Users: {len(user_data)}\n"
        f"Total OTT Accounts: {total_accounts}\n"
        f"Redeemed Accounts: {redeemed_accounts}\n\n"
        f"<b>Select an action:</b>"
    )
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in admin panel: {e}")

async def admin_add_ott(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if not is_admin(user_id):
        return
    
    keyboard = []
    row = []
    for platform in OTT_PLATFORMS:
        row.append(InlineKeyboardButton(f"{platform['emoji']} {platform['name']}", callback_data=f"admin_add_{platform['id']}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="admin_panel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        f"{get_premium_emoji('gift')} <b>Add OTT Account</b>\n\nSelect platform to add account:\n\n<i>Tip:</i> You can also use /addott command:\n<code>/addott platform details</code>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def admin_add_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if not is_admin(user_id):
        return
    
    platform_id = query.data.replace("admin_add_", "")
    platform = next((p for p in OTT_PLATFORMS if p["id"] == platform_id), None)
    
    if not platform:
        await query.message.edit_text("❌ Platform not found.")
        return
    
    context.user_data['admin_platform'] = platform_id
    
    await query.message.edit_text(
        f"{get_premium_emoji('gift')} <b>Add {platform['name']} Account</b>\n\n"
        f"Send the account details:\n"
        f"• For email:password format: <code>email:password</code>\n"
        f"• For Netflix with links: Send all links together\n"
        f"• For multiple accounts: One per line\n\n"
        f"Type /cancel to cancel.",
        parse_mode='HTML'
    )

async def handle_admin_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    if 'admin_platform' not in context.user_data:
        return
    
    platform_id = context.user_data['admin_platform']
    platform = next((p for p in OTT_PLATFORMS if p["id"] == platform_id), None)
    text = update.message.text
    
    if text.startswith('/cancel'):
        await update.message.reply_text(f"{get_premium_emoji('stop')} Cancelled.", parse_mode='HTML')
        context.user_data.pop('admin_platform', None)
        return
    
    lines = text.strip().split('\n')
    added_count = 0
    
    if len(lines) > 1 and any('Link:' in line or 'http' in line for line in lines):
        details = text.strip()
        new_account = {
            "details": details,
            "redeemed": False,
            "added_by": str(user_id),
            "added_date": datetime.now().isoformat()
        }
        if platform_id not in OTT_ACCOUNTS:
            OTT_ACCOUNTS[platform_id] = []
        OTT_ACCOUNTS[platform_id].append(new_account)
        added_count = 1
    else:
        for line in lines:
            if ':' in line or '@' in line or 'http' in line.lower():
                details = line.strip()
                new_account = {
                    "details": details,
                    "redeemed": False,
                    "added_by": str(user_id),
                    "added_date": datetime.now().isoformat()
                }
                if platform_id not in OTT_ACCOUNTS:
                    OTT_ACCOUNTS[platform_id] = []
                OTT_ACCOUNTS[platform_id].append(new_account)
                added_count += 1
    
    if added_count > 0:
        save_ott_accounts(OTT_ACCOUNTS)
        
        if platform:
            sent, failed = await notify_all_users(context, platform['name'], platform['emoji'], added_count)
            await update.message.reply_text(
                f"{get_premium_emoji('approved')} Added {added_count} account(s) to {platform['name']}!\n"
                f"{get_premium_emoji('users')} Notification sent to {sent} users!\n"
                f"{get_premium_emoji('error')} Failed: {failed} users",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(f"{get_premium_emoji('approved')} Added {added_count} account(s)!", parse_mode='HTML')
    else:
        await update.message.reply_text(f"{get_premium_emoji('error')} No valid accounts added.", parse_mode='HTML')
    
    context.user_data.pop('admin_platform', None)
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click below to return to admin panel:", reply_markup=reply_markup)

async def admin_view_ott(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if not is_admin(user_id):
        return
    
    message = f"{get_premium_emoji('stats')} <b>OTT Accounts Overview</b> {get_premium_emoji('stats')}\n\n"
    
    total_accounts = 0
    redeemed_accounts = 0
    
    for platform in OTT_PLATFORMS:
        platform_id = platform["id"]
        accounts = OTT_ACCOUNTS.get(platform_id, [])
        total = len(accounts)
        redeemed = sum(1 for acc in accounts if acc.get("redeemed", False))
        total_accounts += total
        redeemed_accounts += redeemed
        message += f"<b>{platform['name']} {platform['emoji']}:</b> {total} total, {redeemed} redeemed\n"
    
    message += f"\n<b>Total:</b> {total_accounts} accounts, {redeemed_accounts} redeemed"
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in admin view: {e}")

async def admin_view_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if not is_admin(user_id):
        return
    
    message = f"{get_premium_emoji('users')} <b>Users Overview</b> {get_premium_emoji('users')}\n\n"
    
    sorted_users = sorted(user_data.items(), key=lambda x: len(x[1].get("referrals", [])), reverse=True)
    
    for i, (uid, data) in enumerate(sorted_users[:10], 1):
        try:
            user = await context.bot.get_chat(int(uid))
            name = user.username or user.first_name or f"User {uid[:6]}"
        except:
            name = f"User {uid[:6]}"
        
        message += f"{i}. @{name if not name.startswith('User') else name} - {data['coins']} coins, {len(data.get('referrals', []))} referrals\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')
    except Exception as e:
        logger.warning(f"Could not edit message in admin view users: {e}")

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_main_menu(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""
{get_premium_emoji('crown')} <b>Refer & Earn Bot Help</b> {get_premium_emoji('crown')}

<b>Commands:</b>
/start - Start the bot
/help - Show this help message
/balance - Check your balance

<b>Admin Commands:</b>
/add &lt;user_id&gt; &lt;amount&gt; - Add coins to user
/remove &lt;user_id&gt; &lt;amount&gt; - Remove coins from user
/addott &lt;platform&gt; &lt;details&gt; - Add OTT account (auto-notifies users)

<b>How to Earn:</b>
1. Share your referral link with friends
2. Earn <b>{COINS_PER_REFERRAL} coins</b> per referral
3. Your friend gets <b>{REFERRAL_BONUS} bonus coins</b>

<b>How to Redeem:</b>
1. Collect coins through referrals
2. Go to Redeem OTT
3. Select your platform and account
4. Get your account credentials! (Cost: {OTT_COST} coins)

<b>Available Platforms:</b>
{', '.join([p['name'] for p in OTT_PLATFORMS])}
    """
    await update.message.reply_text(help_text, parse_mode='HTML')

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_info = get_user(user_id)
    await update.message.reply_text(
        f"{get_premium_emoji('money')} <b>Your Balance</b> {get_premium_emoji('money')}\n\n"
        f"{get_premium_emoji('coin')} Coins: {user_info['coins']}\n"
        f"{get_premium_emoji('star')} Referrals: {len(user_info['referrals'])}\n"
        f"{get_premium_emoji('trophy')} Total Earned: {len(user_info.get('referrals', [])) * COINS_PER_REFERRAL}",
        parse_mode='HTML'
    )

def main():
    if sys.platform == 'win32':
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except:
            pass
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("add", add_coins))
    application.add_handler(CommandHandler("remove", remove_coins))
    application.add_handler(CommandHandler("addott", add_ott_account))
    
    # Stock removal commands for all platforms
    for platform in OTT_PLATFORMS:
        application.add_handler(CommandHandler(f"r{platform['id']}", remove_ott_stock))
    
    application.add_handler(CommandHandler("cancel", lambda u, c: None))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(check_joined, pattern="^check_joined$"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(account, pattern="^account$"))
    application.add_handler(CallbackQueryHandler(show_balance, pattern="^balance$"))
    application.add_handler(CallbackQueryHandler(show_referrals, pattern="^my_referrals$"))
    application.add_handler(CallbackQueryHandler(premium_status, pattern="^premium_status$"))
    application.add_handler(CallbackQueryHandler(redeem_ott, pattern="^redeem_ott$"))
    application.add_handler(CallbackQueryHandler(show_ott_accounts, pattern="^ott_"))
    application.add_handler(CallbackQueryHandler(process_redeem, pattern="^redeem_"))
    application.add_handler(CallbackQueryHandler(refer, pattern="^refer$"))
    application.add_handler(CallbackQueryHandler(copy_code, pattern="^copy_code$"))
    application.add_handler(CallbackQueryHandler(statistics, pattern="^statistics$"))
    application.add_handler(CallbackQueryHandler(stock, pattern="^stock$"))
    application.add_handler(CallbackQueryHandler(spotify, pattern="^spotify$"))
    application.add_handler(CallbackQueryHandler(hbomax, pattern="^hbomax$"))
    application.add_handler(CallbackQueryHandler(vpn_menu, pattern="^vpn_menu$"))
    
    # Admin handlers
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
    application.add_handler(CallbackQueryHandler(admin_add_ott, pattern="^admin_add_ott$"))
    for platform in OTT_PLATFORMS:
        application.add_handler(CallbackQueryHandler(admin_add_platform, pattern=f"^admin_add_{platform['id']}$"))
    application.add_handler(CallbackQueryHandler(admin_view_ott, pattern="^admin_view_ott$"))
    application.add_handler(CallbackQueryHandler(admin_view_users, pattern="^admin_view_users$"))
    
    application.add_handler(CallbackQueryHandler(lambda u, c: u.answer(), pattern="^no_accounts$"))

    # Message handler for admin input
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_input))

    # Error handler
    application.add_error_handler(error_handler)

    print(f"{get_premium_emoji('rocket')} Bot is starting...")
    print(f"{get_premium_emoji('diamond')} Premium emojis enabled!")
    print(f"{get_premium_emoji('crown')} Bot Token: {BOT_TOKEN[:10]}...")
    print(f"{get_premium_emoji('coin')} Referral Reward: {COINS_PER_REFERRAL} coins per referral")
    print(f"{get_premium_emoji('gift')} OTT Cost: {OTT_COST} coins per account")
    print(f"{get_premium_emoji('crown')} Admins: {ADMIN_IDS}")
    print(f"Available Platforms: {', '.join([p['name'] for p in OTT_PLATFORMS])}")
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except RuntimeError as e:
        if "There is no current event loop" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            application.run_polling(allowed_updates=Update.ALL_TYPES)
        else:
            raise

if __name__ == '__main__':
    main()