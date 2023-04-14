import configparser
import logging
import socket 
import json

#reads the config file
config = configparser.ConfigParser()
config.read("3461-Project2.conf")


#sets up the logging file
logging.basicConfig(filename="clientLogFile.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
logger=logging.getLogger()
logger.setLevel(logging.DEBUG) 


#read the serverHost and serverPort 
serverHost = config.get('project2', 'serverHost')
serverPort = config.getint('project2', 'serverPort')
logging.info("Host address:" + serverHost)
logging.info("Port number:" + str(serverPort))


#read log details
logFile = config.get('logger', 'logFile')
logLevel = config.get('logger', 'logLevel')
logFileMode = config.get('logger', 'logFileMode')


# create a socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.info("Opened TCP socket")

# This is the “3-way handshake” since we’re using TCP. 
clientSocket.connect((serverHost, serverPort))

#loops till user quits
while True:

    #Gets user input
    phrase= input()
    print("Entered string: " + phrase)
    logging.info("Entered string: " + phrase)

    #intializes variables
    words = []
    beginning=0
    end=0
    noSpace=True

    #if string is one word
    if len(phrase) <=1:
        output= phrase
    
    else:
        #parses through string
        for x in phrase:
            end=end+1 #contains value of last character thats stored in the list
            if (x.isspace()) == True:
                noSpace=False
                if len(words) == 0: #if first word of input
                    words.append(phrase[beginning:end].upper())
                else:
                    words.append(phrase[beginning:end])
                beginning=end 
            if end == len(phrase)-1 : #if the last character of input is reached, store last word in list
                if(noSpace==True): #if there is only one word in user input
                    words.append(phrase[beginning:end+1].upper())
                else:
                    words.append(phrase[beginning:end+1])    
        
        #reverses list and displays output
        words.reverse()
        output = words.pop() #first word
        request = output

    # concatenate the 2nd to the last tokens into a string, each separated by whitespace (blanks). 
    # This string will be known as the parameter 
    parameter = ""
    while len(words) > 0:
        parameter= parameter + words.pop()

    
    #creates request in dict form to covert to json
    clientRequest = {"request": request,
                     "parameter": parameter
                     }
    server_Request = json.dumps(clientRequest)

    #sends data to server
    clientSocket.sendall(server_Request.encode())

    # Receive the response
    data = clientSocket.recv(1024).decode()
    if not data:
        logging.error("Server is not responding")
        continue
    
    #converts back to python
    value= json.loads(data)

    if output == "QUIT":
            print("Response recieved: " + value["response"])
            logging.info("Response recieved: " + value["response"])
            break
    else:
        print("Response recieved: " + value["parameter"])
        logging.info("Response recieved: " + value["parameter"])
   



    
