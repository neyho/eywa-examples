import eywa
import asyncio
import json
import numpy as np
import sys




async def search_users():
    return await eywa.graphql("""{
    searchUser (_limit:2000) {
      euuid
      name
      type      
    }
    }""")


# async def insert_movies():


async def delete_movies_dataset():
    return await eywa.graphql("""
    mutation {
        deleteDataset(euuid:"6b48570e-e629-45f7-b118-b27239690a05")
    }
    """)


async def deploy_movies_dataset():
    dataset=None
    with open("../../datasets/Movies_Example_0_2.json") as file:
        dataset=file.read()
    return await eywa.graphql("""
    mutation ($dataset: Transit) {
        importDataset(dataset:$dataset) {
            euuid
            name
            deployed
        }
    }
    """, {"dataset": dataset})


def load_dataset(name):
    with open(f"../../datasets/movies/{name}.json") as file:
        return json.load(file)


async def import_movies():
    return await eywa.graphql("""
    mutation($movies:[MovieInput]) {
        syncMovieList(movie:$movies) {
            euuid
            title
        }
    }
    """,
    {"movies": load_dataset("movies")})


async def import_actors():
    return await eywa.graphql("""
    mutation($actors:[MovieActorInput]) {
        syncMovieActorList(movie_actor:$actors) {
            euuid
        }
    }
    """,
    {"actors": load_dataset("movie_actors")})


async def import_genres():
    return await eywa.graphql("""
    mutation($genres:[MovieGenreInput]) {
        syncMovieGenreList(movie_genre:$genres) {
            euuid
        }
    }
    """,
    {"genres": load_dataset("movie_genres")})


async def import_users():
    return await eywa.graphql("""
    mutation($users:[MovieUserInput]) {
        syncMovieUserList(movie_user:$users) {
            euuid
        }
    }
    """,
    {"users": load_dataset("movie_users")})


async def link_movies():
    return await eywa.graphql("""
    mutation($genres:[MovieGenreInput] $actors:[MovieActorInput]) {
        syncMovieGenreList(movie_genre:$genres) {
            euuid
        }
        syncMovieActorList(movie_actor:$actors) {
            euuid
        }
    }
    """,
    {"genres": load_dataset("movie_genres_mapping"),
     "actors": load_dataset("movie_actors_mapping")})



async def import_rating_part(part):
    print(f'Importing {len(part)} user ratings!')
    result = await eywa.graphql("""
    mutation($ratings:[UserRatingInput]) {
        syncUserRatingList(user_rating:$ratings) {
            euuid
        }
    }
    """, {"ratings": part.tolist()})
    print('Import finished')
    return result 



async def import_ratings():
    all_ratings = load_dataset("user_ratings")
    partitioned = np.array_split(all_ratings, 6)
    tasks = [import_rating_part(part) for part in partitioned]
    results = await asyncio.gather(*tasks)
    return True 



async def import_data():
    await import_movies()
    print('Imported Movies')
    await import_actors()
    print ('Imported Actors')
    await import_genres()
    print ('Imported Genres')
    await import_users()
    print ('Imported Movie users')
    await link_movies()
    print ('Linked movies to actors and genres')
    await import_ratings()
    print ('Imported User ratings')



async def search_movies():
    return await eywa.graphql("""
    {
      searchMovie(_limit: 10) {
        title
        _count {
          all: movie_ratings
          good: movie_ratings(_where: {value: {_ge: 8}})
          bad: movie_ratings(_where: {value: {_le: 4}})
        }
        _agg {
          movie_ratings {
            _avg {
              value
            }
          }
        }
        movie_ratings {
          value
          review
        }
        actors (_limit:10) {
          name
          birth_year
        }
      }
    } 
    """)


async def search_actors():
    return await eywa.graphql("""
   {
      searchMovieActor(_limit: 10) {
        name
        birth_year
        movies(_limit: 5) {
          title
          _agg {
            movie_ratings {
              _avg {
                value
              }
            }
          }
          _count {
            all_reviews: movie_ratings
            good_reviews: movie_ratings(_where: {value: {_ge: 7}})
            bad_reviews: movie_ratings(_where: {value: {_le: 4}})
          }
        }
      }
    } 
    """)


async def bad_query():
    return await eywa.graphql("""
    {
        veryBadQuery(error:"Always")
    }
    """)

    


async def main():
    eywa.open_pipe()
    action = sys.argv[1:][0]
    if action == "delete":
        await delete_movies_dataset()
        print("Movies dataset deleted!")
    elif action == "deploy":
        await deploy_movies_dataset()
        print("Movies dataset deployed!")
    elif action == "import":
        await import_data()
        print("Imported Movies data")
    elif action == "show_movies":
        print(await search_movies())
    elif action == "show_actors":
        print(await search_actors())
    else:
        print("Unknown command!")
    eywa.exit()


asyncio.run(main())
