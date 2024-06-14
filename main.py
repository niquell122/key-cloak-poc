from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

from fastapi_opa import OPAConfig
from fastapi_opa import OPAMiddleware
from fastapi_opa.auth import OIDCAuthentication
from fastapi_opa.auth import OIDCConfig

from routers.books import router as book_router
from routers.users import router as user_router

config = dotenv_values(".env")

app = FastAPI()

opa_host = "http://localhost:8181"
oidc_config = OIDCConfig(
    well_known_endpoint="http://localhost:8080/realms/master/.well-known/openid-configuration",
    app_uri="http://localhost:8000",
    client_id="Keycloak-poc-1",
    client_secret="JbmgTqJFHzc8jWaBtEq1CvUVarqfpeRz"
    )

oidc_auth = OIDCAuthentication(oidc_config)
opa_config = OPAConfig(authentication=oidc_auth, opa_host=opa_host)

app.add_middleware(OPAMiddleware, config=opa_config)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# Test
@app.get("/")
def root():
    return {"msg": "success"}

app.include_router(book_router, tags=["books"], prefix="/book")
app.include_router(user_router, tags=["users"], prefix="/user")
