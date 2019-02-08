import requests
import bs4
from requests.adapters import HTTPAdapter
from urllib import parse
import csv


def get_website(url):
    session = requests.Session()
    session.verify = False
    adapter = HTTPAdapter(max_retries=0)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        req = session.get(url, timeout=30, allow_redirects=False, headers={'Accept-Encoding': 'identity'})

        if 'Content-Type' in req.headers:
            headers = req.headers['Content-Type']

            if headers == 'text/html':
                return req
            else:
                return False
        else:
            return False
    except (requests.ConnectionError,requests.Timeout) as e:
        print("[WARNING] Couldn't connect. Error: " + str(e))
        return False


def find_metrika_ids(code):
    # Start BS4 magic
    soup = bs4.BeautifulSoup(code.text, "html.parser")

    # Get all images
    images = soup.find_all('img')

    # Get all links
    links = soup.find_all('a')

    metrika_ids = []

    # Search for image version of Metrika
    for image in images:
        src = image.get('src', [])

        if 'mc.yandex' in src:
            splitted = src.split('/')
            if splitted[4].isdigit:
                img_id = splitted[4].split('?')
                metrika_ids.append(img_id[0])

    # Search for link version of Metrika
    for link in links:
        href = link.get('href', [])

        if 'mc.yandex' in href or 'metrika.yandex' in href:
            if id in parse.parse_qs(parse.urlparse(href).query):
                href_id = parse.parse_qs(parse.urlparse(href).query)['id'][0]
                if href_id.isdigit:
                    metrika_ids.append(href_id)

    # Make list of just unique IDs
    metrika_ids = list(set(metrika_ids))

    return metrika_ids


def check_open_metrika(ids):
    open_metrika = []
    for id in ids:
        metrika_url = 'https://metrika.yandex.ru/dashboard?id=' + id

        html_code = get_website(metrika_url)

        if html_code is not False and html_code.status_code == 200:
            soup = bs4.BeautifulSoup(html_code.text, "html.parser")

            if soup.find_all("span", {"class": "counter-toolbar__name"}):
                print("Metrika is open!")
                open_metrika.append(metrika_url)

    return open_metrika


def save_unprocessed(sites):
    file = open("unprocessed.txt", "w+")

    for site in sites:
        file.write(site + "\n")

    file.close()


def save_csv_row(row):
    file = open('results.csv', 'a', newline='')
    writer = csv.writer(file, delimiter=',')

    # Write CSV headers
    writer.writerow(row)
    file.close()
