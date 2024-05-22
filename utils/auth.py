from auth0_fastapi import Auth0JWTBearerTokenValidator

from utils.config import get_settings

settings = get_settings()

auth = Auth0JWTBearerTokenValidator(
    domain=settings.auth0_domain,
    audience=settings.auth0_audience,
    issuer=settings.auth0_issuer
)
