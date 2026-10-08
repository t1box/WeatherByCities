import json
import sys
import urllib.request
import urllib.parse
from dataclasses import dataclass


# 3. Модель с обязательными полями
@dataclass
class WeatherData:
    city: str
    temp_c: int
    country: str


# 1. Загрузка городов из файла в память (без пустых строк и дублей, порядок сохраняем)
def load_cities(path):
    cities = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            city = line.strip()
            if city and city not in cities:
                cities.append(city)
    return cities


# 2. Запрос к API wttr.in для одного города
def get_weather(city):
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    request = urllib.request.Request(url, headers={"User-Agent": "curl"})
    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))

    temp_c = int(data["current_condition"][0]["temp_C"])
    country = data["nearest_area"][0]["country"][0]["value"]
    return WeatherData(city=city, temp_c=temp_c, country=country)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cities = load_cities("cities.txt")

    # 4. Получаем и выводим погоду по каждому городу
    weather_list = []
    print("Погода по городам:")
    for city in cities:
        try:
            w = get_weather(city)
        except Exception as e:
            print(f"{city}: не удалось получить данные ({e})")
            continue
        weather_list.append(w)
        print(f"{w.city}, {w.country} {w.temp_c:+d} °C")

    # 5. Группировка по странам
    by_country = {}
    for w in weather_list:
        by_country.setdefault(w.country, []).append(w.temp_c)

    print("\nСтатистика по странам:")
    for country, temps in by_country.items():
        avg = round(sum(temps) / len(temps))
        print(f"{country} — {len(temps)} cities, "
              f"avg: {avg:+d} °C, min: {min(temps):+d} °C, max: {max(temps):+d} °C")


if __name__ == "__main__":
    main()
