from bs4 import BeautifulSoup
import requests, json, re, csv


def get_html(_url, _headers):
    req = requests.get(_url, _headers)
    return req.text


def refined(_string):
    return _string.text.split(', ')


def index_error(list_name, parm):
    try:
        return list_name.append(parm)
    except IndexError:
        return list_name.append('')


def write_csv(file_name, parm, row):
    with open(file_name, parm) as file:
        writer = csv.writer(file)
        writer.writerow(row)


def dollar_str(data):
    for i in data:
        return ''.join(str(i.text[1:-2]).split())


def ball_rubl_str(data):
    for i in data:
        return ''.join(str(i.text[:-2]).split())


def main():
    url = "https://cars.av.by/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"
    }
    csv_headers = (
                'link',
                'brend',
                'model',
                'generation',
                'cost_bell',
                'cost_doll',
                'year',
                'gearbox',
                'engine_volume',
                'fuel',
                'mileage',
                'city',
                'body_type',
                'drive_train',
                'color',

            )

    soup = BeautifulSoup(get_html(url, headers), 'lxml')
    all_cars_brends = soup.find_all(class_='catalog__title')
    all_cars_brends_hrefs = soup.find_all(class_='catalog__link')
    all_cars_brends_dict = dict(zip([i.text.replace(' ', '_') for i in all_cars_brends],
                                    ['https://cars.av.by' + j.get('href') for j in all_cars_brends_hrefs]))

    with open('all_brends_dict.json', 'w') as file:
       json.dump(all_cars_brends_dict, file, indent=4, ensure_ascii=False)
    with open('all_brends_dict.json') as file:
        all_brends = json.load(file)
    write_csv('all_cars.csv', 'w', csv_headers)

    for brend_name, brend_href in all_brends.items():
        soup = BeautifulSoup(get_html(brend_href, headers), 'lxml')
        brend_models_title = soup.find_all(class_='catalog__title')
        brend_models_hrefs = soup.find_all(class_='catalog__link')
        brend_model_dict = dict(zip([i.text.replace(' ', '_') for i in brend_models_title],
                                        ['https://cars.av.by' + j.get('href') for j in brend_models_hrefs]))

        for model_title, model_href in brend_model_dict.items():
            soup_model = BeautifulSoup(get_html(model_href, headers), 'lxml')
            model_car = soup_model.find_all(True, {'class': ['listing-top__title-link', 'listing-item__link']})

            for item in model_car:
                list_deployed = []
                list_deployed.append('https://cars.av.by' + item.get('href'))
                _string = str(item)
                list_find_title = re.findall(r'(\>[^<]+<)', _string)

                for _item in list_find_title:
                    if _item != '>\xa0<' and _item != '> <':
                        list_deployed.append(_item[1:-1].replace('· ', ''))

                if len(list_deployed) == 3:
                    list_deployed.append('')
                hrefs = list_deployed[0]
                soup_model = BeautifulSoup(get_html(hrefs, headers), 'lxml')
                cost_bel = soup_model.find_all(class_='card__price-primary')
                cost_dollar = soup_model.find_all(class_='card__price-secondary')
                params = soup_model.find_all(class_='card__params')
                description = soup_model.find_all(class_='card__description')
                city = soup_model.find_all(class_='card__location')
                list_deployed.append(ball_rubl_str(cost_bel))
                list_deployed.append(dollar_str(cost_dollar))

                for i in params:
                    list_params = refined(i)
                    index_error(list_deployed, list_params[0][:-3])
                    index_error(list_deployed, list_params[1])
                    index_error(list_deployed, (list_params[2][:-2]))
                    index_error(list_deployed, list_params[3])
                    index_error(list_deployed, list_params[4].replace('\u2009', '')[:-3])

                for i in city:
                    list_deployed.append(i.text)

                for i in description:
                    list_description = refined(i)

                    if len(list_description) == 3:
                        list_description[1], list_description[2] = list_description[2], list_description[1]

                    for _ in list_description:
                        list_deployed.append(_)

                write_csv('all_cars.csv', 'a', list_deployed)
                print(list_deployed)


if __name__ == '__main__':
    main()



