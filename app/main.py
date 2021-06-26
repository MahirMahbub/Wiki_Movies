from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.create_data import CreateData
from app.cruds.data_loader import DataLoaderCrud
from app.custom_classes.rating_extractor import RatingExtractor
from app.routes import movies
from db.database import SessionLocal

app = FastAPI()

# API Doc
app = FastAPI(
    title="Wiki-Movie",
    description="Wikipedia Persing Tools",
    version="1.0.0",
)


# Error
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    # print(f"OMG! An HTTP error!: {repr(exc)}")
    # Add error logger here loguru
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# fastapi_users = FastAPIUsers(
#     user_db,
#     [jwt_authentication],
#     User,
#     UserCreate,
#     UserUpdate,
#     UserDB,
# )

app = FastAPI()

# API routes
app.include_router(
    movies.router,
    tags=["Movies"]
)

db = SessionLocal()



@app.on_event("startup")
async def startup_event():
    is_to_load = DataLoaderCrud(session=db).get(activity_name="Movie Data Loading")
    if is_to_load is not None:
        if is_to_load.status==True:
            try:
                CreateData.get_instance().get_chain_of_responsibility()
                DataLoaderCrud(session=db).update_status(activity_name="Movie Data Loading", status=False)
                db.commit()
            except Exception as e:
                print(e)
    is_to_load_rating = DataLoaderCrud(session=db).get(activity_name="Movie Rating Loading")
    if is_to_load_rating is not None:
        if is_to_load_rating.status==True:
            try:
                RatingExtractor(session=db).execute()
            except Exception as e:
                print(e)

# if __name__ == '__main__':
#     uvicorn.run(app='app:app', reload=True, port="7003", host="0.0.0.0")
