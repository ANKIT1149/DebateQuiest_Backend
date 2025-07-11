import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "generated"))
)

from prisma import Prisma


async def test():
    prisma = Prisma()
    try:
        await prisma.connect()
        print("Prisma connected successfully!")
        await prisma.disconnect()
    except Exception as e:
        print(f"Error: {e}")


import asyncio

asyncio.run(test())
