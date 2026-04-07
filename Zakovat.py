import requests
from bs4 import BeautifulSoup

def Savollar(id):
    url = f"https://api.zakovatklubi.uz/v1/package/questions?_l=uz&include=isChosen&filter%5Bpid%5D={id}&sort=-id&page=1"

    response = requests.get(url)

    questions = response.json()

    savollar = []
    javoblar = []

    data = questions['data']
    totalCount = questions['meta']['totalCount']
    needed = totalCount
    while not needed == 0:
        for i in range(20):
            items = data[i]['items']
            question = items[0]['text']
            javoblar.append(items[0]['answer'])

            soup = BeautifulSoup(question, 'html.parser')
            savollar.append(soup.get_text(separator=" ", strip=True))
            needed -= 1

        url = f"https://api.zakovatklubi.uz/v1/package/questions?_l=uz&include=isChosen&filter%5Bpid%5D={id}&sort=-id&page=2"

        response1 = requests.get(url)

        questions1 = response1.json()
        data1 = questions1['data']
        for b in range(needed):
            items = data1[b]['items']
            question = items[0]['text']
            javoblar.append(items[0]['answer'])

            soup = BeautifulSoup(question, 'html.parser')
            savollar.append(soup.get_text(separator=" ", strip=True))
            needed -= 1

    return savollar, javoblar

if __name__ == "__main__":
    savollar, javoblar = Savollar(1245)
    print(javoblar)