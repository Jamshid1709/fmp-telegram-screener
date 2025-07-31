# main.py
from fmp_screener import run_power_hour_screener # Funksiya nomini o'zgartirdik
from telegram_sender import send_telegram_message
import time

def job():
    """Asosiy vazifa: skrinerdan natija olib, telegramga yuborish."""
    print(f"[{time.ctime()}] Skriner ishga tushirildi...")
    
    results_message = run_power_hour_screener() # Yangi funksiyani chaqiryapmiz
    
    if results_message:
        send_telegram_message(results_message)
    else:
        print("Skriner natija qaytarmadi.")
        
    print(f"[{time.ctime()}] Vazifa yakunlandi.")

# Skript ishga tushganda faqat bir marta 'job' funksiyasini chaqirish
if __name__ == "__main__":
    job()
