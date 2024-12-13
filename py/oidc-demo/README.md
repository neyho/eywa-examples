# EYWA IAM + Flask

For starters you will need running instance of EYWA that you can connect to. If you don't have running instance
instructions for creating one can be found at [EYWA Core](https://github.com/neyho/eywa-core)


#### Prerequisites
Clone eywa-examples repo... Run:
```
cd py/oidc-demo
python -m venv .venv
source .venv/bin/activate
# Windows .venv/bin/Activate.ps1
pip install -r requirements.txt
```
This will install required dependencies like [eywa-client](https://pypi.org/project/eywa-client/).

#### Connect to running EYWA instance
In _py/oidc-demo_ folder create eywa.json file
```
Linux:     touch eywa.json
Windows:   New-Item -Path .\eywa.json -ItemType File
```
Running ```eywa connect``` will start Device Code Flow authorization, and
 will require from you to authenticate on EYWA IAM module. When authenticated,
you can interact with EYWA through scripts.

```
eywa connect https://some.running.instance
or
eywa connect http://localhost:8080
```

#### Import OIDC Test Client
```
eywa run -c "python init.py"
```
eywa run -c marks command that eywa client will run. By running this command, eywa client will use
previously authorized user credentials to connect to eywa and run import.js script. import.js script
will read from file _resources/app_react_example.json_ and send that with graphql mutation to EYWA server.

In plain it will import test OAuth Client


#### Run server
```
python app.py
```
Start development environment and navigate to http://127.0.0.1:5000
