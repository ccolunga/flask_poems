from werkzeug.exceptions import HTTPException


class InternalServerError(HTTPException):
    code = 500
    description = ("Something went wrong")


class SchemaValidationError(HTTPException):
    code = 400
    description = ("Request is missing required fields")


class MovieAlreadyExistsError(HTTPException):
    code = 400
    description = ("Movie with given name already exists")


class UpdatingMovieError(HTTPException):
    code = 400
    description = ("Updating movie added by other is forbidden")


class DeletingMovieError(HTTPException):
    code = 403
    description = ("Deleting movie added by other is forbidden")


class MovieNotExistsError(HTTPException):
    code = 400
    description = ("Movie with given id doesn't exists")


class EmailAlreadyExistsError(HTTPException):
    code = 400
    description = ("User with given email address already exists")


class UnauthorizedError(HTTPException):
    code = 401
    description = ("Invalid username or password")


class BadTokenError(HTTPException):
    code = 403
    description = ("Invalid token")


class EmailDoesnotExistsError(HTTPException):
    code = 400
    description = ("Couldn't find the user with given email address")
