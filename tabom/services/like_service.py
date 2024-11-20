from django.db.models import F

from tabom.models import Article, Like


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
    like = Like.objects.create(user_id=user_id, article_id=article_id)
    Article.objects.filter(id=article_id).update(like_count=F("like_count") + 1)
    return like


def undo_like(user_id: int, article_id: int) -> None:
    # get() 이후에 delete() 하는 방법
    # like = Like.objects.filter(user_id=user_id, article_id=article_id).get()  # SELECT
    # like.delete()  # DELETE

    # queryset 에 delete() 를 호출하는 방법
    # 대부분의 경우에는 더 나은 방법.
    # 삭제할 데이터가 없어도 에러 없습니다.

    # 삭제를 성공했을때 -> 삭제된 좋아요 개수만큼 like_count 차감
    # 삭제 실패했을때 -> like_count 를 차감하지 않는다.
    # 삭제를 성공했는지, 실패했는지, 성공을 헀다면 몇개를 삭제했는지 알 수 있는 방법?
    # 제일 좋은 방법: django 문서 정독 -> 문서가 많고 영어고 어렵다.
    # 차선책: 디버깅
    #   중단점을 먼저 찍는다.
    # 코드를 실행할 방법도 모른다면: 전체 테스트 슈트를 디버그 모드로 실행한다.
    deleted_cnt, _ = Like.objects.filter(user_id=user_id, article_id=article_id).delete()  # DELETE
    if deleted_cnt:  # integer 가 0 이면 False 로 취급. 파이썬에는 Falsy 와 Truthy 의 개념이 있기 때문입니다.
        article = Article.objects.get(id=article_id)
        article.like_count -= 1
        article.save()
