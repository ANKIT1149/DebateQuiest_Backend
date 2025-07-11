import logging
from prisma import Prisma
from models.RegisterModel import RegisterModel

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def register_userdata(user: RegisterModel):
    prisma = Prisma()
    try:
        logger.debug(f"Received user data: {user.model_dump()}")
        await prisma.connect()
        existing_user = await prisma.user.find_first(where={"email": user.email})
        if existing_user:
            return {"message": "User already exists", "status": 400}
        created_user = await prisma.user.create(
            data={
                "clerk_id": user.clerk_id,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "imageUrl": user.imageUrl,
            }
        )
        return {
            "message": "User created successfully",
            "status": 201,
            "data": created_user,
        }
    except Exception as error:
        print(f"Prisma error: {error}")
        return {"message": f"Failed to register user: {error}", "status": 400}
    except Exception as error:
        print(f"Unexpected error: {error}")
        return {"message": f"Unexpected error: {error}", "status": 500}
    finally:
        await prisma.disconnect()
