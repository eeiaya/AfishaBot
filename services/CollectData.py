
import requests
import json


class CollectData:

    # общая функция для сбора данных
    def collect(self, event_type, output_file, pages):
        # результирующий список, где будем хранить наши объекты с нужными нам данными
        all_events = []

        for page in range(1, pages + 1):
            # собираем общий url запроса
            url = f'https://www.culture.ru/_next/data/yo72uJqt_z-kY1sWLY5Vq/afisha/vladimirskaya-oblast-vladimir/{event_type}.json?page={page}&locale=vladimirskaya-oblast-vladimir&pathParams={event_type}'
            # обращаемся к сайту с запросом по данному url'у
            response = requests.get(
                url=url,
            )

            # сохраняем ответа в формате JSON
            data = response.json()
            # добираемся в объекте до списка с событими items[]
            events = data.get('pageProps', {}).get('events', {}).get('items', [])

            for event in events:
                # забираем нужные нам данные
                full_name = event.get('title')
                price_min = event.get('priceMin')
                author_name = event.get('thumbnailFile', {}).get('meta', {}).get('author')
                place_title = event.get('topPlaceTitle')
                microdata = json.loads(event.get('microdata', '{}'))
                event_link = microdata.get('url')
                # добавляем в массив объекты подставляя вытащенные данные в нужные поля
                all_events.append(
                    {
                        'name': full_name,
                        'priceMin': price_min,
                        'author': author_name,
                        'place': place_title,
                        'link': event_link
                    }
                )
        #записываем в файл наш список в формате JSON
        with open(output_file, 'w') as file:
            json.dump(all_events, file, indent=4, ensure_ascii=False)

    # вызываем функцию собирая данные о концертах в файл kontserti.json
    def collect_data_concerts(self):
        self.collect(event_type='kontserti', output_file='storage/kontserti.json', pages=3)

    # вызываем функцию собирая данные о концертах в файл spektakli.json
    def collect_data_perfomances(self):
        self.collect(event_type='spektakli', output_file='storage/spektakli.json', pages=2)

    # вызываем функцию собирая данные о концертах в файл vistavki.json
    def collect_data_exhibitions(self):
        self.collect(event_type='vistavki', output_file='storage/vistavki.json', pages=3)