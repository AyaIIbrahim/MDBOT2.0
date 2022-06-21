
## MDBOT
<img src="https://user-images.githubusercontent.com/60445096/173965333-60d9b9bd-228b-4ce6-8a20-1382bb4143e4.jpg" width="30%"></img> 



 # For Windows 
## All the commands are written in Command Prompt (Admin)
To open Command Prompt with administrative privileges, right-click the result and then click “Run as Administrator.”
<img src="https://user-images.githubusercontent.com/60445096/173980989-fcf2d409-7e9e-46a0-b176-33ab42a8bff2.png" width="45%"></img> 
______________
Recommended Steps for successful running 

1. Install/upgrade to Python 3.9.2
   -  Run the Python Installer
   [Python 3.9.2](https://www.python.org/downloads/release/python-392/)
    
      Check python version
       ```
      $ python -V
       ```
2. install PIP
    download the get-pip.py file.
    [click](https://bootstrap.pypa.io/get-pip.py)
   
   command to download the get-pip.py file
   
       
       $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
             
   
   - install PIP
    
       ```
       $ python get-pip.py
       ``` 
   - Verfiy the Installation
       ```
       $ pip help
       ```
   -  Add Pip to Windows Environment Variables
   <img src="https://user-images.githubusercontent.com/60445096/173977880-de1dc9c2-2ce3-4b3b-b13f-ac919eefa47c.png" width="90%"></img> 
   <img src="https://user-images.githubusercontent.com/60445096/173977938-829c28d6-e6f4-4dc8-a7cd-8d6518f6141d.png" width="90%"></img> 
   <img src="https://user-images.githubusercontent.com/60445096/173977991-243bebde-8f9c-4363-916c-1f5862b3954a.png" width="90%"></img> 
 

3. install Git -if first time-
    [git](https://git-scm.com/download/win)
    
4. git clone
    ```
    $ git clone https://github.com/eris-ez/MDBOT1.0.git
    ```
5. Navigate to the project folder and install the the requirements for the project to run
  ```
  $ pip install -r requirements.txt
   ```   
   if it didn't work, try
   ```   
  $ pip3 install -r requirements.txt
   ```   
__________________________________________

## if all the above commands are running and giving no error,  your environment is ready to run the app now.

1.    Use any Python IDE (PyCharm, Spyder, Visual Studio Code) to open the project


2.    run train.py    
      if you don't have a Python IDE installed, open cmd and run 
      ```   
      $ python3 train.py  
      ```  

3.    run index.py  

     
4.    Mostly, it will be running on server  http://127.0.0.1:5000/

      The frontend connects to the backend using a local IP address. The default is set to 127.0.0.1:5000


5.    type  http://127.0.0.1:5000/ in the browser and everthing should be working fine
