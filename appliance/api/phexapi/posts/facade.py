from phexcore import services

from .controller import PostsService


def posts() -> PostsService:
    return services.get("posts")
