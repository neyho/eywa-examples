import eywa from 'eywa-client'
import { promises as fs } from 'fs'


let read_dataset = async (name) => {
  try {
    const data = await fs.readFile(`../../datasets/movies/${name}.json`, 'utf8');
    return JSON.parse(data)
  } catch (err) {
    return null;
  }
}


let read_model = async () => {
  return await fs.readFile(`../../datasets/Movies_Example_0_2.json`, 'utf8');
}


const deployDatasetMutation = `
mutation ($dataset: Transit) {
  importDataset(dataset:$dataset) {
    euuid
    name
    deployed
  }
}
`

const deploy_movies = async () => {
  await eywa.graphql(deployDatasetMutation, { dataset: await read_model() })
}


const drop_movies = async () => {
  await eywa.graphql(`
  mutation {
    deleteDataset(euuid: "6b48570e-e629-45f7-b118-b27239690a05")
  }
  `)
}


const import_movies = async () => {
  console.log("importing movies")
  const data = await read_dataset("movies")
  await eywa.graphql(`
  mutation($movies:[MovieInput]) {
        syncMovieList(movie:$movies) {
            euuid
            title
        }
    }
`, { movies: data })
}


const import_actors = async () => {
  console.log("importing actors")
  const data = await read_dataset("movie_actors")
  await eywa.graphql(`
mutation($actors:[MovieActorInput]) {
        syncMovieActorList(movie_actor:$actors) {
            euuid
        }
    }`, { actors: data })
}


const import_genres = async () => {
  console.log("importing genres")
  const data = await read_dataset("movie_genres")
  await eywa.graphql(`
mutation($genres:[MovieGenreInput]) {
        syncMovieGenreList(movie_genre:$genres) {
            euuid
        }
    }`, { genres: data })
}


const import_users = async () => {
  console.log("importing users")
  const data = await read_dataset("movie_users")
  await eywa.graphql(`
mutation($users:[MovieUserInput]) {
        syncMovieUserList(movie_user:$users) {
            euuid
        }
    }`, { users: data })
}


const link_movies = async () => {
  console.log("Linking movies")
  const genres = read_dataset("movie_genres_mapping")
  const actors = read_dataset("movie_actors_mapping")
  await eywa.graphql(`
mutation($genres:[MovieGenreInput] $actors:[MovieActorInput]) {
        syncMovieGenreList(movie_genre:$genres) {
            euuid
        }
        syncMovieActorList(movie_actor:$actors) {
            euuid
        }
    }`,
    {
      genres: await genres,
      actors: await actors
    })
}


const import_rating_part = async (part) => {
  console.log('importing rating part')
  await eywa.graphql(`
  mutation($ratings:[UserRatingInput]) {
          syncUserRatingList(user_rating:$ratings) {
              euuid
          }
      }
  `,
    { ratings: part })
  return null
}


function partitionAll(array, size) {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}


const import_ratings = async () => {
  const ratings = await read_dataset("user_ratings")
  const partitioned_ratings = partitionAll(ratings, 10000)
  for (const part of partitioned_ratings) {
    await import_rating_part(part); // Wait for each part to complete before starting the next
  }
}




(async () => {
  let command = process.argv.slice(2)[0]
  eywa.open_pipe()
  //console.log(await read_model())
  //let client = await read_client()
  try {
    switch (command) {
      case "delete":
        await drop_movies()
        break
      case "deploy":
        await deploy_movies()
        break
      case "import":
        await import_movies()
        await import_actors()
        await import_genres()
        await import_users()
        await link_movies()
        await import_ratings()
        break
      case "test":
        let response = await eywa.graphql(`
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
`)
        console.log('Received result:\n')
        console.log(JSON.stringify(response, null, 2))
        break
      case "error":
        try {
          await eywa.graphql(`
    {
        veryBadQuery(error:"Always")
    }
`)
        } catch (error) {
          console.error("Couldn't execute", error)
        }
        break
      default:
        console.log(
          `
Hi this is example script for importing Movies dataset
and importing Movies dataset data. To use this script
run one of:

eywa run -c "node movies.js deploy"
eywa run -c "node movies.js import"
eywa run -c "node movies.js test"
eywa run -c "node movies.js delete"
`)
    }
  } catch (error) {
    console.error("Couldn't execute command!", error)
  }
  process.exit()
})();
