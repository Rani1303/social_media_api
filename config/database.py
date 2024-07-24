from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb+srv://root:root@cluster0.hztpjzw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(uri)
db = client.social_media_api
collection = db.social_media_api