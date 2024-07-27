# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List

app = FastAPI()
users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    return users


@app.post("/user", response_model=User)
async def post_user(user: User) -> User:
    user.id = len(users) + 1
    users.append(user)
    return user


@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, new_data: User = Body()) -> User:
    for user in users:
        if user.id == user_id:
            user.username = new_data.username
            user.age = new_data.age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            del_user = user
            users.remove(user)
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")