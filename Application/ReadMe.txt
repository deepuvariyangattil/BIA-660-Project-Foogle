#----------------------------------------README-------------------------------------------#

How to get started.

1. Download and install MongoDB from https://www.mongodb.com/download-center/community
2. Copy MASTERRECIPELIST.csv file into bin folder of MongoDB
3. Open CMD where you have installed and run following command
                mongoimport -d biafinal -c democoll --type csv --file MASTERRECIPELIST.csv --headerline
4. Above command will import CSV data into MongoDB
5. Download and Install NODE.JS if you dont have already from https://nodejs.org/en/download/
6. From the directory where you have coppied content of application run following command "npm start" in CMD.
7. Open your browser and enter url "http://localhost:3000"
8. Foogle is ready to be used.

#----------------------------------------EOF----------------------------------------------------#