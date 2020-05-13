import requests
import lxml.html

base_url = 'https://rabota.ua/'

class RobotaUa:
    def __init__(self,base_url):
        self.base_url = base_url

    def get_info(self):
        page = 1
        flag = True
        cards = []
        while flag:
            url = '{0}/ровно?parentId={1}'.format(self.base_url,page)
            rez = requests.get(url)
            if rez.status_code==200:
                dom = lxml.html.fromstring(rez.text)
                trs = dom.xpath('//article[@class="card"]')
                # flag = len(trs)!=0
                flag = False
                for tr in trs:
                    a_s = tr.xpath("div[@class='card-body']/div[@class='card-main-content']/div[@class='common-info']/p/a[@class='ga_listing']")                        #посада  tr.xpath('a[@class="ga_listing"]')
                    kompani_trs = tr.xpath("div[@class='card-body']/div[@class='card-main-content']/div[@class='common-info']/p/a[@class='company-profile-name']")      #Компания                    
                    tr_bs = tr.xpath("div[@class='card-body']/div[@class='card-main-content']/div[@class='common-info']/span [@class='salary']")                        #ЗП
                    times = tr.xpath("div[@class='card-footer']/div [@class='publication-time']")                                                                       #Час
                    for a,tr_b,time,kompani_tr in zip(a_s,tr_bs,times,kompani_trs):
                        # kompani = kompani_tr.xpath('span')
                        # if kompani:
                        #     kompani = kompani[0]
                        cards.append(
                                {
                                    'link':base_url+a.attrib.get('href'),
                                    'title':a.text_content(),
                                    'sel':tr_b.text_content(),
                                    'kompani':kompani_tr.text_content(),
                                    'time':time.text_content()                                    
                                }
                        )
            else:
                print('Error', rez.status_code)
            page = page + 1
        return cards
robota = RobotaUa('https://rabota.ua/')
print(robota.get_info())
