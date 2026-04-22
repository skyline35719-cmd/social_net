from rest_framework import serializers

from posts.models import Comment, Group, Post

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title',)
        model = Group

class PostSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    group = serializers.StringRelatedField(read_only=True)
    publication_date = serializers.DateTimeField(
        source='pub_date', read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'group', 'publication_date')

    def get_symbol_quantity(self, obj):
        return len(obj.text)

class CommentSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    post = serializers.StringRelatedField(
        read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment