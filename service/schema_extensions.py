# from drf_spectacular.extensions import OpenApiAuthenticationExtension
#
# class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
#     target_class = "service.authentication.CustomJWTAuthentication"
#     name = "JWTAuth"
#
#     def get_security_definition(self, auto_schema):
#         return {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#             "description": "JWT-based authentication. Provide the token in the `Authorization` header as `Bearer <token>`.",
#         }
