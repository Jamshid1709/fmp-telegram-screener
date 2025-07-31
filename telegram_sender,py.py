import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message: str):
    """Telegram bot orqali berilgan chat ID ga xabar yuboradi."""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    params = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'  # Xabarni chiroyli formatlash uchun
    }
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        print("✅ Xabar Telegramga muvaffaqiyatli yuborildi.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Telegramga xabar yuborishda xatolik: {e}")
        return False
