#REST Demo in Python

This is a simple Python client for *Documentum REST Services*.

##What the demo demonstrates?

It will do the following jobs for your reference.  

1. reset demo environment;  
2. create a temp cabinet for demo use;  
3. demo folder CRUD;  
4. demo sys object CRUD;  
5. demo content management;  
6. demo version management;  
7. demo DQL query;  
8. clear the temp cabinet

##Requirements
1. Python 2.7.x is installed.
2. Library [request](http://docs.python-requests.org/en/latest/) is installed.
3. *Documentum REST Services 7.2* is deployed.


##Instruction
The instruction is for Windows. For other operating system, only steps 1-4 are different. Try your luck.

1. Download and install [Python 2.7.x](https://www.python.org/downloads/)
2. Add `python` to the environment variable PATH. Open a new console and run the command.

        setx PATH "%PATH%;C:\Python27"

3. Add *pip* to the environment variable PATH. Open a console and run the command. 

        setx PATH "%PATH%;C:\Python27\Scripts"

4. To verify the environment variable PATH is modified successfully, Open a new console and the command as below to check if the path is appended.

        echo %PATH%       

5. Run command to install library [requests](http://docs.python-requests.org/en/latest/)

        pip install requests

6. Extract the demo package and change directory to the folder.

        cd python-demo
            
7. Edit rest.properties according to the environment.

8. Run the command to execute the demo.

        python RestDemo.py
        
9. During the execution, the program will prompt the file path to create new rendition. Input *enter* to skip this step. [^1]

[^1]: If a wrong path is input, the step will be skipped.  
