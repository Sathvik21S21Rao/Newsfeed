from bs4 import BeautifulSoup
import urllib.request as m
from gnewsclient import gnewsclient as d
import time
def allow(news):
	List=[]
	Title=[]
	begin=time.time()
	r=news.get_news()

	
	for i in r:
		if len(List)==5:
			break
		try:
			List+=[m.urlopen(i['link'])]
			Title+=[i['title']]
		except:
			pass
	time.sleep(1)
	end=time.time()
	print(end-begin)

	return List,Title

class newsfeed:
	def __init__(self,topic,location):
		self.topic=topic
		self.Body=[]
		self.Title=[]
		self.links=[]
		self.image=[]
		self.location=location

	def url(self):
		news=d.NewsClient(language='english',topic=self.topic,location=self.location,max_results=10)
		List,Title=allow(news)
		y=0
		for url in List:
			image=[]
			r=''
			soup = url.read()
			soup2 = BeautifulSoup(soup, 'html.parser')
			for j in soup2('a'):
				if 'click' in (j.text).lower() or j.text=='' or 'subscribe' in (j.text).lower() or 'join' in (j.text).lower() or len(j.text)>25 or 'more' in (j.text).lower()or len(j.text)>25 or 'sign up' in (j.text).lower():
					j.decompose()
			for j in soup2('button'):
				j.decompose()
			for j in soup2('footer'):
				j.decompose()
			for j in soup2('header'):
				j.decompose()
			
			for j in soup2('span',class_='copyright'):

				j.decompose()		
			for j in soup2('span'):
				if 'sign up' in (j.text).lower() or 'subscribe' in (j.text).lower() or 'join' in (j.text).lower():
					j.decompose()

			for j in soup2('img',class_='img_ad'):
				j.decompose()
			for j in soup2('p'):
				if 'sign up' in (j.text).lower() or 'subscribe' in (j.text).lower() or 'join' in (j.text).lower():
					j.decompose()
			

			
			
			if soup2.body!=None:
				html = soup2.body.find_all('p',class_="")
			else:
				html=[]
			for i in html:
				r+=i.text
			s=[]
			end=['copyright','sign up to start','market data powered by','©','advertisement','for more sports updates','for more updates',]
			start=["Thanks for contacting us. We've received your submission.","AdvertisementSupported byAdvertisement","CBS Sports is a registered trademark of CBS Broadcasting Inc. Commissioner.com is a registered trademark of CBS Interactive Inc",]


			for j in start:
				if j in r.lower():
					r=r.replace(j,'')
			for j in end:
				if r.find(j)!=-1:
					r=r.replace(r[r.find(j):],'')
			if len(r)<100 or Title[y][Title[y].rfind('-'):] == " CNBCTV18":
				Title.pop(y)
				continue
			
				
			r=Title[y]+'\n'+r
			w=soup2.figure
			m=None
			if w!=None:
				m=w.find("img")
			P=""
			if m!=None:
				P=m.get("src")
			if P==None:
				P=""
			k=soup2.body.find_all('img')
			for i in k:
				
				image.append(i.get('src'))
			for i in image:
				try:
					if ('.jpg' in i.lower() or '.jpeg' in i.lower()) and i.startswith('http')  :
						s+=[i]
				except:
					pass
			img=r"https://cdn.pixabay.com/photo/2015/02/15/09/33/news-636978_960_720.jpg"
			if not P.startswith("http"):
				P=""
			if P!="":
				img=P
			elif s!=[]:
				for i in s:
					if i!="":
						img=i
						break
			
			if r not in self.Body:
				self.Body+=[r,img]
			img=""
			y+=1
		return self.Body
			
			
		
			
		
		

	
			
		