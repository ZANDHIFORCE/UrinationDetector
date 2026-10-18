from blog.models import Post
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    
    class Meta:
        model = Post
        fields = ('title', 'text', 'created_date', 'published_date', 'label', 'image')
    pass