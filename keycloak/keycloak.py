from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
import jwt
from typing import Annotated


oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://localhost:8080/realms/master/protocol/openid-connect/token",
    authorizationUrl="http://localhost:8080/realms/master/protocol/openid-connect/auth",
    refreshUrl="http://localhost:8080/realms/master/protocol/openid-connect/token",
)


async def valid_access_token(
    access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    url = "http://localhost:8080/realms/master/protocol/openid-connect/certs"
    optional_custom_headers = {"User-agent": "custom-user-agent"}
    jwks_client = jwt.PyJWKClient(url, headers=optional_custom_headers)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=["api", "account"],
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Not authenticated")