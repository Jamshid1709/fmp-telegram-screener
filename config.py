import os

def load_my_env():
    """
    .env faylini o'qib, o'zgaruvchilarni OS muhitiga qo'shadi.
    Bu funksiya python-dotenv kutubxonasiga muqobil.
    """
    try:
        # Faylni 'utf-8-sig' bilan ochish BOM belgisidan himoyalaydi
        with open('.env', 'r', encoding='utf-8-sig') as f:
            for line in f:
                clean_line = line.strip()
                # Izohlarni va bo'sh qatorlarni o'tkazib yuborish
                if clean_line and not clean_line.startswith('#') and '=' in clean_line:
                    key, value = clean_line.split('=', 1)
                    # Agar OS muhitida bu o'zgaruvchi hali yo'q bo'lsa, uni qo'shamiz
                    if key not in os.environ:
                        os.environ[key] = value
        return True
    except FileNotFoundError:
        print("XATO: .env fayli topilmadi!")
        return False
    except Exception as e:
        print(f".env faylini o'qishda kutilmagan xatolik: {e}")
        return False

# O'zimizning funksiyamizni chaqirib, .env faylini yuklaymiz
env_loaded_successfully = load_my_env()

# O'zgaruvchilarni OS muhitidan o'qiymiz
FMP_API_KEY = os.getenv('FMP_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Barcha kalitlar yuklanganini tekshiramiz
if not all([FMP_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    raise ValueError("Xatolik: .env faylidan o'zgaruvchilarni o'qib bo'lmadi. Fayl tarkibini yoki joylashuvini tekshiring.")
