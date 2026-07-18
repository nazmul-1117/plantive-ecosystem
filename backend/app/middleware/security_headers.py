from fastapi.requests import Request

from app.constants.security_headers import (
    X_CONTENT_TYPE_OPTIONS,
    X_FRAME_OPTIONS,
    REFERER_POLICY
)

async def security_header_middleware(request: Request, call_next):
    response = await call_next(request)

    # Prevent browsers from guessing (sniffing) the MIME type.
    # Forces the browser to respect the Content-Type sent by the server.
    # Helps mitigate certain content-sniffing attacks.
    response.headers["X-Content-Type-Options"] = X_CONTENT_TYPE_OPTIONS

    # Prevent this application from being embedded inside an <iframe>.
    # Protects against clickjacking attacks, where users are tricked into
    # interacting with a hidden version of your website.
    response.headers["X-Frame-Options"] = X_FRAME_OPTIONS
    
    # Control how much referrer information the browser sends when users
    # navigate to another website.
    # "strict-origin-when-cross-origin" sends the full URL for same-origin
    # requests, but only the origin (e.g., https://plantive.com) to other sites.
    response.headers["Referrer-Policy"] = REFERER_POLICY

    return response