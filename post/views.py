from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from post.models import Post
from post.serializers import PostSerializer
from rest_framework.generics import ListAPIView
from rest_framework import generics


# Create your views here.
# class ListApiView(ListAPIView, generics.):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
# pagination_class = #TODO


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    # permission_classes =
    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':  # TO_DO
            print('in create')
            return [permissions.IsAuthenticated(), ]
        elif self.action == 'update' or self.action == 'partial_update':
            return [permissions.IsAuthenticated(), ]  # You can define your own custom permission class
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), ]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
