
# Ahmad Allan
# Project 2: HTML Parser with Multithreading
# Date: 03/16/2020

#Import librariaries important to this project like HTML parser which
#will help us find image objects and socket libraries to connect to the
#desired website and download its info

from html.parser import HTMLParser
import socket
import os
from os import path
import threading
import time
import sys

exitFlag = 0
x_count=1

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, url):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.url=url
    def run(self):
        print_time(self.name, 1, self.counter, self.url)
      
def print_time(threadName, counter, delay, url):
    while counter:
        if exitFlag:
            threadName.exit()

        #find file name and extention in order to make folder and subfolders
        whileCounter = 0
        finalPath = ""

        aa=url.split('//')
        bb=aa[2]
        counterr = bb.count("/")
        extension_file = bb.split("/")
        imagePath = os.getcwd()

        while whileCounter < counterr:
            finalPath += extension_file[whileCounter] + "/";
            whileCounter += 1;

        try:
            os.makedirs(imagePath + "/" + finalPath)
        except:
            pass

        file_image = open (imagePath + "\\" + bb, 'wb');


        #establish a new socket for image and connect to it
        s_image = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_image.connect((host_ip, 80))

        #GET statement to be sent to server (after converting to bytes)
        request_pic = "GET {} HTTP/1.0\r\n\r\n".format(url)
        my_request_as_bytes_2 = str.encode(request_pic)
        s_image.send(my_request_as_bytes_2)


        #recv data/response back from server (high buffer size woked best)
        #This first receive will be overwritten (server response)
        result_2 = s_image.recv(100000)

        #establish an accumulator variable to get data from server
        result_total_2=b''

        # continuos while loop until there are no data left
        while (len(result_2) > 0):

            #Frist real data(actual datat not server response)
            result_2 = s_image.recv(100000)

            #add results in accumulator as we get them from server
            result_total_2=result_total_2+result_2

        #write results in html file    
        file_image.write(result_total_2)

        #close html file
        file_image.close()
         
        counter -= 1
        print(threadName)
        print("--- %s seconds ---" % (time.time() - start_time))


#Ask the user to input the website name
website=input('Input website to parse (html only): ')

start_time = time.time()

print("\nwebsite is: ",website)

#create directrory path in desktop
Desktop=os.getcwd()
cName = os.path.join(Desktop, "Website.html")

print(cName)

#Open Html file for writing bytes              
file_html=open(cName,'wb')

#HTML parser class
class MyHTMLParser(HTMLParser):

    #used to find start tage, especially the one we are interested in 'img'
    def handle_starttag(self, tag, attrs):
        global Desktop
        global x_count
        global hala
        if tag=="img":

            #if statement to check if image link already has the website link at the beginning
            if(dict(attrs)["src"][0]=='h' and dict(attrs)["src"][1]=='t'):
                url=dict(attrs)["src"]

            #If it didn't have it, we add it in
            else:
                url=web_pic+'/' + dict(attrs)["src"]

            print("\npicture found, URL is: ",url,"\n")
            x_count+=1
            thread2= myThread(x_count, "Thread-"+str(x_count), 0, url)
            thread2.start() 

        #To download images exlusively
        elif hala==1:
            chris_the_counter=1
            chris_the_website=web_pic
            while chris_the_counter<len(x):

                chris_the_website+='/'
                chris_the_website=os.path.join(chris_the_website, x[chris_the_counter])
                chris_the_counter+=1
            url=chris_the_website
            hala=0
            threadz= myThread(100, "Thread-100", 0, url)
            threadz.start() 
        else:
            #Skip function if no image found
            pass

#open socket    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#simple_web is used to get the IP address of the website
#using the gethostbyname function later on
#In order to use gethostbyname, wee need the basic website
#without http or any other things

simple_web=website
simple_web=simple_web.replace('http://',"")
x=simple_web.split('/')
simple_web=x[0]

    
# get host ip from simple_web
host_ip = socket.gethostbyname(simple_web)
print('host_ip is: ', host_ip)

#connect to socket using port 80 and host ip
s.connect((host_ip, 80))

#send request to server in bytes for the website
request = "GET {} HTTP/1.0\r\n\r\n".format(website)
my_request_as_bytes = str.encode(request)
s.send(my_request_as_bytes)

#listen for server response (first on is going to be 200 ok if program works)
#This will be overriden later
result = s.recv(100000)

#establish an accumulator variable to get data from server
result_total=b''

# continuos while loop until there are no data left
while (len(result) > 0):
    result = s.recv(100000)
    result_total=result_total+result

#write accumulated data to html file  
file_html.write(result_total)

#close html file
file_html.close()

# some websites have indexed names like webpages.eng.wayne.edu/~ae4849/
# that are needed for image url
# using these if statement we can preserve it if it exists
if len(x)>2:
    if x[1][0]=='~':
        web_pic='http://'+x[0]+'/'+x[1]
    else:
        web_pic='http://'+x[0]+'/'
else:
    web_pic='http://'+x[0]+'/'

hala=0

#If only a picture was found
try:
    x[-1][-4]
    if x[-1][-4]==".":
        hala=1
except:
    hala=2

#call parser function   
parser = MyHTMLParser()

#feed data to parser function
parser.feed(str(result_total))
            
#prints after program is finished
print("\n\n\n\nIm done\n\n\n\n\n")

#Print Main thread time
print("Main thread time")
print("--- %s seconds ---" % (time.time() - start_time))



