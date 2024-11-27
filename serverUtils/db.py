from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Depends, HTTPException

# method for starting the MongoDB connection
async def startup_db_client(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(
        "mongodb+srv://roshanbiswanathpatra:wHgiypCLk1Eyi3aw@devcluster.gmovc.mongodb.net/?retryWrites=true&w=majority&appName=devCluster")
    app.mongodb = app.mongodb_client.get_database("devDatabase")
    try:
        await app.mongodb_client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("Unable to connect to MongoDB")
        print(e)

# method to close the database connection
async def shutdown_db_client(app: FastAPI):
    app.mongodb_client.close()

# method to get the database connection
def getDatabase(app: FastAPI):
    return app.mongodb

# method to get the business from API key
async def getBusinessFromAPIKey(api_key: str, app: FastAPI):
    business_collection = getDatabase(app).get_collection("business")
    business = await business_collection.find_one({"businessAPIKey": api_key})
    print(business)
    # if business is None:
    #     raise HTTPException(status_code=404, detail="Business not found")
    return business

# # Register startup and shutdown events
# app.add_event_handler("startup", startup_db_client)
# app.add_event_handler("shutdown", shutdown_db_client)