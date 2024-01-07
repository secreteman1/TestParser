import requests
from bs4 import BeautifulSoup as BS
import translators as ts

r = requests.get("https://fow.kr/stats")
html = BS(r.content, 'html.parser')

characters = []

for a in html.select('[position=jungle]'):
    information = a.select('.td_rate') 
    if information and float(information[0].text.strip('%')) > 51 and int(information[3].text.replace(',', '')) > 100000:
        try:
            name_translation = ts.translate_text(a['rname'], from_language='ko', to_language='ru')
            matches_played = int(information[3].text.replace(",", ""))
            information_value = float(information[0].text.strip('%').replace(",", ""))
            characters.append({
                'name': name_translation,
                'wins': information_value,
                'matches_played': matches_played
            })
        except Exception as e:
            print(f"Произошла ошибка при переводе или извлечении данных: {e}")
sorted_characters = sorted(characters, key=lambda x: (-x['matches_played'], -x['wins']))

for character in sorted_characters[:5]:
    print(f"{character['name']} - Винрейт: {character['wins']}%, Количество матчей: {character['matches_played']}")
