from rest_framework import serializers
from blogApp.models import User,Blogs
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
    def newsave(self,user):
        today=date.today()
        d=today.strftime("%B %d, %Y")
        blog=Blogs(
        user=user,
        created_on=d,
        last_updated=d,
        picture=self.validated_data['picture'],
        caption=self.validated_data['caption'],

        )
        blog.save()
        return blog
