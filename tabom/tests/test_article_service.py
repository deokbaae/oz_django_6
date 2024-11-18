from django.test import TestCase

from tabom.models import Article, Like, User
from tabom.services.article_service import get_an_article, get_article_list


class TestArticleService(TestCase):
    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title=title)

        # When
        result_article = get_an_article(article.id)

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(invalid_article_id)

    def test_get_article_list_should_prefetch_likes(self) -> None:
        # Given
        user = User.objects.create(name="user1")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]  # 20 개의 article 생성
        Like.objects.create(user_id=user.id, article_id=articles[-1].id)

        # When
        result_articles = get_article_list(0, 10)

        # Then
        with self.assertNumQueries(2):

            # 실제로 쿼리가 나가는 지점. (왜? len() 으로 감쌋기 때문에,
            # queryset 은 evaluate 될 때 sql 이 실행되니까)
            self.assertEqual(len(result_articles), 10)  # 길이가 10개가 맞는지

            self.assertEqual(1, result_articles[0].like_set.count())

            # 내림차순대로 10개가 가져와진 것이 맞는지
            self.assertEqual([a.id for a in reversed(articles[10:21])], [a.id for a in result_articles])
