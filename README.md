# Introduction

This repo contains examples and use cases how to interact with EYWA and
how to extend EYWA. Clients for connecting to EYWA backend are available
in number of languages. More about [EYWA](https://github.com/neyho/eywa-core)

Examples cover how to use EYWA Identity Access Management to authenticate
users through frontend applications, as well as how to authenticate user
from CLI and than use EYWA Data module to insert and query data.


## [Extend with Clojure](clojure/README.md)
EYWA is written in Clojure. To extend EYWA backend with new features and GraphQL
mutations,queries and subscriptions check out _clojure_ folder. In addition it
highlights how to build and package modified code in uberjar.


## Movies
Movies_Example  data model with fake movie data is available in _datasets/_
folder. _datasets/movies_ contain "dump" of Movies_Example data model that
is used in examples for every language in this repo.

Idea is to show how to deploy Movies_Example datamodel, insert data by reading JSON
files in _dataset/movies_ folder by using GraphQL mutations for each language.

* [JS](js/scripting/README.md)
* [PY](py/scripting/README.md)
* [BB](bb/README.md)


### OIDC JS



### OIDC PY
Python oidc-demo example demonstrates how to use [Authlib](https://authlib.org/) to
authenticate user with EYWA IAM module.

