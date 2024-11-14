from django.db import models

# Create your models here.


class User(models.Model):
    # django 기본 모델이 auth_user 가 있습니다. 원래는 그걸 사용하는게 맞습니다만
    # 단순화를 위해 user model 도 그냥 생성하겠습니다.
    name = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
