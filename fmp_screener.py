import requests
import pandas as pd
from config import FMP_API_KEY
from datetime import datetime

def run_power_hour_screener():
    """
    Kunlik va soatlik hajmni tahlil qiluvchi murakkab skriner.
    1. Kunlik filtrlash (narx < $5, hajm > 100k, OTC emas).
    2. Soatlik filtrlash (oxirgi soatdagi hajmning g'ayrioddiy o'sishi).
    """
    print("Murakkab 'Power Hour' skrineri ishga tushdi...")
    
    # 1-Qadam: Dastlabki kunlik filtrlash
    try:
        screener_params = {
            'apikey': FMP_API_KEY,
            'priceLowerThan': 5,
            'volumeMoreThan': 100000,
            'exchange': 'NYSE,NASDAQ,AMEX', # OTC bo'lmagan birjalar
            'isActivelyTrading': True,
            'limit': 500 # Tekshirish uchun maksimal aksiyalar soni
        }
        response = requests.get('https://financialmodelingprep.com/api/v3/stock-screener', params=screener_params)
        response.raise_for_status()
        pre_screened_stocks = response.json()
        
        if not pre_screened_stocks:
            return "Dastlabki filtrga mos aksiyalar topilmadi."
            
        print(f"Dastlabki filtrdan {len(pre_screened_stocks)} ta aksiya o'tdi. Soatlik tahlil boshlanmoqda...")
        
    except requests.exceptions.RequestException as e:
        return f"❌ Dastlabki filtrlashda API xatoligi: {e}"

    # 2-Qadam: Soatlik hajmni tahlil qilish
    final_results = []
    
    for stock in pre_screened_stocks:
        symbol = stock['symbol']
        try:
            # Soatlik sham ma'lumotlarini olish
            hourly_response = requests.get(f"https://financialmodelingprep.com/api/v3/historical-chart/1hour/{symbol}?apikey={FMP_API_KEY}")
            hourly_response.raise_for_status()
            hourly_data = hourly_response.json()

            if not hourly_data or len(hourly_data) < 2:
                continue # Agar ma'lumot yetarli bo'lmasa, keyingi aksiyaga o'tish

            # FMP ma'lumotlarni eng so'nggisini birinchi qilib beradi
            # Oxirgi sham (15:00 - 16:00)
            candle_15 = None
            # Oxirgidan oldingi sham (14:00 - 15:00)
            candle_14 = None

            # To'g'ri soatdagi shamlarni topish
            # Vaqtlar Nyu-York vaqti bilan bo'ladi
            for candle in hourly_data:
                candle_time = datetime.strptime(candle['date'], '%Y-%m-%d %H:%M:%S').time()
                if candle_time.hour == 15:
                    candle_15 = candle
                elif candle_time.hour == 14:
                    candle_14 = candle
                # Ikkala sham topilsa, tsiklni to'xtatish mumkin
                if candle_15 and candle_14:
                    break
            
            # Agar kerakli shamlar topilsa, shartlarni tekshirish
            if candle_15 and candle_14:
                volume_15 = candle_15['volume']
                volume_14 = candle_14['volume']
                
                print(f"Tekshirilmoqda: {symbol} | 15:00 Hajm: {volume_15}, 14:00 Hajm: {volume_14}")

                # Asosiy shartlarni tekshirish
                condition_1 = volume_15 > 1000000
                condition_2 = volume_15 >= 1.5 * volume_14

                if condition_1 and condition_2:
                    print(f"*** TOPILDI: {symbol} barcha shartlarga mos keldi! ***")
                    final_results.append(symbol)
        
        except requests.exceptions.RequestException:
            # Bitta aksiya xato bersa, jarayonni to'xtatmasdan davom ettirish
            print(f"{symbol} uchun soatlik ma'lumot olishda xatolik. O'tkazib yuborildi.")
            continue

    # Yakuniy natijani formatlash
    if not final_results:
        return "Yakuniy filtrlashdan so'ng hech qanday aksiya topilmadi."

    message = "📈 **'Power Hour' Hajm Skrineri Natijalari**\n\n"
    message += "Quyidagi aksiyalar bozor yopilish oldidan g'ayrioddiy hajm ko'rsatdi:\n\n"
    message += "Tickerlar: **" + ", ".join(final_results) + "**"
    
    return message
