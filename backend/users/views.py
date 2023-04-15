from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

from api.pagination import CustomPagination
from users.models import Follow, User
from users.serializers import (
    CustomUserSerializer,
    FollowSerializer,
)


class CustomUserViewSet(UserViewSet):
    """
    ViewSet для работы с пользователями.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        """Список подписок пользоваетеля."""
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, id):
        """Создаёт или удаляет подписку на пользователя."""
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {'errors': 'На себя нельзя подписаться / отписаться'},
                status=HTTP_400_BAD_REQUEST)
        subscription = Follow.objects.filter(
            author=author, user=user)
        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    {'errors': 'Нельзя подписаться повторно'},
                    status=HTTP_400_BAD_REQUEST)
            queryset = Follow.objects.create(author=author, user=user)
            serializer = FollowSerializer(
                queryset, context={'request': request})
            return Response(serializer.data, status=HTTP_201_CREATED)
        if not subscription.exists():
            return Response(
                {'errors': 'Нельзя отписаться повторно'},
                status=HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=HTTP_204_NO_CONTENT)
