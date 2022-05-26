import requests


TOKEN = '2619421814940190'
urls = [
    f'https://www.superheroapi.com/api.php/{TOKEN}/search/Hulk',
    f'https://www.superheroapi.com/api.php/{TOKEN}/search/Thanos',
    f'https://www.superheroapi.com/api.php/{TOKEN}/search/Captain%America',
]


def requests_get(url_all):
    r = (requests.get(url) for url in url_all)
    return r


def parsing():
    super_hero = []
    for x in requests_get(urls):
        intelligence = x.json()
        try:
            for power_stats in intelligence['results']:
                super_hero.append({
                    'name': power_stats['name'],
                    'intelligence': power_stats['powerstats']['intelligence']})

        except KeyError:
            print(f"Проверте ссылки urls: {urls}")

    intelligence_super_hero = 0
    name = ''
    for intelligence_hero in super_hero:
        if intelligence_super_hero < int(intelligence_hero['intelligence']):
            intelligence_super_hero = int(intelligence_hero['intelligence'])
            name = intelligence_hero['name']

    print(f"Самый интеллектуальный - {name}, интеллект равен: {intelligence_super_hero}.")


class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.header = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token}'
        }

    def get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        param = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=self.header, params=param)
        return response.json()

    def upload(self, disk_file_path, file_name):
        href = self.get_upload_link(disk_file_path).get('href', ' ')
        response = requests.put(href, data=open(file_name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Файл успешно создан!')


if __name__ == '__main__':
    parsing()
    print()
    token = input('Введите токен: ')
    file_name = input('Имя файла для загрузки на ЯДиск: ')
    disk_file_path = input('Путь на ЯДиске: ')
    uploader = YaUploader(token)
    uploader.upload(disk_file_path, file_name)

