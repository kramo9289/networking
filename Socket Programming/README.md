Kevin Ramos
111019436
URL: http://localhost:6969/HelloWorld.html

Running the code:
Run the module 
The shell will print out a message that it is ready to accept up to 6 clients. This is where clients are able to connect
using the localhost:6969.

**Note, refreshing will not work for some reason so please enter the url everytime thanks :)

I have decided on port number 6969 because
"the numerology number 69 is a number of idealism, family, and harmony. It's also a number of health and compassion."
GOTO https://affinitynumerology.com/number-meanings/number-69-meaning.php for more information

Code description:
-My code creates a new thread for each client that connects to the server.
 
-If the client requests the correct file from the server, then it will also generate a 5 second timer which
will show that there are multiple threads running. This can be seen in the shell when it prints the appropriate information

-If the client requests an incorrect file from the server, then it will immediately send a 404 Not found message and the 
appropriate html file with the 404 message. There is also a 5 second timer for the thread that requested an inccorect file

-My code will print out the number of threads that are currently used as well as information regarding the current threads in use.

Screenshots:
-There are two screenshots in this zip file
-pass.png shows two browsers getting the response from the server for HelloWorld.html
-fail.png shows one browser getting the HelloWorld.html file and the other getting a 404 not found msg because it requested a file that did not exist