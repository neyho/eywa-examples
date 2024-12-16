# EYWA Core + NodeJS

For starters you will need running instance of EYWA that you can connect to. If you don't have running instance
instructions for creating one can be found at [EYWA Core](https://github.com/neyho/eywa-core)


#### Prerequisites
Clone eywa-examples repo... Run:
```
cd js/scripting
npm install
```
This will install required dependencies.


#### Connect to running EYWA instance
In _js/react-oidc-demo_ folder create eywa.json file
```
Linux:     touch eywa.json
Windows:   New-Item -Path .\eywa.json -ItemType File
```
Running ```eywa connect``` will start Device Code Flow authentication, and
 will require from you to authenticate on EYWA IAM module. When authenticated,
you can interact with EYWA through scripts.

```
eywa connect https://some.running.instance
or
eywa connect http://localhost:8080
```


#### Movies
```movies.js``` script is small showcase that highlights how to deploy dataset, populate
deployed dataset with fake data for entities and releations by running following commands:

```
eywa run -c "node movies.js deploy"
eywa run -c "node movies.js import"
eywa run -c "node movies.js test"
eywa run -c "node movies.js error"
eywa run -c "node movies.js delete"
```


You can monitor how above commands affect your DB. Also, please do feel free and check out
how easy it is to query EYWA by using https://my.eywaonline.com/data/graphql.

