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


class CommentsAPI(Resource):
    def get(self):
        query = Comments.objects()
        comments = Comments.objects().to_json()
        return Response(comments, mimetype="application/json", status=200)

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("comment_id")
            args = parser.parse_args()
            comment_id = args["comment_id"]

            comment = Comments.objects.get(id=comment_id)

            comment.delete()
            return {"message": args}
        except Exception as e:
            raise e


class CommentAPI(Resource):
    def post(self, poem_id=None):
        try:
            body = request.get_json()
            poem = Poems.objects.get(id=poem_id)
            comment = Comments(**body)
            comment.save()
            poem.comments.append(comment.id)
            poem.save()
            return {"id_comment": str(comment.id), "id_poem": str(poem.id)}, 200
        except Exception as e:
            raise e
