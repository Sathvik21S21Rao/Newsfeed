import sys
import csv
import ctypes as ct

def bubbleSort(arr,arr1):
	n = len(arr)
	for i in range(n-1):
   
		for j in range(0, n-i-1):
			if int(arr[j]) < arr[j+1] :
				arr[j], arr[j+1] = arr[j+1], arr[j]
				arr1[j],arr1[j+1]=arr1[j+1],arr1[j]
	return arr1
def descending():
	for i in ['Australia','Brazil','China','France','Germany','India','Italy','Japan','Russia','Saudi Arabia','Singapore','South Africa',"United States","United Kingdom"]:
		with open(i+'.csv','r',encoding="utf-8",errors="ignore") as file:
			file_reader=csv.reader(file)
			k=[]
			for line in file_reader:
				k+=line
		COUNT=[]
		news1=[]

		keyword=input("Enter Keyword:").lower()
		for i in k:

			if keyword in i.lower():
				count=(i.lower()).count(keyword)
				COUNT.append(count)
				news1.append(i)
		return bubbleSort(COUNT,news1)
for i in descending():
	print(i)
	