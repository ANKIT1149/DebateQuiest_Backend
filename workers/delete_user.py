from prisma import Prisma

async def delete_user():
    try:
        prisma = Prisma()
        await prisma.connect()

        print("Prisma connected Successfully")

        # Delete all users
        deleted_users = await prisma.user.delete_many()

        if not deleted_users:
            return {"message": "No users found to delete", "status": 404}

        return {
            "message": "All users deleted successfully",
            "status": 200,
            "data": deleted_users
        }
    except Exception as error:
        print(f"Error deleting users: {error}")
        return {"message": f"Failed to delete users: {error}", "status": 500}
    finally:      
        await prisma.disconnect()
        print("Prisma disconnected Successfully")

if __name__ == "__main__":
    import asyncio
    asyncio.run(delete_user())