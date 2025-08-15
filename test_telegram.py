import requests

TOKEN = '8396764345:AAH2aFy5lLAnr4xf-9FU91cWkYIrdG1f7hs'
CHAT_ID = '@abkllr'

try:
    # Test getMe per verificare il bot
    r = requests.get(f'https://api.telegram.org/bot{TOKEN}/getMe', timeout=5)
    if r.status_code == 200:
        bot_info = r.json()
        bot_name = bot_info.get('result', {}).get('first_name', 'Unknown')
        print(f'✅ Bot Telegram connesso: {bot_name}')
        
        # Test invio messaggio di prova
        test_msg = "🧪 TEST PRE-DEPLOY - Verifica configurazione Telegram"
        payload = {
            "chat_id": CHAT_ID,
            "text": test_msg,
            "parse_mode": "Markdown"
        }
        
        r2 = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=payload, timeout=10)
        if r2.status_code == 200:
            print(f'✅ Messaggio test inviato con successo a {CHAT_ID}')
        else:
            print(f'❌ Errore invio messaggio: {r2.status_code} - {r2.text}')
    else:
        print(f'❌ Errore verifica bot: {r.status_code}')
except Exception as e:
    print(f'❌ Errore connessione Telegram: {e}')
