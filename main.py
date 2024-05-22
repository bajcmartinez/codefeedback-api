import sys

from fastapi import FastAPI
from app import api
from utils.auth import auth

app = FastAPI()

app.include_router(api.router)

if 'pytest' in sys.modules:
    def override_auth_get_authenticated_user():
        return {
            "sub": "auth0|test",
            "org_id": "org_test"
        }


    app.dependency_overrides[auth.get_authenticated_user] = override_auth_get_authenticated_user
