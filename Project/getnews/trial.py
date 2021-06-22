from classnewsfeed import newsfeed
import csv
location=['Australia','Brazil','China','France','Germany','India','Italy','Japan','Russia','Saudi Arabia','Singapore','South Africa','United Kingdom','United States']
news1=[]
for i in location:
	a=newsfeed("World",i)
	k=a.url()
	if k not in news1:
		news1+=[k]
with open("World.csv","w",encoding="utf-8") as newfile:
	csv_writer=csv.writer(newfile)
	csv_writer.writerows(news1)