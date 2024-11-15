from django.db import models
from django.db.models import UniqueConstraint


# Create your models here.
class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(BaseModel):
    # django 기본 모델이 auth_user 가 있습니다. 원래는 그걸 사용하는게 맞습니다만
    # 단순화를 위해 user model 도 그냥 생성하겠습니다.
    name = models.CharField(max_length=50)


class Article(BaseModel):
    title = models.CharField(max_length=255)


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=["user", "article"], name="UIX_user_id_article_id")]
