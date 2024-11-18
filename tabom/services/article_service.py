from django.db.models import QuerySet

from tabom.models import Article


def get_an_article(article_id: int) -> Article:
    return Article.objects.get(id=article_id)


# Article 이 들어있는 쿼리셋을 반환할 것이다.
def get_article_list(offset: int, limit: int) -> QuerySet[Article]:
    return Article.objects.order_by("-id")[offset : offset + limit]
