import requests
import json
from bs4 import BeautifulSoup
def space_remove(string):
    if string[0] == " ":
        string = string[1:]
    return string
class serial:
    #def __init__(self, tittle,original,desc, genres_ids, actors_ids,author_id,status,channel_id,thumb,timing,rating):
        '''
        self.tittle = tittle
        self.original = original
        self.desc = desc
        self.genres_ids = genres_ids
        self.actors_ids = actors_ids
        self.author_id = author_id
        self.status = status
        self.channel_id = channel_id
        self.thumb = thumb
        self.timing = timing
        self.rating = rating
        '''

class season:
    def __init__(id,serial_id,tittle):
        self.id = id
        self.serial_id = serial_id
        self.tittle = tittle

class episode:
    def __init__(id,season_id,number,tittle,original,date):
        self.id = id
        self.season_id = season_id
        self.number = number
        self.tittle = tittle
        self.original = original
        self.date = date

if __name__ == "__main__":
    serials = []
    seasons = []
    episodes = []
    genres = []
    authors = ["Нет данных"]
    actors = ["Нет данных"]
    statuses = []
    channels = []
    count = int(input())
    for i in range(1,count+1):
        request = requests.get("https://www.toramp.com/schedule.php?id="+str(i))
        request = request.text
        soup = BeautifulSoup(request,'lxml')
        header = soup.find('h1', {'class': 'title-basic'})
        if header == None:
            continue
        new_serial = serial()
        new_serial.tittle = soup.find('span', {'itemprop': 'name'}).text
        new_serial.original = soup.find('span', {'itemprop': 'alternativeHeadline'}).text
        header = BeautifulSoup(str(soup.find('div',{'class':'second-part-info'})),'lxml')
        content = header.div.contents
        new_serial.genres_ids = []
        for k in range(1,len(content)):
            if content[k].name == None:
                new_serial.timing = content[k].replace(' - ','')
            elif content[k].name == 'a':
                if content[k].text not in genres:
                    genres.append(content[k].text)
                new_serial.genres_ids.append(genres.index(content[k].text)+1)
        new_serial.desc = soup.find('p',{'class':'body_large summary'}).text
        serials.append(new_serial)
        header = BeautifulSoup(str(soup.find('div',{'class':'content-widget-1'})),'lxml')
        content = header.div.contents
        info2 = BeautifulSoup(str(header.find('a')),'lxml')
        print(info2.a)
        if info2.a == None:
            new_serial.authors_ids = [1]
            new_serial.actors_ids = [1]
        else:
            new_serial.authors_ids = []
            new_serial.actors_ids = []
            print("https://www.toramp.com/"+info2.a.attrs['href'])
            html2 = requests.get("https://www.toramp.com/"+info2.a.attrs['href'])
            soup1 = BeautifulSoup(html2.text,'lxml')
            blocks = soup1.findAll('div',{'class':'block_list'},'lxml')
            arr = space_remove(BeautifulSoup(str(blocks[1]),'lxml').text).split('\n')
            for j in arr:
                if j not in authors:
                    authors.append(j)
                new_serial.authors_ids.append(authors.index(j)+1)
            arr = space_remove(BeautifulSoup(str(blocks[2]),'lxml').text).split('\n')
            for j in arr:
                if j not in actors:
                    actors.append(j)
                new_serial.actors_ids.append(actors.index(j)+1)
        new_serial.channel_id = content[9].text
        if content[9] not in channels:
            channels.append(content[9].text)
        new_serial.channel_id = channels.index(content[9].text)+1
        if content[5] not in statuses:
            statuses.append(content[5].text)
        new_serial.status_id = statuses.index(content[5].text)+1
        new_serial.rating = soup.find('div',{'id':'ratStat'}).text
        header = BeautifulSoup(str(soup.find('td',{'id':'img_basic'})),'lxml')
        new_serial.thumb = header.td.img.attrs['src']
        print(i,'/',count)
    for i in range(len(genres)):
        print(i+1,genres[i])
    for i in range(len(statuses)):
        print(i+1,statuses[i])
    for i in range(len(channels)):
        print(i+1,channels[i])
    for i in range(len(authors)):
        print(i+1,authors[i])
    for i in range(len(actors)):
        print(i+1,actors[i])
    for i in serials:
        print(i.tittle,"(",i.original,")")
        print('Длительность:',i.timing)
        print('Жанры:',i.genres_ids)
        print(i.desc)
        print("Статус:",statuses[i.status_id-1])
        print(i.channel_id)
        print(i.rating)
        print(i.thumb)
        print("Авторы:")
        print(i.authors_ids)
        print("Актёры:")
        print(i.actors_ids)
        