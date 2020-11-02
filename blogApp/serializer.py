from rest_framework import serializers
from blogApp.models import User


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
        fields = ['first_name','middle_name', 'last_name','date_joined', 'last_login', 'profile_picture', 'dob', 'email', 'password','confirm_pass']

    def save(self):
        user = User(
            first_name=self.validated_data['first_name'],
            middle_name=self.validated_data['middle_name'],
            last_name=self.validated_data['last_name'],
            dob=self.validated_data['dob'],
            date_joined = self.validated_data['date_joined'],
            last_login = self.validated_data['last_login'],
            is_active =True,
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