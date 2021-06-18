from flask import Response, request, session
from flask_jwt_extended import create_access_token
from mongoengine.queryset.transform import query
from database.models import User
from flask_restful import Resource
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import (
    SchemaValidationError,
    EmailAlreadyExistsError,
    UnauthorizedError,
    InternalServerError,
)


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {"id": str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError()
        except NotUniqueError:
            raise EmailAlreadyExistsError()
        except Exception as e:
            raise e  # InternalServerError()


class LogoutApi(Resource):
    def post(self):
        print(request)
        return {"logout": "logrado"}, 200


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get("email"))
            authorized = user.check_password(body.get("password"))
            if not authorized:
                raise UnauthorizedError()

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=str(user.id), expires_delta=expires
            )
            return {"token": access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError()
        except Exception as e:
            raise InternalServerError()


class UsersAPI(Resource):
    def get(self):
        query = User.objects()
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)
