
# CS50 -  Stock Exchange

![](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCx166ijuW_yTBd_sdrpwibXRzyVgyPVMvNA&usqp=CAU)


**Table of Contents**

[TOC]

#Setup

#### Step 1
First, you need to install 'requirements.txt' via pip.

`pip install -r requirements.txt`

#### Step 2
Last step is that you have to initialize the Flask App.

###### On CMD

`set FLASK_APP=application.py`

###### On Powershell

`$env:FLASK_APP = "application.py"`

###### On Bash

`export FLASK_APP=application.py`

---

#### Running the Application

After installing requirements and initializing app, you are ready to go!

In root directory, run:

`flask run`

This command will start the local server. Which you can connect via 

http://127.0.0.1:5000/

or 

[Localhost](http://127.0.0.1:5000/)


###Lists

#### Features

- Search shares to see the current value 
- Buy shares
- Sell shares
- View transaction history
