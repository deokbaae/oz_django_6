from django.http import HttpRequest
from ninja import Router, Schema

from tabom.models import Like
from tabom.services.like_service import do_like

router = Router()


class LikeRequest(Schema):
    """
    좋아료를 생성할 때, user_id 와 article_id 가 필요하니까.
    """

    user_id: int
    article_id: int


class LikeResponse(Schema):
    """
    이런 형태의 json 이 클라이언트에게 응답으로 내려가게 됩니다.
    """

    id: int
    user_id: int
    article_id: int


@router.post("/", response={201: LikeResponse})
def post_like(request: HttpRequest, like_request: LikeRequest) -> tuple[int, Like]:
    like = do_like(like_request.user_id, like_request.article_id)
    return 201, like
