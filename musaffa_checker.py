import requests as r

# Musaffa API uchun sozlamalar. Bularni o'zgartirish shart emas.
headers = {
    'accept': 'application/json',
    'authorization': 'Bearer 826034|u2GoR0NplyMoxAOHo0NmB5Y6fkWQKShxzn4gBRZQeecd2c67',
    'x-typesense-api-key': 'NHAYhtkThbpAtxpBemD4AKPc9loguxqT',
}
base_url = 'https://h3ques1ic9vt6z4rp-1.a1.typesense.net/collections/company_profile_collection/documents/{}'

def is_shariah_compliant(ticker: str) -> bool:
    """
    Berilgan tickerning Musaffa API orqali shariatga muvofiqligini tekshiradi.
    Faqat 'COMPLIANT' bo'lsa True qaytaradi, aks holda False.
    """
    try:
        # API so'rovini 10 soniyalik timeout bilan yuborish
        re = r.get(base_url.format(ticker.upper()), headers=headers, timeout=10)
        
        if re.status_code == 200:
            data = re.json()
            # 'shariahCompliantStatus' kaliti mavjudligini va uning qiymatini tekshirish
            if data.get('shariahCompliantStatus') == 'COMPLIANT':
                print(f"✅ {ticker} shariatga muvofiq (Halal).")
                return True
                
    except requests.exceptions.RequestException as e:
        # Tarmoq xatoliklarini ushlash
        print(f"Musaffa API'ga ulanishda xato ({ticker}): {e}")
    
    # Boshqa barcha holatlarda (not-halal, doubtful, xatolik) False qaytaramiz
    print(f"❌ {ticker} shariatga muvofiq emas yoki ma'lumot topilmadi.")
    return False
