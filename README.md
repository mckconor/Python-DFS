# Python-Distributed File System


## How to use
Navigate to folder in cmd/powershell. Open one instance for each of the following instructions

-python .\main.py

-python .\server.py

-python .\user.py

### main.py

This is the main controller of the directory service. It encompasses the directoryServ.py and authServ.py routes.

### server.py

Launch a new one of these to store files to. File names are stored in the files table in the database, with a reference to what server the file contents are stored on.

### user.py

This is the client interface for use with the system. The user is presented with the following commands to use: Download, Upload, Edit.

## How to use the system

1. Start python .\main.py

2. Start up a server, python .\server.py. You will be prompted to assigne it a unique name (eg: C, D, etc.)

3. Start up a user client, python .\user.py. 

4. Upload a file from the same directory. You will be prompted to choose the file name, followed by the server name to store the file to.

5. Download a file from a server. You will be prompted to enter the file name you wish to download, then the server name of where the file is stored (since the same file may reside on multiple servers.) You will then be prompted to save the file locally with a new name. The file is also cached at this point to the user.

6. Edit a file on the server. You will be prompted to enter the file name you wish to edit and the server name of where it is located. You will then be prompted to append whatever text you wish to the file contents, which are then returned and overwitten on the selected file server.

## Testing the features

1. Caching

-- Upload a file. Download the file again, it will now be cached. Download it once more, a message will print stating that the cached version is being accessed. Upload the same file from the start. Download again, the message will not appear.

2. Locking

-- Start 2 user clients. Upload a file. Edit the file with one client, but before confirming the text to append, try to download the same file on the same server with the second client. You will see the second client will have to wait and begins polling until the file becomes unlocked.

3. Authentication

-- Not as visible from the front end, the user's randomly generated username and set password are sent to be registered, then the user is authenticated where a server key is given to them. Done for simplicity and ease of testing. 
