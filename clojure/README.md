# Extending EYWA Core with Clojure

EYWA Core offers Data Modeling through UI and deploying modeled datasets
to DB with out of the box interface exposed throught generic GraphQL methods.

What to do when that is not enough? What if frontend requires backend state
value(i.e. atom, ref)? Can I extend GraphQL schema and how can i do it?


This example project is all about that. It will guide you through extending
queries and mutations, as well as extending deployed entity fields with custom
fields and defining resolvers for those fields through graphql schema.

Subscription? What about that? Sure, it is explained here in this project,
as well as how to build uberjar. This project highlights EYWA Core features
 and dynamic nature by covering most common use cases (it will be extendend
in the future to cover less common situations).


#### Install [Clojure](https://clojure.org/guides/install_clojure)
Java is required! Suggesting Java17


#### Environment
Setup environment variables required by EYWA. If you are in luck and
are working on OSx or Linux or WSL than checkout [direnv](https://direnv.net/)

Otherwise:
```
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=eywa_dev
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password


export POSTGRES_ADMIN_USER=postgres
export POSTGRES_ADMIN_PASSWORD=password
export POSTGRES_ADMIN_DB=postgres
```

Adjust values to target PostgreSQL server.


### tools.deps.alpha
Recommended way to explore this repo is by using repl or nrepl, but
it is possible to run segments from command line directly. If using
(n)repl, please focus on _examples.main_ namespace. Follow comments...


Otherwise:
```
clj -m examples.main "setup" # only once to setup EYWA Core
clj -m examples.main "init"
clj -m examples.main
# clj -m examples.main "teardown" # this will drop POSTGRES_DB from Postgres server
```


Build: 
```
clj -T:build all
```

Run jar:
```
java -jar target/example.jar "setup"
java -jar target/example.jar "init"
java -jar target/example.jar
java -jar target/example.jar "teardown"
```


### Leiningen
PRs welcome!
