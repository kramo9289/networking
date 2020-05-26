Kevin Ramos
111019436
CSE 310 PA02

The global variables that I decided to use in my implementation for the sending side records the previous packet
that A sent and the current sequence number (1 or 0). The global variable used for the recieving side (B) is the
last sequence number that was correctly recieved. This will help when B side is sending a ACK/NACK packet to A.

A_init:
The only thing that needs to be initialized is the current sequence number for A. The first packet that will
be sent will be a 0 packet.

B_init: 
The only thing that will be initialized is the last good sequence number recieved for B. It will be set to 0

A_output:
I first create a packet based on the message recieved from layer 5. I use the A_currSeqNum for the sequence number 
and the ack num (the ack num is not necessary as this is a one directional). I create checksum using the ints and 
looping through the payload, adding each char as an int to checksum. I then set the A_prevPkt to the one just
created and set the end of the payload to a NULL terminator (better for printf) I print out information which 
will describe the packet along with the source and destination. I send the packet to B and start a time for 20
units

A_input:
I disect the packet information recieved. I use checksum for corruption check. If it is corrupted it will print 
appropriate infromation. The code then waits for the timer to expire to resend the information. If it is not a 
corrupted ACK packet then I check to see if it is the expected ACK or a NACK using the A side global variable
A_currSeqNum. If it is a ACK then I print that the packet was recieved without problem and set A_currSeqNum to 
the opposite of the packets ACK (the ACK and SEQ nums are the same for a B side packet because it doesn't matter
as it's one direction send/recieve). If it is a NACK packet then I print the appropriate information and wait for
the timer to expire

A_timerinterrupt:
I print appropriate information on the timer expiring and retransmit the packet using the A side global variable
A_prvPkt. I also restart the timer for A

B_input:
I disect the packet recieved from A and check for corruption using checksum. If it is a corrupted packet I send
a NACK packet to A using the opposite (1 or 0) of the B side global variable B_lastRecGoodSeq. If there is no 
corruption and everything checks out, I send the message to layer 3 and send an ACK packet to A. I also send
the B side global variable to B_lastRecGoodSeq to the sequence number from the good packet. I print the 
appropriate information
