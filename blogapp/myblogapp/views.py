from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import Post, Comments, Likes, CustomUser
from .serializers import (
    PostSerializer, LikesSerializer, CommentsSerializer, 
    UserSerializer, loginSerializer
)


# Simple home view
def home(request):
    return HttpResponse('Welcome to my blog app')


# User registration view
class UserRegistration(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

registration_view = UserRegistration.as_view()


# User login view
class LoginView(generics.GenericAPIView):
    serializer_class = loginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(email=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

login_view = LoginView.as_view()


# View for creating and listing posts, with optional filtering by user ID.
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_id = request.query_params.get('user_id')
        
        # Filter posts by user if 'user_id' is provided.
        if user_id:
            posts_by_user = queryset.filter(created_by=user_id)
            if not posts_by_user.exists():
                return Response({'error': 'User has not posted yet'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(posts_by_user, many=True)
        else:
            # Return all posts if no 'user_id' filter is provided.
            serializer = PostSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def perform_create(self, serializer):
        media = serializer.validated_data.get('media')
        text_content = serializer.validated_data.get('text_content')
        user = self.request.user

        # Ensure that either media or text_content is provided.
        if not media and not text_content:
            raise serializer.ValidationError({'error': 'Both media and text_content cannot be empty'})

        serializer.save(created_by=user)

post_list_view = PostListView.as_view()


# View for creating a comment on a post.
class CreateComment(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(post=post, user=self.request.user)

create_comment_view = CreateComment.as_view()


# View for liking or unliking a post.
class CreateLike(generics.GenericAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        # Toggle like status
        like, created = Likes.objects.get_or_create(post=post, user=user)
        if not created:
            like.delete()
            return Response({'message': 'Disliked'}, status=status.HTTP_200_OK)

        return Response({'message': 'Liked'}, status=status.HTTP_201_CREATED)

create_like_view = CreateLike.as_view()


# View for retrieving, updating, and deleting a specific post.
class RetrieveUpdateAndDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.created_by != request.user:
            return Response({'error': 'You are not authorized to update this post.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.created_by != request.user:
            return Response({'error': 'You are not authorized to delete this post.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

retrieve_update_and_delete_view = RetrieveUpdateAndDelete.as_view()
