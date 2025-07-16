import eywa
import asyncio
import json
import numpy as np
import sys
import pprint


async def search_users():
    return await eywa.graphql("""{
    searchUser (_limit:2000) {
      euuid
      name
      type
    }
    }""")


async def main():
    eywa.open_pipe()
    users = await search_users()
    print("Users\n" + str(users))
    eywa.exit()


asyncio.run(main())
