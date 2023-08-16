from django.db import models
from django.contrib.auth.models import User


#  Создаём модель Author
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один к одному со встроенной моделью User
    rating = models.FloatField(default=0.0)  # Рейтинг автора - число с плавающей точкой

    def update_rating(self):  # Метод обновления рейтинга автора
        # Рейтинг всех постов автора
        post_rating = self.post_set.aggregate(total_rating=models.Sum('rating'))['total_rating'] or 0
        # Рейтинг всех комментариев пользователя
        comment_rating = self.comment_set.aggregate(total_rating=models.Sum('rating'))['total_rating'] or 0
        # Рейтинг всех комментариев под постом автора
        comment_post_rating = self.post_set.annotate(total_rating=models.Sum('comment__rating')).aggregate(
            total_rating=models.Sum('total_rating'))['total_rating'] or 0
        #  Общая сумма рейтинга
        self.rating = post_rating * 3 + comment_rating + comment_post_rating
        self.save()


# Создаём модель Category
class Category(models.Model):
    # Название категории (небольшой 255 символов, должно быть уникальным)
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Связь  один ко многим с моделью Author
    article = models.BooleanField(default=False)  # Статья(False) или новость(True)
    time_add = models.DateTimeField(auto_now_add=True)  # Текущая дата и время создания
    # Связь многие ко многим с моделью Category через модель PostCategory
    category = models.ManyToManyField(Category, through="PostCategory")
    name = models.CharField(max_length=255)  # Название статьи/новости
    text = models.CharField(max_length=255)  # Текст статьи/новости
    rating = models.FloatField(default=0.0)  # Рейтинг статьи/новости

    #  Метод увеличения рейтинга статьи/новости
    def like(self):
        self.rating += 1
        self.save()

    #  Метод уменьшения рейтинга статьи/новости
    def dislike(self):
        self.rating -= 1
        self.save()

    #  Метод предпросмотра статьи/новости (124 символа)
    def preview(self):
        return self.text[:124] + "..." if len(self.text) > 124 else self.text


#  Создаём вспомогательную модель PostCategory
class PostCategory(models.Model):
    #  Связь один ко многим с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #  Связь один ко многим с моделью Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


#  Создаём модель Comment
class Comment(models.Model):
    #  Связь один ко многим с моделью Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    #  Связь один ко многим с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #  Связь один ко многим с моделью User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #  Текст комментария (не больше 255 символов)
    text = models.CharField(max_length=255)
    # Текущая дата и время создания комментария
    time_add = models.DateTimeField(auto_now_add=True)
    # Рейтинг комментария
    rating = models.FloatField(default=0.0)

    #  Метод увеличения рейтинга комментария
    def like(self):
        self.rating += 1
        self.save()

    #  Метод уменьшения рейтинга комментария;
    def dislike(self):
        self.rating -= 1
        self.save()

    time_add = models.DateTimeField(auto_now_add=True)
    # Рейтинг комментария
    rating = models.FloatField(default=0.0)

    #  Метод увеличения рейтинга комментария
    def like(self):
        self.rating += 1
        self.save()

    #  Метод уменьшения рейтинга комментария
    def dislike(self):
        self.rating -= 1
        self.save()
