(ns example.movies
  (:require
   [eywa.client :as eywa]
   [cheshire.core :as json]
   [eywa.client.json :refer [<-json ->json]]
   [clojure.pprint :refer [pprint]]
   [clojure.core.async :as async]
   [toddler.graphql :as graphql]))

(defn deploy-movie-model
  []
  (let [model  (slurp "../datasets/Movies_Example_0_2.json")]
    (async/go
      (async/<!
       (eywa/graphql
        (graphql/mutations
         [{:mutation :importDataset
           :types {:dataset :Transit}
           :selection {:euuid nil}
           :variables {:dataset model}}])))
      (println "Movies dataset deployed"))))

(defn slurp-dataset [x] (slurp (str "../datasets/movies/" x ".json")))

(defn load-datasets
  []
  (async/go
    (println "Importing Movies, Actors, Genres, Users...")
    (time
     (let [mutations [{:mutation :syncMovieList
                       :selection {:euuid nil}
                       :types {:data :MovieInput}
                       :variables {:data (<-json (slurp-dataset "movies"))}}
                      {:mutation :syncMovieActorList
                       :alias "actors"
                       :selection {:euuid nil}
                       :types {:data :MovieActorInput}
                       :variables {:data (<-json (slurp-dataset "movie_actors"))}}
                      {:mutation :syncMovieGenreList
                       :selection {:euuid nil}
                       :alias "genres"
                       :types {:data :MovieGenreInput}
                       :variables {:data (<-json (slurp-dataset "movie_genres"))}}
                      {:mutation :syncMovieUserList
                       :selection {:euuid nil}
                       :types {:data :MovieUserInput}
                       :variables {:data (<-json (slurp-dataset "movie_users"))}}
                      {:mutation :syncMovieActorList
                       :alias "actors_mapping"
                       :selection {:euuid nil}
                       :types {:data :MovieActorInput}
                       :variables {:data (<-json (slurp-dataset "movie_actors_mapping"))}}
                      {:mutation :syncMovieGenreList
                       :alias "genres_mapping"
                       :selection {:euuid nil}
                       :types {:data :MovieGenreInput}
                       :variables {:data (<-json (slurp-dataset "movie_genres_mapping"))}}]]
       (eywa/graphql (graphql/mutations mutations))))
    (doseq [part (partition-all 10000 (<-json (slurp-dataset "user_ratings")))]
      (println "Importing ratings...")
      (time
       (async/<!
        (eywa/graphql
         (graphql/mutations
          [{:mutation :syncUserRatingList
            :types {:data :UserRatingInput}
            :variables {:data part}
            :selection {:euuid nil}}])))))
    (println "Data importing finished!")))

(defn delete-movies
  []
  (async/go
    (async/<!
     (eywa/graphql
      (graphql/mutations
       [{:mutation :deleteDataset
         :args {:euuid #uuid "6b48570e-e629-45f7-b118-b27239690a05"}}])))
    (println "Movies dataset removed!")))

(defn statistics-query
  ([] (statistics-query nil))
  ([{:keys [limit title]
     :or {limit 10}}]
   (graphql/queries
    [{:query :searchMovie
      :args (cond-> {:_limit limit}
              title (assoc :title {:_ilike (str \% title \%)}))
      :selection
      {:title nil
       :release_year nil
       :_count [{:selections
                 {:movie_ratings [{:alias :all}
                                  {:alias :super
                                   :args {:_where {:value {:_ge 8}}}}
                                  {:alias :bad
                                   :args {:_where {:value {:_le 4}}}}]}}]
       :_agg [{:selections
               {:movie_ratings
                [{:selections
                  {:_avg [{:selections {:value nil}}]}}
                 {:selections
                  {:_max [{:selections {:value nil}}]}}
                 {:selections
                  {:_min [{:selections {:value nil}}]}}]}}]
       :movie_ratings
       [{:args {:_join :LEFT :_order_by {:value :desc} :_limit 5}
         :selections {:value nil
                      :user [{:selections {:name nil}}]}}]}}])))

(defn -main
  [& args]
  (eywa/start)
  (case (first args)
    "deploy" (async/<!! (deploy-movie-model))
    "import" (async/<!! (load-datasets))
    "delete" (async/<!! (delete-movies))
    "show" (pprint
            (time
             (async/<!
              (eywa/graphql {:query (statistics-query {:title "enhanced"})}))))))

(comment
  (eywa/start)
  (println "HI")
  (println
   (async/<!
    (eywa/graphql
     {:query (graphql/queries
              [{:query :searchUser
                :selection {:euuid nil
                            :name nil}}])})))

  (deploy-movie-model)
  (load-datasets)

  (println (statistics-query {:title "enhanced"}))
  (async/go
    (pprint
     (time
      (async/<!
       (eywa/graphql {:query (statistics-query {:title "enhanced"})})))))

  (delete-movies))
