# myapp/jwt_middleware.py
from django.http import JsonResponse
from token_utils import decode_jwt  # Import your decode_jwt function

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Retrieve the token from the Authorization header
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            # Expecting header format: "Bearer <token>"
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
                decoded_payload = decode_jwt(token)
                if decoded_payload:
                    # Attach the decoded payload to the request object
                    request.jwt_payload = decoded_payload
                else:
                    # Optional: Return an unauthorized response if token is invalid/expired
                    return JsonResponse({"detail": "Invalid or expired token."}, status=401)
            else:
                # Optional: Return an error if the token format is incorrect
                return JsonResponse({"detail": "Invalid or expired token."}, status=401)
        else:
            # If no token is provided, you can either set jwt_payload to None
            # or, if authentication is mandatory, return an unauthorized response.
            request.jwt_payload = None
            # Uncomment the following lines to enforce token presence:
            # return JsonResponse({"detail": "Authorization header missing."}, status=401)

        # Process the request further down the middleware chain / view
        response = self.get_response(request)
        return response
