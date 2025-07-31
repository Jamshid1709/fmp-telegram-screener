import requests
import pandas as pd
from config import FMP_API_KEY

def run_screener():
    """FMP API orqali aksiyalarni belgilangan kriteriyalar bo'yicha filtrlaydi."""
    
    BASE_URL = 'https://financialmodelingprep.com/api/v3/stock-screener'
    
    # --- BU YERDA O'Z KRITERIYALARINGIZNI SOZLANG ---
    params = {
        'apikey': FMP_API_KEY,
        'marketCapMoreThan': 50000000000,   # Kapitallashuvi > 50 mlrd $
        'volumeMoreThan': 1000000,          # Kunlik savdo hajmi > 1 mln
        'isActivelyTrading': True,          # Faol savdodagi aksiyalar
        'exchange': 'NASDAQ,NYSE',          # Faqat NASDAQ va NYSE birjalari
        'limit': 20                         # Natijalar soni (maksimal 20 ta)
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return "✅ Kriteriyalarga mos aksiyalar topilmadi."
            
        df = pd.DataFrame(data)
        return format_results(df)
        
    except requests.exceptions.RequestException as e:
        return f"❌ FMP API ga ulanishda xatolik: {e}"
    except Exception as e:
        return f"❌ Noma'lum xatolik yuz berdi: {e}"

def format_results(df: pd.DataFrame) -> str:
    """Natijalarni Telegram uchun chiroyli matn formatiga o'tkazadi."""
    
    if df.empty:
        return "✅ Natijalar bo'sh."
        
    message = "📈 **FMP Skriner Natijalari**\n\n"
    message += "Quyidagi aksiyalar belgilangan kriteriyalarga mos keldi:\n\n"
    
    for index, row in df.iterrows():
        symbol = row['symbol']
        company = row['companyName']
        price = row['price']
        market_cap_bil = row['marketCap'] / 1_000_000_000
        
        message += f"▪️ **{company} ({symbol})**\n"
        message += f"   - Narxi: `${price:,.2f}`\n"
        message += f"   - Kapitallashuvi: `${market_cap_bil:,.2f} mlrd`\n\n"
        
    message += f"_{pd.Timestamp.now('Asia/Tashkent').strftime('%Y-%m-%d %H:%M:%S')} holatiga ko'ra._"
    
    return message
