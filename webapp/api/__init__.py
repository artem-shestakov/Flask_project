from flask_restful import Api
from .post.routes import PostApi, CommentPostApi, CommentsApi
from .users.resources import AvatarApi


# Register API module
def create_module(app, **kwargs):
    rest_api = Api(app)

    rest_api.add_resource(
        AvatarApi,
        "/api/users/<user_id>/avatar"
    )

    rest_api.add_resource(
        PostApi,
        "/api/post",
        "/api/post/<int:post_id>"
    )

    rest_api.add_resource(
        CommentPostApi,
        "/api/post/<int:post_id>/comments"
    )

    rest_api.add_resource(
        CommentsApi,
        "/api/comments/<int:comment_id>"
    )

