from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from .models import Post

from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import PostSerializer

from rest_framework.response import Response
from rest_framework import status


class IntruderImage(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class LatestUCFPostView(APIView):
    def get(self, request):
        try:
            latest_post = Post.objects.filter(label="UCF").first()  # created_at 필드를 기준으로 가장 최신 데이터 가져오기
            serializer = PostSerializer(latest_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"detail": "No posts available."}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        try:
            latest_post = Post.objects.filter(label="UCF").first()
            if not latest_post:
                return Response({"detail": "No posts available."}, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(latest_post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

