import eywa
import asyncio
import json


async def main():
    eywa.open_pipe()
    client = None
    with open("resources/client.json") as file:
        client = json.loads(file.read())

    print(client)
    await eywa.graphql("""
    mutation ($client:OAuthClientInput) {
      syncOAuthClient(oauth_client:$client) {
        euuid
        name
      }
    }
    """, {"client": client})
    eywa.exit()


asyncio.run(main())
