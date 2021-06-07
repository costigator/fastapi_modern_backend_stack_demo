from fastapi import APIRouter, Body, HTTPException, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import User, UpdateUser
from apis.login.routers import get_current_active_user
from core.hashing import Hashing

router = APIRouter()

@router.get("/", response_description="List all users")
async def list_users(request: Request):
    users = []
    for doc in await request.app.mongodb["users"].find(projection={"name": 1, "email": 1}).to_list(length=1000):
        users.append(doc)

    return users

@router.post("/", response_description="Create a new user")
async def create_user(request: Request, user: User = Body(...), current_user: User=Depends(get_current_active_user)):
    user = jsonable_encoder(user)
    user['login']['password'] = Hashing.get_password_hash(user['login']['password'])
    new_user = await request.app.mongodb["users"].insert_one(user)
    created_user = await request.app.mongodb["users"].find_one(
        {"_id": new_user.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

@router.get("/{id}", response_description="Get a single user")
async def show_user(id: str, request: Request):
    if (user := await request.app.mongodb["users"].find_one({"_id": id})) is not None:
        user['login']['password'] = "*****************"
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.delete("/{id}", response_description="Delete user")
async def delete_user(id: str, request: Request, current_user: User=Depends(get_current_active_user)):
    delete_result = await request.app.mongodb["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")


@router.put("/{id}", response_description="Update a user")
async def update_user(id: str, request: Request, user: UpdateUser = Body(...), current_user: User=Depends(get_current_active_user)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        if user.get('login'):
            if user.get('login').get('password'):
                user['login']['password'] = Hashing.get_password_hash(user['login']['password'])

        update_result = await request.app.mongodb["users"].update_one(
            {"_id": id}, {"$set": user}
        )

        if update_result.modified_count == 1:
            if (
                updated_user := await request.app.mongodb["users"].find_one({"_id": id})
            ) is not None:
                return updated_user

    if (
        existing_user := await request.app.mongodb["users"].find_one({"_id": id})
    ) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


