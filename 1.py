from bs4 import BeautifulSoup
import requests, json
url = "https://cars.av.by/"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}
#req = requests.get(url, headers)
#scr = req.text
#print(src)
#with open('av.by.html', 'w') as file:
#    file.write(scr)
#with open('av.by.html') as file:
#    src = file.read()

#soup = BeautifulSoup(src, 'lxml')
#all_cars_brends = soup.find_all(class_='catalog__title')
#all_cars_brends_hrefs = soup.find_all(class_='catalog__link')
#all_cars_brends_dict = dict(zip([i.text.replace(' ', '_') for i in all_cars_brends], ['https://cars.av.by' + j.get('href') for j in all_cars_brends_hrefs]))

#print(all_cars_brends_dict)
#with open('all_brends_dict.json', 'w') as file:
#    json.dump(all_cars_brends_dict, file, indent=4, ensure_ascii=False)
with open('all_brends_dict.json') as file:
    all_brends = json.load(file)
count = 0
for brend_name, brend_href in all_brends.items():
    if count == 0:
         req_ = requests.get(url=brend_href, headers=headers)
         src_ = req_.text

         with open(f'data/{count}_{brend_name}.html', 'w') as file:
             file.write(src_)
         with open(f'data/{count}_{brend_name}.html') as file:
             scr_ = file.read()

         count += 1