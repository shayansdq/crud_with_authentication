from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    # user = CourierIncomeSerializer(read_only=True,)
    class Meta:
        model = Post
        exclude = ['user', ]
