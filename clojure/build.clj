(ns build
  (:require
   [clojure.string :as str]
   [clojure.pprint :refer [pprint]]
   [clojure.java.io :as io]
   [clojure.tools.build.api :as b]
   [clojure.java.shell :refer [sh]]))

(def lib 'neyho/eywa-example)
(def class-dir "target/classes")
(def basis
  (b/create-basis
   {:project "deps.edn"}))

(def version "0.1.0")

(def uber-file (format "target/eywa.%s.jar" version))

(defn clean []
  (b/delete {:path "target"}))

; (def exclude-uber-basis-pattern #"src.*$")

; (def uber-basis
;   (update basis :libs
;           (fn [libs]
;             (reduce-kv
;              (fn [libs lib context]
;                (if (contains? context :local/root)
;                  (update-in libs [lib :paths]
;                             (fn [paths]
;                               (vec
;                                (remove
;                                 (fn [path]
;                                   (re-find exclude-uber-basis-pattern path))
;                                 paths))))
;                  libs))
;              libs
;              libs))))

(defn compile
  [& _]
  (b/write-pom {:class-dir class-dir
                :lib lib
                :version version
                :basis basis
                :src-dirs ["src/clj" "src/prod"]})
  (println "Compiling backend")
  (b/compile-clj
   {:basis basis
    :src-dirs ["src" "resources"]
    :ns-compile ['examples.main
                 'clojure.core.async
                 'clojure.core.async.impl.protocols]
    :class-dir class-dir})
  (b/copy-dir
   {:src-dirs ["resources"]
    :target-dir class-dir}))

(defn uber [& _]
  (println "Creating uberjar file")
  (b/copy-file
   {:src "resources/logback.xml"
    :target (str class-dir "/logback.xml")})
  (b/uber
   {:class-dir class-dir
    :uber-file uber-file
    :main 'examples.main
    :manifest {"Application-Name" "EYWA"}
     ;; Exclude source code
    :basis basis}))

(defn all [& _]
  (clean)
  (compile)
  (uber))
