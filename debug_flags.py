#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test debug del sistema flag
exec(open('555-serverlite.py').read())

print('🔍 [DEBUG] Stato flags corrente:')
for key, value in GLOBAL_FLAGS.items():
    print(f'  {key}: {value}')

print()
print('🔍 [DEBUG] Test flag functions:')
print(f'  is_message_sent_today morning_news: {is_message_sent_today("morning_news")}')
print(f'  is_message_sent_today daily_report: {is_message_sent_today("daily_report")}')
print(f'  is_message_sent_today evening_report: {is_message_sent_today("evening_report")}')

print()
print('🔍 [DEBUG] Simulo invio morning news:')
set_message_sent_flag('morning_news')
print(f'  Dopo set_flag - morning_news_sent: {GLOBAL_FLAGS["morning_news_sent"]}')
print(f'  is_message_sent_today morning_news: {is_message_sent_today("morning_news")}')

print()
print('🔍 [DEBUG] Data check:')
import datetime
current_date = datetime.datetime.now().strftime('%Y%m%d')
print(f'  current_date: {current_date}')
print(f'  last_reset_date: {GLOBAL_FLAGS["last_reset_date"]}')
print(f'  Reset needed: {current_date != GLOBAL_FLAGS["last_reset_date"]}')

print()
print('✅ [DEBUG] Test flag system completato')
