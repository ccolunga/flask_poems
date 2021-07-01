from flask import Response, request, session
from flask_jwt_extended import create_access_token
from flask_jwt_extended.utils import get_jwt, get_jwt_identity
from mongoengine.queryset.transform import query
from database.models import Category
from flask_restful import Resource
import datetime
from mongoengine.errors import (
    FieldDoesNotExist,
    NotUniqueError,
    DoesNotExist,
    ValidationError,
    InvalidQueryError,
)
from resources.errors import (
    SchemaValidationError,
    EmailAlreadyExistsError,
    UnauthorizedError,
    InternalServerError,
    UpdatingMovieError,
    MovieAlreadyExistsError,
    DeletingMovieError,
)


class CategoryAPI(Resource):
    # @jwt_required()
    def get(self):
        category = Category.objects().to_json()
        return Response(category, mimetype="application/json", status=200)

    # @jwt_required()
    def post(self):
        try:
            # user_id = get_jwt_identity()
            body = request.get_json()
            category = Category(**body)
            category.save()
            id = category.id
            return {"id": str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError()
        except NotUniqueError:
            raise MovieAlreadyExistsError()
        except Exception as e:
            raise InternalServerError()


class CategoriesAPI(Resource):
    # @jwt_required()
    def put(self, id):
        try:
            # user_id = get_jwt_identity()
            body = request.get_json()
            category = Category.objects.get(id=id)
            category.update(**body)
            return {
                "id": str(category.id),
                "message": "Category updated successfully",
            }, 200
        except InvalidQueryError:
            raise SchemaValidationError()
        except DoesNotExist:
            raise UpdatingMovieError()
        except Exception as e:
            raise e  # InternalServerError()

    # @jwt_required()
    def delete(self, id=None):
        try:
            # user_id = get_jwt_identity()
            category = Category.objects.get(id=id)
            category.delete()
            return {"message": "Category deleted successfully"}, 200
        except DoesNotExist:
            raise DeletingMovieError()
        except Exception:
            raise InternalServerError()
