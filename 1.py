from bs4 import BeautifulSoup
import requests, json, re

url = "https://cars.av.by/"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}


req = requests.get(url, headers)
scr = req.text

#with open('av.by.html', 'w') as file:
#  file.write(scr)
with open('av.by.html') as file:
   src = file.read()
soup = BeautifulSoup(src, 'lxml')
all_cars_brends = soup.find_all(class_='catalog__title')
all_cars_brends_hrefs = soup.find_all(class_='catalog__link')
all_cars_brends_dict = dict(zip([i.text.replace(' ', '_') for i in all_cars_brends], ['https://cars.av.by' + j.get('href') for j in all_cars_brends_hrefs]))

#print(all_cars_brends_dict)
with open('all_brends_dict.json', 'w') as file:
   json.dump(all_cars_brends_dict, file, indent=4, ensure_ascii=False)
with open('all_brends_dict.json') as file:
    all_brends = json.load(file)
count = 0
co = 0
for brend_name, brend_href in all_brends.items():
    if count == 0:
        req_ = requests.get(url=brend_href, headers=headers)
        src_ = req_.text

        # with open(f'data/{count}_{brend_name}.html', 'w') as file:
        #     file.write(src_)
        # with open(f'data/{count}_{brend_name}.html') as file:
        #     src_ = file.read()
        soup = BeautifulSoup(src_, 'lxml')
        brend_models_title = soup.find_all(class_='catalog__title')
        brend_models_hrefs = soup.find_all(class_='catalog__link')
        brend_model_dict = dict(zip([i.text.replace(' ', '_') for i in brend_models_title],
                                        ['https://cars.av.by' + j.get('href') for j in brend_models_hrefs]))
        #print(brend_model_dict)
        for model_title, model_href in brend_model_dict.items():
            if co == 0 or co == 1:
                req__ = requests.get(url=model_href, headers=headers)
                src__ = req__.text
                soup_model = BeautifulSoup(src__, 'lxml')
                model_car = soup_model.find_all(True, {'class': ['listing-top__title-link', 'listing-item__link']})
                model_car_href = ['https://cars.av.by' + item.get('href') for item in model_car]

                model_car_to_string = [(str(i)) for i in model_car ]
                print(len(model_car_to_string), model_car_to_string)
                for _string in model_car_to_string:
                    list_find_title = re.findall(r'(\>[\w,\s]+<)', _string)
                    print(list_find_title)
                    list_deployed = []
                    for item in list_find_title:
                        if item != '>\xa0<' and item != '> <':

                            list_deployed.append(item[1:-1])
                        for item in model_car_href:
                            req__ = requests.get(url=item, headers=headers)
                            src__ = req__.text
                            soup_model = BeautifulSoup(src__, 'lxml')
                            equipment = soup_model.find_all(class_='card__price-primary')
                            card_title = soup_model.find_all(class_='card__title')
                            for i in equipment:
                                a = str(i.text[:-2])
                                b = ''.join(a.split())
                                print(b)

                        print(f'{list_deployed} =')





                co +=1
        count += 1