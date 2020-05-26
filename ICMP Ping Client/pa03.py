from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

#this will be used to hold the information about the 10 pings that will be sent
pingtimeinfo = []
#this will be used to store whether a ping was lost or not (1 meaning received and 0 meaning lost)
pinglossinfo = []
dest = ""

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
        
    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff
        
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        #print(whatReady[0])
        if whatReady[0] == []: # Timeout
            pinglossinfo.append(0)
            pingtimeinfo.append(-1)
            return "Request timed out.", -1

        #change the time received to ms
        timeReceived = int(round(time.time()*1000))
        recPacket, addr = mySocket.recvfrom(1024)
        #Fill in start

        #Fetch the ICMP header from the IP packet
        #retrieve the imcp header which starts after bit 160 (20 bytes) of the ip header
        #the imcp header is 64 bits (8 bytes) 
        imcp_header = recPacket[20:28]

        #following the code from sendOnePing, unpack the struct using the imcp header
        #the format string for unpack is the same as the imcp header which consists of 2 bytes, 2 unsigned
        #shorts and a short for the sequence number. They are unpacked in the order of the icmp header
        imcpType, imcpCode, imcpChecksum, imcpId, imcpSequence = struct.unpack("2b2Hh", imcp_header)

        #If the imcpID is equal to myID, then retrieve the time sent of the packet and subtract it from the time received
        if imcpId == ID:
            #The time sent is the next 8 bytes as shown in sendOnePing
            time_sent = struct.unpack("d", recPacket[28:36])[0]
            #set the ttl global variable which will be used to print information
            ttl = struct.unpack("B", recPacket[8:9])[0]
            #since this was received append 1 to the array
            pinglossinfo.append(1)
            pingtimeinfo.append(timeReceived - time_sent)
            return timeReceived - time_sent, ttl
        #Fill in end

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            pinglossinfo.append(0)
            pingtimeinfo.append(-1)
            return "Request timed out.", -1

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0

    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    #change the time to ms
    data = struct.pack("d", int(round(time.time()*1000)))
    
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    
    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging host: " + host + " at: " + dest + " using Python:")
    print("")

    i = 0
    # Send ping requests to a server separated by approximately one second
    # Only send 10 pings
    while i < 10 :
        delay, ttl = doOnePing(dest, timeout)
        if(ttl == -1):
            print("Request timed out")
        else:
            print("Reply from " + str(dest) + ": " + "time=" + str(delay) + "ms TTL=" + str(ttl))
        time.sleep(1)# one second
        i+=1
    #return delay
    print("")
    loss = 0
    received = 0
    #get the loss information from the array
    for x in pinglossinfo:
        if(x == 0):
            loss+=1
        if(x == 1):
            received+=1
    #calculates the min max and ave of the pings
    mini = 100000000
    maxi =0
    totalamt = 0
    totalpings = 0
    for y in pingtimeinfo:
        if(y == -1):
            continue
        if(y > maxi):
            maxi = y
        if(y < mini):
            mini = y
        totalamt+=y
        totalpings+=1
    #If the total pings received is 0 then change values to n/a since there are no statistics
    percent = 0
    if(totalpings == 0):
        mini = "N/A "
        maxi = "N/A "
        avg = "N/A "
        percent = 100
    else:
        avg = totalamt/totalpings
        percent = (loss*10)
    print("Ping statistics for " + str(dest) + ":")
    print("Packets: Sent = 10, Received = "+str(received) +", Lost = "+str(loss) + " (" +"{}%".format(percent) + " loss),")
    print("Approximate round trip times in milli-seconds:")
    print("Minimum = "+str(mini)+"ms, Maximum = "+str(maxi)+"ms, Average = "+str(avg) +"ms")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
if __name__ == "__main__":
    while 1:
        print("Ping Program - This program pings a target host 10 times and retrieves information\n")
        host = input("Enter the name of the host you would like to ping: ")
        print("")
        ping(host)
        #reset the global variables
        pingtimeinfo = []
        pinglossinfo = []
        dest = ""
