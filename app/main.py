from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

from app.custom_classes.emails import invite_user_email
from app.routes import ocr_character_seperator
from db.database import database
from db.models import user_db, User, UserCreate, UserUpdate, UserDB, fastapi_users, jwt_authentication, SECRET

app = FastAPI()

# API Doc
app = FastAPI(
    title="OCR-Tools",
    description="This is a OCR data collection tool project",
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


def after_verification_request(user: UserDB, token: str, request: Request):

    response = invite_user_email(email="bsse0807@iit.du.ac.bd", token=token)
    print(request.items())
    if response:
        print(f"Verification requested for user {user.id}. Verification token: {token} generated in mail")
    else:
        print(f"Verification requested for user {user.id}. Verification token: {token} failed to send")






# fastapi_users = FastAPIUsers(
#     user_db,
#     [jwt_authentication],
#     User,
#     UserCreate,
#     UserUpdate,
#     UserDB,
# )

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(requires_verification=True),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_verify_router(SECRET, after_verification_request=after_verification_request),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(SECRET),
    prefix="/auth",
    tags=["auth"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



# API routes
app.include_router(
    ocr_character_seperator.router,
    prefix="/hello",
    tags=["Hello"],
)

import uvicorn

if __name__ == '__main__':
    uvicorn.run(app='app:app', reload=True, port="7003", host="0.0.0.0")
