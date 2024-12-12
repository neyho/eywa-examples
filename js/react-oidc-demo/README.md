# EYWA IAM + React

For starters you will need running instance of EYWA that you can connect to. If you don't have running instance
instructions for creating one can be found at [EYWA Core](https://github.com/neyho/eywa-core)


#### Prerequisites
Clone eywa-examples repo... Run:
```
cd js/react-oidc-demo
npm install
```
This will install required dependencies like [eywa-client](https://www.npmjs.com/package/eywa-client).

#### Connect to running EYWA instance
In _js/react-oidc-demo_ folder run
```
eywa core gen-config -j
```
This will generate _eywa.json_
```
eywa connect https://some.running.instance
or
eywa connect http://localhost:8080
```
Running ```eywa connect``` will start Device Code Flow authorization, and will require from you to authorize
on EYWA IAM module. When authorized, you can interact with EYWA through scripts.


#### Import React Example Client
```
eywa run -c "node init.js"
```
eywa run -c marks command that eywa client will run. By running this command, eywa client will use
previously authorized user credentials to connect to eywa and run import.js script. import.js script
will read from file _resources/app_react_example.json_ and send that with graphql mutation to EYWA server.

In plain it will import example OAuth Client


#### Run server
```
npm run dev
```
Start development environment and navigate to http://localhost:5173

Congratulations, you have declared OAuth Client in EYWA IAM module. Happy coding...
