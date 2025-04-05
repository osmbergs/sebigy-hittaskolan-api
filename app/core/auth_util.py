import json
from typing import Optional

import fastapi
import jwt
from aiohttp import payload
from attr import dataclass
from fastapi import HTTPException, status, Depends
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings



class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


class RequestContext:
    user_id: str
    email:  str
    first_name:  str
    last_name:  str
    avatar_url:  str

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


    @classmethod
    def from_dict(self, dict):
        ret = RequestContext()

        if "user_id" in dict:
            ret.user_id = dict["user_id"]

        if "email" in dict:
            ret.email = dict["email"]

        if "first_name" in dict:
            ret.first_name = dict["first_name"]

        if "last_name" in dict:
            ret.last_name = dict["last_name"]

        if "avatar_url" in dict:
            ret.avatar_url = dict["avatar_url"]

        return ret

    def __str__(self):
        return self.toJson()

class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self):

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)
    # 👆 new code




    def _createRequestContext(self,payload:dict):




        ret=RequestContext()
        ret.user_id=payload['sub'][6:]

        return ret



    async def verify(self,
                 ):

        ret = RequestContext()
        ret.user_id="dummy"

        return ret


    async def verify_real(self,
                 security_scopes: SecurityScopes,
                 token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
                 ):
        if token is None:
            raise UnauthenticatedException

        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.AUTH0_ALGORITHMS,
                audience=settings.AUTH0_API_AUDIENCE,
                issuer=settings.AUTH0_ISSUER,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))


        return self._createRequestContext(payload)


auth = VerifyToken()