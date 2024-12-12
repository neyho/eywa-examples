import eywa from 'eywa-client'
import { promises as fs } from 'fs'


const gql = (strings) => strings[0]


let read_client = async () => {
  try {
    const data = await fs.readFile('resources/app_react_example.json', 'utf8');
    return JSON.parse(data)
  } catch (err) {
    return null;
  }
}


const syncClient = gql`
mutation ($client:OAuthClientInput) {
  syncOAuthClient(oauth_client:$client) {
    euuid
    name
  }
}
`

let import_client = async (data) => {
  try {
    console.log(syncClient)
    let result = await eywa.graphql(syncClient, { client: data })
    console.log('Successfully imported client!')
    return result
  }
  catch (err) {
    console.log(err)
  }
}


let delete_client = async (data) => {
  try {
    console.log("EUUID: " + data.euuid)
    const query = `
      mutation {
        deleteOAuthClient(euuid:\"${data.euuid}\")
      }
    `
    console.log(query)
    let result = await eywa.graphql(query)
    return result
  } catch (err) {
    console.log(err)
    return false
  }
}


(async () => {
  let command = process.argv.slice(2)[0]
  eywa.open_pipe()
  let client = await read_client()
  if (command == "reset") {
    await delete_client(client)
  } else {
    await import_client(client)
  }
  process.exit()
})();
