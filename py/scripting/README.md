# EYWA Core + Python

For starters you will need running instance of EYWA that you can connect to. If you don't have running instance
instructions for creating one can be found at [EYWA Core](https://github.com/neyho/eywa-core)


#### Prerequisites
Clone eywa-examples repo... Run:
```
cd py/scripting
python -m venv .venv
source .venv/bin/activate
# Windows .venv/bin/Activate.ps1
pip install -r requirements.txt

```
This will install required dependencies like [eywa-client](https://pypi.org/project/eywa-client/).


#### Connect to running EYWA instance
In _py/react-oidc-demo_ folder create eywa.json file
```
Linux:     touch eywa.json
Windows:   New-Item -Path .\eywa.json -ItemType File
```
Running ```eywa connect``` will start Device Code Flow authentication, and
 will require from you to authenticate on EYWA IAM module. When authenticated,
you can interact with EYWA through scripts.

```
eywa connect https://some.running.instance
```
or
```
eywa connect http://localhost:8080
```


#### Movies
```movies.js``` script is small showcase that highlights how to deploy dataset, populate
deployed dataset with fake data for entities and releations by running following commands:

```
eywa run -c "python movies.py deploy"
eywa run -c "python movies.py import"
eywa run -c "python movies.py show_movies"
eywa run -c "python movies.py show_actors"
eywa run -c "python movies.py delete"
eywa run -c "python movies.py error"
```


You can monitor how above commands affect your DB. Also, please do feel free and check out
how easy it is to query EYWA by using https://my.eywaonline.com/data/graphql.

