from flask import Response, request
from database.models import Comments, Poems
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from bson import ObjectId
import re
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


def delete_comments(array):
    for arr in array:
        id = arr["id"]
        comment = Comments.objects.get(id=id)
        comment.delete()


def convert_body_str_to_object(body):
    exp = "[a-z0-9]{24}"
    for value in body:
        if re.findall(exp, body[value]):
            body[value] = ObjectId(body[value])
    return body


class PoemsAPI(Resource):
    def get(self):
        movies = Poems.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    # @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            poem = Poems(**body)
            poem.save()
            id = poem.id
            return {"id": str(id)}, 200
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

    def put(self, id):
        try:
            body = request.get_json()
            poem = Poems.objects.get(id=id)
            convert_body = convert_body_str_to_object(body)
            poem.update(**convert_body)
            return {"id": str(poem.id), "message": "Poem updated successfully"}, 200
        except InvalidQueryError:
            raise SchemaValidationError()
        except DoesNotExist:
            raise UpdatingMovieError()
        except Exception as e:
            raise e  # InternalServerError()

    # @jwt_required()
    def delete(self, id=None):
        try:
            poem = Poems.objects.get(id=id)
            delete_comments(poem.comments)
            poem.delete()
            return {"message": "Poem successfully deleted"}, 200
        except DoesNotExist:
            raise DeletingMovieError()
        except Exception as e:
            raise e  # InternalServerError()


class SearchPoemAPI(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("q")
            parser.add_argument("author")
            args = parser.parse_args()
            print(f'args["author"] -->>  {args["author"]}')
            print(f'args["q"] -->>  {args["q"]}')
            if args["author"] is not None:
                author = args["author"]
                poem = Poems.objects(author=author).to_json()
                return Response(poem, mimetype="application/json", status=200)
            else:
                query = args["q"]
                poem = Poems.objects.search_text(query).to_json()
                return Response(poem, mimetype="application/json", status=200)
        except Exception as e:
            raise e
            # else:

            # poem = Poems.objects.find(title=q)
