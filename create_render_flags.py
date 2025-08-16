#!/usr/bin/env python3
"""
Script per creare flag su Render via API per fermare il recovery
"""
import requests
import datetime

def create_render_flags():
            render_url="https://five55-7ozo.onrender.com",
    italy_tz = datetime.timezone(datetime.timedelta(hours=1))
    today = datetime.datetime.now(italy_tz).strftime('%Y%m%d')

    print(f'🚀 Creazione flag su Render per {today}...')

    # Crea flag rassegna stampa mattutina
    morning_content = f'Morning news sent at {datetime.datetime.now(italy_tz).strftime("%Y-%m-%d %H:%M:%S")}\nFlag created via API to stop recovery'
    morning_files = {'file': (f'morning_news_sent_{today}.flag', morning_content.encode())}

    try:
        response1 = requests.post(f'{render_url}/api/upload', files=morning_files, timeout=30)
        if response1.status_code == 200:
            print('✅ Flag rassegna stampa creato su Render')
        else:
            print(f'❌ Errore flag rassegna: {response1.status_code} - {response1.text}')
    except Exception as e:
        print(f'❌ Errore rassegna: {e}')

    # Crea flag report giornaliero  
    daily_content = f'Daily report sent at {datetime.datetime.now(italy_tz).strftime("%Y-%m-%d %H:%M:%S")}\nFlag created via API to stop recovery'
    daily_files = {'file': (f'daily_report_sent_{today}.flag', daily_content.encode())}

    try:
        response2 = requests.post(f'{render_url}/api/upload', files=daily_files, timeout=30)
        if response2.status_code == 200:
            print('✅ Flag report giornaliero creato su Render')
        else:
            print(f'❌ Errore flag report: {response2.status_code} - {response2.text}')
    except Exception as e:
        print(f'❌ Errore report: {e}')

    print('🎯 Recovery dovrebbe fermarsi in max 30 secondi!')
    print('📱 Monitorizza Telegram per confermare che i messaggi si fermano')

if __name__ == "__main__":
    create_render_flags()
