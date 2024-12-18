(ns examples.main
  (:require
   [neyho.eywa]
   [clojure.java.io :as io]
   [clojure.tools.logging :as log]
   [clojure.core.async]
   [neyho.eywa.core :as core]
   [neyho.eywa.server]
   [neyho.eywa.dataset.sql.compose :as compose]
   [neyho.eywa.lacinia :as lacinia]
   [examples.movies :as movies])
  (:gen-class :main true))

;; Defined example state to showcase how
;; application state can be combined with
;; DB state
;; For GraphQL details checkout resources/examples.graphql
(defonce counter (atom nil))

(defn get-counter
  [_ _ _]
  @counter)

;; This function is used to extend GraphQL
;; schema for User entity to include counter
;; state
(defn extend-counter
  [_ _ _]
  @counter)

(defn inc-counter
  [_ _ _]
  (swap! counter inc))

(defn dec-counter
  [_ _ _]
  (swap! counter dec))

(defn reset-counter
  [_ _ _]
  (reset! counter 0))

;; Counter subscription... Use my.eywaonline.com/data/graphql
;; UI to test counterListener
;; subscription {
;;   counterListener
;; }
(defn counter-subscription
  [_ _ upstream]
  (let [id (str (java.util.UUID/randomUUID))]
    (upstream @counter)
    (add-watch
     counter id
     (fn [_ _ _ new-value]
       (upstream new-value)))
    (fn []
      (remove-watch counter id))))

(comment
  ;; To see how counter subscription will handle subscription
  ;; messages use section bellow when subscribed and
  ;; notifications should be visible in UI
  (swap! counter (fnil inc 0)))

;; Declaration of entity uuids... Tip: It is possible to copy
;; UUID from my.eywaonline.com/data/modeling UI, by selecting
;; Entity and clicking on barcode in opened drawer. In general
;; wherever ther is barcode, you can copy EUUID
(def movie-actor #uuid "f274cee0-681f-48d5-a67d-b0232f456f86")
(def movie #uuid "607556f6-8eaa-4089-a438-70aa91cd96e0")
(def user-rating #uuid "43056d28-e652-49a9-9276-70abb7019785")

(defmethod compose/prepare [::best-actors neyho.eywa.Postgres]
  [_ {:keys [user limit]
      :or {limit 1000}}]
  [(compose/ml
    (format "select actor._eid, actor.name, actor.euuid, avg(ratings.value) rating from %s as actor" (compose/table movie-actor))
    (compose/relation-join
     {:entity movie-actor
      :from-alias "actor"
      :label :movies})
    (compose/relation-join
     {:entity movie
      :label :movie_ratings
      :to-alias "ratings"})
    (when user
      (str "where actor._eid=%s" user))
    "group by actor._eid"
    (format "order by rating desc limit %s" limit))])

;; resolver for bestActors GraphQL query
(defn best-actors
  [_ data _]
  (compose/execute! (compose/prepare ::best-actors data)))

(defmethod compose/prepare [::best-movies neyho.eywa.Postgres]
  [_ {:keys [limit]}]
  [(compose/ml
    (format "select movie._eid, movie.euuid, movie.title , avg(ratings.value) rating, count (ratings.value) ratings from %s as movie" (compose/table movie))
    (compose/relation-join
     {:entity movie
      :label :movie_ratings
      :from-alias "movie"
      :to-alias "ratings"})
    "group by movie._eid"
    (format "order by rating desc limit %s" limit))])

;; resolver for bestMovies GraphQL query
(defn best-movies
  [_ data _]
  (compose/execute! (compose/prepare ::best-movies data)))

(comment
  ;; To test query preparation
  (def data nil))

(defn -main
  [& [command]]
  (log/info "Starting EXAMPLE EYWA service")
  (case command
    "setup" (do
              (core/initialize)
              (core/set-superuser
               {:username "admin"
                :password "admin"})
              (System/exit 0))
    "init" (do
             (core/warmup)
             (movies/all)
             (System/exit 0))
    "teardown" (do
                 (core/tear-down)
                 (System/exit 0))
    (do
      (core/start)
      (log/info "Adding 'example.graphql' shard")
      (lacinia/add-shard ::example (slurp (io/resource "example.graphql"))))))

(comment
  ;; Initialize

  (require '[examples.movies :as movies])
  (movies/all)

  ;; To clean DB of movie models use my.eywaonline.com UI
  ;; and delete Movies dataset

  (println
   (compose/relation-join
    {:entity movie-actor
     :label :movies
     :to-alias "movies"}))
  (println
   (compose/prepare ::best-actors nil)))
