from fastapi import FastAPI
#vacations is the file so baicaly we import all the file
from routers import vacations


app = FastAPI()
#this is how to hook the router in to the main router

app.include_router(vacations.router)
