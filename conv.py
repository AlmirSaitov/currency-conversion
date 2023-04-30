import os
import requests
import json
import time

if not os.path.exists('currency_rates'):
    os.mkdir('currency_rates')

# Создаем словарь для хранения курсов валют
currency_rates = {}

# Читаем данные из файлов и сохраняем курсы валют в словарь
for file_name in os.listdir('currency_rates'):
    if file_name.endswith('_rate.txt'):
        with open(os.path.join('currency_rates', file_name)) as f:
            currency_code = file_name.split('_')[0]
            currency_rate = float(f.read())
            currency_rates[currency_code] = currency_rate

# Получаем текущие курсы валют с API ЦБ РФ
while True:
    try:
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url)
        data = json.loads(response.text)
        for currency_code, currency_data in data['Valute'].items():
            currency_rate = currency_data['Value']
            file_name = os.path.join(
                'currency_rates', f"{currency_data['CharCode']}_rate.txt")
            with open(file_name, 'w') as f:
                f.write(str(currency_rate))
                currency_rates[currency_data['CharCode']] = currency_rate
        break
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при получении курсов валют: {e}')
    time.sleep(5)

# Выводим список доступных валют
print('Доступные валюты:')
for currency_code in currency_rates:
    print(currency_code)

# Запрашиваем у пользователя данные для конвертации
while True:
    try:
        currency_from = input(
            'Введите название валюты, которую хотите конвертировать: ')
        currency_to = input(
            'Введите название валюты, в которую хотите конвертировать: ')
        amount = float(input('Введите сумму, которую хотите конвертировать: '))
        break
    except ValueError:
        print('Ошибка: введите корректное значение')

# Рассчитываем конвертированную сумму
converted_amount = amount * \
    currency_rates[currency_from] / currency_rates[currency_to]

# Выводим результат
print(f'{amount} {currency_from} = {converted_amount} {currency_to}')
