from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from keycloak import valid_access_token

from models import Book, BookUpdate

router = APIRouter()

@router.get('/')
def get_user():
    return {"message": "/user"}
