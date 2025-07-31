import schedule
import time
from fmp_screener import run_screener
from telegram_sender import send_telegram_message

def job():
    """Asosiy vazifa: skrinerdan natija olib, telegramga yuborish."""
    print(f"[{time.ctime()}] Skriner ishga tushirildi...")
    
    # Skrinerdan natijani olish
    results_message = run_screener()
    
    # Natijani telegramga yuborish
    if results_message:
        send_telegram_message(results_message)
    else:
        print("Skriner natija qaytarmadi.")
        
    print(f"[{time.ctime()}] Vazifa yakunlandi. Keyingi ishga tushishni kutilmoqda...")

if __name__ == "__main__":
    print("🤖 FMP-Telegram Skriner Boti ishga tushdi.")
    
    # --- ISHLASH VAQTINI SOZLANG ---
    # Har kuni Toshkent vaqti bilan soat 18:30 da ishga tushirish (AQSh bozori ochilishidan keyin)
    schedule.every().day.at("18:30").do(job)
    
    # Test uchun: har 1 daqiqada ishga tushirish
    # schedule.every(1).minutes.do(job)
    
    # Dastlab bir marta darhol ishga tushirish
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
