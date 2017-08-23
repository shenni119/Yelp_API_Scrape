import urllib3
from bs4 import BeautifulSoup
import pandas as pd
from pandas.compat import u
import csv
import time
import html

# In[356]:

names=[]
n_addresses=[]
phones=[]
types=[]

csvfile = open("02111_02116_1000busi_url.csv",'r')
reader = csv.reader(csvfile, delimiter=',')

outfile4 = open("business_types.csv","w")
outfile4.write("name,phone,type\n")

loop_lim=3
loop_lim2=20
# In[357]:
n=0
for yelp_link in reader:
    busi_name=yelp_link[0]
    busi_phone=yelp_link[1]
    url = yelp_link[2]
    if 'https' not in url:
        continue
    n+=1
    if n<loop_lim2:
        continue
    # if n==loop_lim2:
    #     break
    #print (url)
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    soup = BeautifulSoup(r.data,'html.parser')
    #print (soup)
    div_subheaders= soup.find("div", attrs={"class":"biz-page-subheader"})
    print (busi_name)
    #print (div_subheaders)
    try:
        span_title =div_subheaders.find("span",attrs={"class":"hidden"})
        #print (span_title)
        html_type = span_title.find("span", attrs={"itemprop":"title"})
#        busi_type=html_type.findALL(text=True)
        print ("try worked!!!!")
    except:
        html_type = soup.find("span", attrs={"itemprop":"title"})
#        busi_type=html_type.findALL(text=True)
        print ("try failed??????")
    print (html_type)
    #print (type(span_title))
    #print (len(span_title))
    #print(busi_type.findALL(text=True))
#phone = r_phone.replace("\r\n","").replace("\n","").replace("  ","")
    time.sleep(.3)
    outfile4.write("{},{},{}\n".format(busi_name,busi_phone,html_type))
outfile4.close()

csvfile = open("business_types.csv",'r')
reader = csv.reader(csvfile, delimiter=',')

outfile5 = open("business_types_final.csv","w")
outfile5.write("name,phone,type\n")

for yelp_link in reader:
    busi_name=yelp_link[0][2:][:-1]
    busi_phone=yelp_link[1]
    busi_type = html.unescape(yelp_link[2]).replace('<span itemprop="title">','').replace('</span>','')
    outfile5.write("{},{},{}\n".format(busi_name,busi_phone,busi_type))
outfile4.close()
