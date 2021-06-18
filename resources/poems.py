from flask import Response, request
from database.models import Poems, User, Comments, Category
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import (
    FieldDoesNotExist,
    NotUniqueError,
    DoesNotExist,
    ValidationError,
    InvalidQueryError,
)
from resources.errors import (
    SchemaValidationError,
    MovieAlreadyExistsError,
    InternalServerError,
    UpdatingMovieError,
    DeletingMovieError,
    MovieNotExistsError,
)


class PoemsAPI(Resource):
    def get(self):
        query = Poems.objects()
        movies = Poems.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    # @jwt_required()
    def post(self):
        try:
            # user_id = get_jwt_identity()
            body = request.get_json()
            # user = User.objects.get(id=user_id)
            poem = Poems(**body)
            poem.save()
            # user.update(push__poems=p)
            # user.save()
            id = poem.id
            return {"id": "Complete"}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError()
        except NotUniqueError:
            raise MovieAlreadyExistsError()
        except Exception as e:
            raise InternalServerError()


class PoemAPI(Resource):
    def get(self, id=None):
        try:
            poem = Poems.objects.get(id=id).to_json()
            return Response(poem, mimetype="application/json", status=200)
        except DoesNotExist:
            raise MovieNotExistsError()
        except Exception:
            raise InternalServerError()


# class MovieApi(Resource):
#     @jwt_required()
#     def put(self, id):
#         try:
#             user_id = get_jwt_identity()
#             movie = Movie.objects.get(id=id, added_by=user_id)
#             body = request.get_json()
#             print(body)
#             movie_update = Movie.objects.get(id=id).update(**body)
#             return {
#                 "message": "Movie successfully updated",
#                 "id": str(movie.id),
#             }, 200
#         except InvalidQueryError:
#             raise SchemaValidationError()
#         except DoesNotExist:
#             raise UpdatingMovieError()
#         except Exception:
#             raise InternalServerError()

#     @jwt_required()
#     def delete(self, id=None):
#         try:
#             user_id = get_jwt_identity()
#             poem = Poems.objects.get(id=id)
#             poem.delete()
#             return "Poem successfully deleted", 200
#         except DoesNotExist:
#             raise DeletingMovieError()
#         except Exception:
#             raise InternalServerError()
