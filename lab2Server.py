import configparser
import logging
import socket
import time
import json

#reads the config file
config = configparser.ConfigParser()
config.read("3461-Project.conf")

#sets up the logging file
logging.basicConfig(filename="serverLogFile.log", 
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
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.info("Opened TCP socket")

# Open a socket and bind to the IP address and port
serverSocket.bind((serverHost, serverPort))

# servers listens for incoming connections
serverSocket.listen()

# accept new connection
conn, address = serverSocket.accept()  
print("Server starting on: " + serverHost)
logging.info("Server starting on: " + serverHost)

while True:
        
        #recieve the request
        data = conn.recv(1024).decode()
        if not data:
            logging.error("Server is not responding")
            continue

        #convert to python
        convert = json.loads(data)
        
        #if request is to quit
        if convert['request'] == "QUIT":
            null = {'response': 'Server shutting down ...', 'parameter': None}
            print("Server shutting down ...")
            logging.warning("Server is shutting down ...")
            convertBack = json.dumps(null)
            conn.send(convertBack.encode())
            break
        
        else:
            #converts python to json format in dict form
            response = {'response': convert['request'],
                        'parameter': f'{convert["parameter"]} ({int(time.time())})'
                        }
      
        #convert back to json and send to client
        convertBack= json.dumps(response)
        conn.send(convertBack.encode())  # send data to the client

        
    

    

