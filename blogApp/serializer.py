from rest_framework import serializers
from blogApp.models import User,Blogs,Comment,Reply
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type": "password"},)


class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    password = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['first_name','middle_name', 'last_name', 'profile_picture', 'dob', 'email', 'password','confirm_pass']

    def save(self):
        user = User(
            first_name=self.validated_data['first_name'],
            middle_name=self.validated_data['middle_name'],
            last_name=self.validated_data['last_name'],
            dob=self.validated_data['dob'],
            profile_picture=self.validated_data['profile_picture'],
            email=self.validated_data['email']

        )
        password = self.validated_data['password']
        confirm_pass = self.validated_data['confirm_pass']
        if password != confirm_pass:
            raise serializers.ValidationError({'password' : 'Passwords does not match'})
        user.set_password(password)
        user.save()
        return user

class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model=Blogs
        fields=['id','user','created_on','last_updated','picture','caption']
    

class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model=Reply
        fields=['id','comment','reply_text']

    def create(self,validated_data):
        validated_data['reply_by'] = User.objects.get(email=self.context.get('request').user)
        return Reply.objects.create(**validated_data)

    
class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)
    class Meta:
        model=Comment
        fields=['id','blog','comment_text','replies']
    
    def create(self,validated_data):
        validated_data['comment_by'] = User.objects.get(email=self.context.get('request').user)
        return Comment.objects.create(**validated_data)
    
   
    
    
