
# CS50 -  Stock Exchange
<p align="center">
  <img width="200" height="200" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCx166ijuW_yTBd_sdrpwibXRzyVgyPVMvNA&usqp=CAU">
</p>
  <h2> Table of Contents </h1>

+ [Setup](#setup)
    + [Step 1](#Step1)
    + [Step 2](#Step2)
+ [Running The Application](#app)  
+ [Features](#features)

<a name="setup"/>
  <h2> Setup </h2>

<a name="step1"/>
  <h4> Step 1 </h4>

First, you need to install 'requirements.txt' via pip.

`pip install -r requirements.txt`

<a name="step2"/>
<h4> Step 2 </h4>
Last step is that you have to initialize the Flask App.

###### On CMD

`set FLASK_APP=application.py`

###### On Powershell

`$env:FLASK_APP="application.py"`

###### On Bash

`export FLASK_APP=application.py`

---
<a name="app"/>
  <h2> Running The Application </h2>

After installing requirements and initializing app, you are ready to go!

In root directory, run:

`flask run`

This command will start the local server. Which you can connect via 

http://127.0.0.1:5000/

or 

[Localhost](http://127.0.0.1:5000/)

<a name="features"/>
  <h2> Features </h2>

- Search shares to see the current value 
- Buy shares
- Sell shares
- View transaction history
