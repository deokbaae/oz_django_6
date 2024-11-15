from tabom.models import Like


def do_like(user_id: int, article_id: int) -> Like:
    """
    get 을 할 필요가 없는 이유
        - Foreign key contraint 가 있기 때문에

    user_id:
        - 이 id 의 user 가 실제로 있는 경우
        - 실제로 없는 경우

    article_id:
        - 이 id 의 article 이 실제로 있는 경우
        - 실제로 없는 경우

    - Foreign key contraint 에 의해서 "실제로 없는 경우는" insert 되지 않는다.
        - db 가 지켜줍니다. (정합성을)
        - 따라서 지금은 크게 신경 안써도 됩니다.

    """
    return Like.objects.create(user_id=user_id, article_id=article_id)


def undo_like(user_id: int, article_id: int) -> None:
    Like.objects.filter(user_id=user_id, article_id=article_id).delete()
