#Kevin Ramos
#CSE 310 PA01
#111019436

#import socket module
from socket import *

#Import the threading module to enable multithreading
import threading
#Import time to delay the closing of each thread to see if there is multithreading
import time

#This will be a global variable to determine how many active threads there are
numOfActiveThreads = 0

#Create the socket thread class 
class socketThread(threading.Thread):
    #To initialize a socketThread, the parameter will be the connection socket from serverSocket.accept()
    def __init__(self, cs):
        threading.Thread.__init__(self)
        self.connectionSocket = cs
    def run(self):
        try:
            #Use the global variable to determine how many sockets there are
            global numOfActiveThreads
            #Increase it by 1 bc this is a new thread
            numOfActiveThreads += 1
            #Initialize currThread which will identify this thread 
            currThread = numOfActiveThreads
            #print the thread # and say it started
            print('Thread # ' + str(numOfActiveThreads) +  ' has started')
            #message will contain everything recieved from the client
            #Get part/full message from recieve
            #Waits for socket to recv all the data
            while True:
                message = self.connectionSocket.recv(1024)
                if message != '':
                    break
            message = message.decode()
            #The whole msg has been recieved so we will now open the file
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()
            #Send one HTTP header line into socket
            httpHeader = 'HTTP:/1.1 200 OK\r\n\r\n'
            connectionSocket.send(httpHeader.encode())                        
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())                
            connectionSocket.send("\r\n".encode())
            #Close the file
            f.close()
            #Close the connection Socket
            connectionSocket.close()
            #create a timer to check if threads are working
            print('SENT A 200 OK MESSAGE TO REQUEST ')
            print(message)
            print('Closing thread # ' + str(currThread) +  ' in 5 seconds\r\n')
            time.sleep(5.0)
            print('thread # ' + str(currThread) + ' has been closed')
            numOfActiveThreads -= 1
            print('Number of threads is: ' + str(numOfActiveThreads))
        except IOError:
            #Send response message forfile not found
            print('SENT A 404 BAD MESSAGE')
            connectionSocket.send('HTTP:/1.1 404 Not Found\r\n\r\n'.encode())
            #Send the 404 html file
            f = open('404.html')
            outputdata = f.read()                       
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())                
            connectionSocket.send("\r\n".encode())
            #Close the connection
            connectionSocket.close()
            print('Closing thread # ' + str(currThread) +  ' in 5 seconds \r\n')
            time.sleep(5.0)
            print('thread # ' + str(currThread) + ' has been closed')
            numOfActiveThreads -= 1
            print('Number of threads is: ' + str(numOfActiveThreads))
            
#Local host so the ip is left blank to default to local host
hostIP = ''
#The port number that will be used for this server - I chose the number
portNum = 6969
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.bind((hostIP, portNum))

#The socket will now listen for clients on the port number
#We will listen to 6 clients at a time
serverSocket.listen(6)
print('Ready to recieve up to 6 clients.....');
threads = []

while True:
    #Establish the connection
    connectionSocket, addr = serverSocket.accept()
    #Create a thread for a new connection
        
    newSocketThread = socketThread(connectionSocket)
    #Start the thread and append it to the threads array
    newSocketThread.start()
    threads.append(newSocketThread)
   
for t in threads:
    t.join()



