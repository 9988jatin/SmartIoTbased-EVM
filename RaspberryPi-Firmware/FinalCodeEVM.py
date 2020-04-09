'#!usr/bin/env python' //Making code executable 
import serial //importing serial library for UART communication
import time //This library is for sleep and delay
from twilio.rest import Client //importing twilio library 

//initialzing functions for storing voting data
countRWE = 0 // Variable to store RWE count 
countTNR = 0 // Variable to store TNR count 
votesTNR = 0 //function to store final votes of TNR party
votesRWE = 0 //function to store final votes of RWE party


account_sid = 'AC34be9483362ab6f056b4d9ff01c25976' //Twilio account SSID 
auth_token = '755c012e59af99fb7403bc9dcc7c9c74' //Authentication token

client = Client(account_sid, auth_token) //Passing SSID data and authentication token to client function of Twilio

ser = serial.Serial("/dev/ttyS0",baudrate=9600) //Initializing serial port of raspberry to read data from STM32 with baud rate of 9600

while True: //Start of code

    

    print ("Please place your finger on the scanner") //Printing data for reading fingerprint sensor data from STM32

    data = ser.readline().strip('\r\n').strip() //Read STM data and strip /r/n from data and store in variable data

    value = int(data) //converting byte data to int

   # print(value) //uncomment this to print uart data on serial port

    if value == 1: //if Read data from STM is 1 that means correct finger // 2 means invalid finger // 3 means communication error

        print("Valid finger. Please enter details to vote") //If valid finger read the user details

        userFirstName = raw_input('Enter your first name: ') //Reading first name and storing in userFirstName 
        userLastName = raw_input('Enter your last name: ') //Reading last name and storing in userLastName 
        userFatherName = raw_input('Enter your father name: ') //Reading Father name and storing in userFatherName 
        userNumber = input('Enter your phone number: ') //Reading phone number

        userParty = input('Press 1 to vote for RWE party, Press 2 to vote for TNR party:\n') //Reading which party user voted


        //Twilio message body 
        message = client.messages \
                 .create(
                         body="Dear " + userFirstName + "," + " Your vote casted successfully. Thank you!",
                        from_='+19415848699',
                         to= userNumber

                ) //If details are ok send confirmation message
        print ("Message sent successfully to user: ",userFirstName) //Print if successful

    

        if userParty == 1: //if user pressed 1 add it to RWE party

            countRWE +=1 //Adding vote to RWE party by increasing count by 1

            print ("Vote casted to party RWE: ", countRWE) //print count of RWE

            print ("Vote casted to party TNR: ", countTNR) //print count of TNR

            votesRWE = countRWE //Store the new value to votesRWE if in this loop



        elif userParty == 2: //if user pressed 2 add it to TNR party

            countTNR +=1 //Adding vote to TNR party by increasing count by 1

            print ("Vote casted to party TNR: ", countTNR) //print count of TNR

            print ("Vote casted to party RWE: ", countRWE) //print count of RWE

            votesTNR = countTNR //Store the new value to votesTNR if in this loop



        else:

            print ("Invalid user Input") // if other than 1 and 2 user presses other number

            totalVotes = votesRWE + votesTNR //variable to store total votes //Sum of votes of RWE + TNR party



        print("\033c") //clear the screen and read data of new user

        print ("Total no of votes casted: ", totalVotes) //Keep printing total no of votes on screen



        time.sleep(5) //Delay of 5 secs after each vote



    elif value == 2: //if STM data is 2

        print("Invalid finger")



    else:        //Communication error between Raspberry and STM

        print("Try again")



exit()        //End 



