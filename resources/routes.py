from .auth import SignupApi, LoginApi, LogoutApi, UsersAPI
from .reset_password import ForgotPassword, ResetPassword
from .poems import PoemsAPI, PoemAPI
from .categories import CategoriesAPI, CategoryAPI
from .comments import CommentAPI, CommentsAPI


def initialize_routes(api):
    # Poems
    api.add_resource(PoemsAPI, "/api/poems")
    api.add_resource(PoemAPI, "/api/poems/<id>")

    # Comments
    api.add_resource(CommentsAPI, "/api/comments")
    api.add_resource(CommentAPI, "/api/comments/<poem_id>")

    # Categories
    api.add_resource(CategoryAPI, "/api/categories")
    api.add_resource(CategoriesAPI, "/api/categories/<id>")

    # Users
    api.add_resource(UsersAPI, "/api/auth/users")

    # Auth
    api.add_resource(SignupApi, "/api/auth/signup")
    api.add_resource(LoginApi, "/api/auth/login")
    api.add_resource(LogoutApi, "/api/auth/logout")

    # Reset/Forgot
    api.add_resource(ForgotPassword, "/api/auth/forgot")
    api.add_resource(ResetPassword, "/api/auth/reset")
