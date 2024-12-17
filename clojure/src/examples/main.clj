(ns examples.main
  (:require
   [neyho.eywa]
   [clojure.java.io :as io]
   [neyho.eywa.core :as core]
   [neyho.eywa.dataset.sql.compose :as compose]
   [neyho.eywa.lacinia :as lacinia]
   [examples.movies :as movies]))

(defonce counter (atom nil))

(defn get-counter
  [_ _ _]
  @counter)

(defn extend-counter
  [_ _ v]
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

(defn counter-subscription
  [_ _ upstream]
  (let [id (str (java.util.UUID/randomUUID))]
    (add-watch
     counter id
     (fn [_ _ _ new-value]
       (upstream new-value)))
    (fn []
      (remove-watch counter id))))

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

(defn best-actors
  [_ data _]
  (compose/execute! (compose/prepare ::best-actors data)))

(defmethod compose/prepare [::best-movies neyho.eywa.Postgres]
  [_ {:keys [limit]}]
  [(compose/ml
    (format "select movie._eid, movie.title , avg(ratings.value) rating, count (ratings.value) ratings from %s as movie" (compose/table movie))
    (compose/relation-join
     {:entity movie
      :label :movie_ratings
      :from-alias "movie"
      :to-alias "ratings"})
    "group by movie._eid"
    (format "order by rating desc limit %s" limit))])

(defn best-movies
  [_ data _]
  (compose/execute! (compose/prepare ::best-movies data)))

(defn -main
  [& _]
  (core/start)
  (lacinia/add-shard ::example (slurp (io/resource "example.graphql"))))

(comment
  ;; Initialize

  (movies/all)

  ;; To clean DB of movie models use my.eywaonline.com UI
  ;; and delete Movies dataset

  ;;
  (swap! counter (fnil inc 0))
  (println
   (compose/relation-join
    {:entity movie-actor
     :label :movies
     :to-alias "movies"}))
  (def data nil)
  (println
   (compose/prepare ::best-actors nil)))
