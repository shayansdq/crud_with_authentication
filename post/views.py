import logging

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
import post.permissions as custom_permissions
from post.models import Post
from post.pagination import PageNumberPagination
from post.serializers import PostSerializer
from rest_framework.generics import ListAPIView
from rest_framework import generics

logger = logging.getLogger('django')


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated(), ]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(),
                    custom_permissions.IsOwner()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
