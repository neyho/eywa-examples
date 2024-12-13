# EYWA IAM + Babashka

For starters you will need running instance of EYWA that you can connect to. If you don't have running instance
instructions for creating one can be found at [EYWA Core](https://github.com/neyho/eywa-core)


#### Prerequisites
Clone eywa-examples repo... Run:
```
cd bb/
clj -X:deps prep
```
This will install required dependencies.

#### Connect to running EYWA instance
In _js/react-oidc-demo_ folder create eywa.json file
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

#### Development
```
eywa run -c "bb nrepl-server"
```
eywa run -c marks command that eywa client will run. By running this command, eywa client will use
previously authorized user credentials to connect to EYWA server and run command wrapped in new process.

This will work fine for above situation, where nrepl-server is started, but it won't work for classic
command line repl. Like starting ```clj``` won't work.


#### Movies Playground
Namespace _example.movies_ presents playground for deploying Movies_Example dataset as well
as functions for importing movies data. Model itself holds few entities like: Movies, Actors,
Genres, Movie Users and Movie Ratings. Data is fake, so no correlation to real life movies and
actors.

Anyway this is good enough to showcase dataset deploy consequences. When model is deployed
DB tables are created and GraphQL exposed for reading and writing.

Also functions for deploying and inserting data can be called directly from cli:
```
eywa run -c "bb -m example.movies deploy"
eywa run -c "bb -m example.movies import"
eywa run -c "bb -m example.movies show"
eywa run -c "bb -m example.movies delete"
```


Do try and hack current setup... Happy Hacking!
