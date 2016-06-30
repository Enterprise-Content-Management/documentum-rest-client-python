Documentum REST Python Client Samples
=========

[![Python: 2.7](https://img.shields.io/pypi/pyversions/Django.svg)](https://www.python.org/download/releases/2.7/) 
[![License: Apache 2](https://img.shields.io/hexpm/l/plug.svg)](http://www.apache.org/licenses/LICENSE-2.0)

This is a simple Python client for *Documentum REST Services*.

##What the demo demonstrates?

It will do the following jobs for your reference.  

```
0. Reset demo environment
1. REST all demos
2. REST sysObject CRUD
3. REST content management
4. REST version management
5. REST DQL
6. REST search with URL parameters 
7. REST formats 
8. REST network locations 
9. REST relation CRUD 
10. REST folder CRUD
11. REST type
```



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

7. Edit `rest.properties` or input the info during running the demo.

8. Run the command to execute the demo.

        python RestDemo.py

9. During the execution, the program will prompt the file path to create new rendition. Input *enter* to skip this step. [^1]

[^1]: If a wrong path is input, the step will be skipped.  
