from rest_framework import serializers
from .models import Post, CustomUser, Likes,Comments


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password_confirmation = serializers.CharField(write_only =True)
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password','password_confirmation']


    def validate(self, attrs):
            
            if attrs['password'] != attrs['password_confirmation']:
                raise serializers.ValidationError({'error':'passwords dont match'})
            return attrs
        

    def create(self, validated_data):
            validated_data.pop('password_confirmation')

            user = CustomUser(
                username=validated_data['username'],
                email = validated_data['email'],

            )
            user.set_password(validated_data['password'])

            user.save()


            return user



class loginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)




class LikesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    
    class Meta:
        model = Likes
        fields = ['id', 'user']

  



class CommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Comments
        fields = ['id', 'user', 'comment']


    def validate_content(self, value):
         if not value.strip():
              return serializers.ValidationError('cannot have empty comment')
         

         return value

    





class PostSerializer(serializers.ModelSerializer):
    # you serializing it so as to get all information about the user rather than only the id....
    created_by = UserSerializer(read_only = True)
    comments = CommentsSerializer(many= True, read_only = True)
    likes = LikesSerializer(many = True, read_only = True)
    likes_counts = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'text_content', 'media', 'created_by', 'comments', 'likes', 'likes_counts']
    
    def get_likes_counts(self, obj):
        return obj.likes.count()




