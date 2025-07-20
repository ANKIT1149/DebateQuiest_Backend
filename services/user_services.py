from prisma import Prisma

async def create_user_table():
    try:
        prisma = Prisma()
        await prisma.connect()

        print("Creating user table if it does not exist...")
        return True
    except Exception as error:
        print(f"Error creating user table: {error}")
        return False
