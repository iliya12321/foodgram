from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPagination
from users.models import Follow, User
from users.serializers import (
    CustomUserSerializer,
    FollowSerializer,
    FollowListSerializer,
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
        pages = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = FollowListSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            context = {'request': request}
            data = {
                'user': user.id,
                'author': author.id
            }
            serializer = FollowSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=HTTP_201_CREATED
            )
        subscribe = get_object_or_404(
            Follow,
            user=user,
            author=author
        )
        subscribe.delete()
        return Response(status=HTTP_204_NO_CONTENT)
