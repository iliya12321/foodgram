from core.enums import Limits
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    CharField,
    EmailField,
    ForeignKey,
    Model,
    UniqueConstraint,
)

from users.validators import validate_username


class User(AbstractUser):
    email = EmailField(
        'Адрес электронной почты',
        max_length=Limits.MAX_LEN_EMAIL_FIELD.value,
        unique=True,
    )
    username = CharField(
        'Уникальный юзернейм',
        max_length=Limits.MAX_LEN_USERS_CHARFIELD.value,
        unique=True,
        validators=[validate_username],
    )
    first_name = CharField(
        'Имя',
        max_length=Limits.MAX_LEN_USERS_CHARFIELD.value,
    )
    last_name = CharField(
        'Фамилия',
        max_length=Limits.MAX_LEN_USERS_CHARFIELD.value,
    )
    password = CharField(
        'Пароль',
        max_length=Limits.MAX_LEN_PASSWORD.value,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Автор',
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
