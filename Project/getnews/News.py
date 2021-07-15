
from classnewsfeed import newsfeed
import csv

def bubbleSort(arr,arr1):
	n = len(arr)
	for i in range(n-1):
   
		for j in range(0, n-i-1):
			if int(arr[j]) < arr[j+1] :
				arr[j], arr[j+1] = arr[j+1], arr[j]
				arr1[j],arr1[j+1]=arr1[j+1],arr1[j]
	return arr1
topics=['Sports','Business','Health','Entertainment','Science','Technology','Nation']
location=['Australia','Brazil','China','France','Germany','India','Italy','Japan','Russia','Saudi Arabia','Singapore','South Africa','United Kingdom','United States']


for i in location:
	news=[]
	for j in topics:
		a=newsfeed(j,i)
		k=a.url()
		news+=[k]
	with open("C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+i+'.csv','w',encoding="utf-8") as newfile:
		csv_writer=csv.writer(newfile)
		csv_writer.writerows(news)
news1=[]
for i in location:
	a=newsfeed("World",i)
	k=a.url()
	news1+=[k]
with open("C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+"World.csv","w",encoding="utf-8") as newfile:
	csv_writer=csv.writer(newfile)
	csv_writer.writerows(news1)





