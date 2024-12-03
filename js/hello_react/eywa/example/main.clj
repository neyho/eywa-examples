(ns example.main
  (:require 
    neyho.eywa.transit
    neyho.eywa
    neyho.eywa.lacinia
    neyho.eywa.server
    neyho.eywa.server.jetty
    neyho.eywa.data
    neyho.eywa.db.postgres
    neyho.eywa.avatars.postgres
    neyho.eywa.authorization
    neyho.eywa.iam
    neyho.eywa.dataset
    neyho.eywa.dataset.default-model
    neyho.eywa.dataset.postgres
    neyho.eywa.dataset.postgres.query
    [neyho.eywa.server.interceptors.authentication :refer [init-default-encryption]])
  (:gen-class :main true))


(defn -main
  []
  (neyho.eywa.transit/init)
  (init-default-encryption)
  (neyho.eywa.db.postgres/init)
  (neyho.eywa.dataset/init)
  (neyho.eywa.avatars.postgres/init)
  (neyho.eywa.iam/init)
  (neyho.eywa.server/start
    {:context-configurator neyho.eywa.server.jetty/context-configuration}))
