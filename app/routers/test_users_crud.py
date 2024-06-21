from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from routers.users import router as user_router

# TODO: FIX

app = FastAPI()
config = dotenv_values(".env")
app.include_router(user_router, tags=["users"], prefix="/user")


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"] + "test"]

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
    app.database.drop_collection("users")

def test_create_user():
    with TestClient(app) as client:
        response = client.post("/user/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."})
        assert response.status_code == 201

        body = response.json()
        assert body.get("title") == "Don Quixote"
        assert body.get("author") == "Miguel de Cervantes"
        assert body.get("synopsis") == "..."
        assert "_id" in body


def test_create_user_missing_title():
    with TestClient(app) as client:
        response = client.post("/user/", json={"author": "Miguel de Cervantes", "synopsis": "..."})
        assert response.status_code == 422


def test_create_user_missing_author():
    with TestClient(app) as client:
        response = client.post("/user/", json={"title": "Don Quixote", "synopsis": "..."})
        assert response.status_code == 422


def test_create_user_missing_synopsis():
    with TestClient(app) as client:
        response = client.post("/user/", json={"title": "Don Quixote", "author": "Miguel de Cervantes"})
        assert response.status_code == 422


def test_get_user():
    with TestClient(app) as client:
        new_user = client.post("/user/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        get_user_response = client.get("/user/" + new_user.get("_id"))
        assert get_user_response.status_code == 200
        assert get_user_response.json() == new_user


def test_get_user_unexisting():
    with TestClient(app) as client:
        get_user_response = client.get("/user/unexisting_id")
        assert get_user_response.status_code == 404


def test_update_user():
    with TestClient(app) as client:
        new_user = client.post("/user/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        response = client.put("/user/" + new_user.get("_id"), json={"title": "Don Quixote 1"})
        assert response.status_code == 200
        assert response.json().get("title") == "Don Quixote 1"


def test_update_user_unexisting():
    with TestClient(app) as client:
        update_user_response = client.put("/user/unexisting_id", json={"title": "Don Quixote 1"})
        assert update_user_response.status_code == 404


def test_delete_user():
    with TestClient(app) as client:
        new_user = client.post("/user/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        delete_user_response = client.delete("/user/" + new_user.get("_id"))
        assert delete_user_response.status_code == 204


def test_delete_user_unexisting():
    with TestClient(app) as client:
        delete_user_response = client.delete("/user/unexisting_id")
        assert delete_user_response.status_code == 404