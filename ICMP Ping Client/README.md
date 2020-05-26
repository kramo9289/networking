Kevin Ramos
111019435
kevramos

*NOTE I have changed the time to milliseconds to replicate the ping program
for windows

The way I have implemented this program is by running a prompt in a while loop
that will ask the user for a host name (google.com etc.) The program will then
print out the information for each packet sent. This can either print out reply
information or it can print out 'request timed out'. After attempting to ping 10
times it will then print out the statistics from the the 10 pings. After printing
out the statistics, it will again prompt the user to enter a host name.

The way I implemented this was by first retrieving the information from the packet
recieved. I retrieved the imcp header by taking bytes 28-36 (corresponding to the 
8 bytes after bit 160) of the recPacket. I think unpacked the header using struct.unpack
following closely what sendOnePing() packed. I also retrieved the TTL of the packet
which is an unsigned char at byte 8.

I created 3 global variables that are used in the program. pingtimeinfo is an array
that will store the rtt of the packets as they are retrieved. If there is a timeout
then a -1 will be appended to indicate that there was a timeout. pinglossinfo is an 
array that stores either 0 or 1. 0 indicates that there was a time out and 1 indicates
that for that ping, there was a reply from the host. dest will hold the information of
the ip. 

In ping() there is a while loop that calls doOnePing() 10 times. It either prints out
'request timed out' or information for each ping. After completing the 10 pings and
gathering information using the global variables, my program prints out the ping statistics
for the 10 pings. This is done by iterating through the 2 global arrays. pinglossinfo
contains 10 zeros or ones. I use this to calculate the loss percentage. pingtimeinfo
contains 10 rtts or -1s. I use this to calculate the avg, min and max of the pings.

I printed the information in a way that it closely resembles the ping command in windows
which I used to make sure that my program was gathering the correct information.