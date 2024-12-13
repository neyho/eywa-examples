# EYWA IAM + NodeJS

For starters you will need running instance of EYWA that you can connect to. If you don't have running instance
instructions for creating one can be found at [EYWA Core](https://github.com/neyho/eywa-core)


#### Prerequisites
Clone eywa-examples repo... Run:
```
cd js/nodejs-oidc-demo
npm install
```
This will install required dependencies like [eywa-client](https://www.npmjs.com/package/eywa-client).

#### Connect to running EYWA instance
In _js/nodejs-oidc-demo_ folder create eywa.json file
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

#### Import React Example Client
```
eywa run -c "node import.mjs"
```
eywa run -c marks command that eywa client will run. By running this command, eywa client will use
previously authorized user credentials to connect to eywa and run import.js script. import.js script
will read from file _resources/app_react_example.json_ and send that with graphql mutation to EYWA server.

In plain it will import example OAuth Client


#### Run server
```
node app.js
```
Start development environment and navigate to http://localhost:5173

Congratulations, you have declared OAuth Client in EYWA IAM module. Happy coding...
