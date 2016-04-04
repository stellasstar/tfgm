from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash, authenticate

from gatekeeper import forms

# import custom user model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

PASSWORD_MAX_LENGTH = 30


class UserRegistrationSerializer(serializers.ModelSerializer):

    password_confirmation = serializers.CharField(
                                        max_length=PASSWORD_MAX_LENGTH)

    def validate_password_confirmation(self, attrs, source):
        """
        password_confirmation check
        """
        password_confirmation = attrs[source]
        password = attrs['password']

        if password_confirmation != password:
            raise serializers.ValidationError('Password confirmation mismatch')

        return attrs

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password', 'password_confirmation',
                  'homepage', 'picture', 'latitude', 'longitude')
        non_native_fields = ('password_confirmation', )
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        """ user's full name """
        return obj.get_full_name()

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name',
                  'first_name', 'last_name', 'password',
                  'homepage', 'picture', 'latitude',
                  'longitude', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ('username', 'created',)


class LoginSerializer(serializers.Serializer):

    username=serializers.CharField(max_length=
                                   User._meta.
                                   get_field('username').max_length)
    password=serializers.CharField(max_length=PASSWORD_MAX_LENGTH)

    def user_credentials(self, attrs):
        """
        Provides the credentials required to authenticate the user for login.
        """
        credentials = {}
        credentials["username"] = attrs["username"]
        credentials["password"] = attrs["password"]
        return credentials

    def validate(self, attrs):
        """ checks if login credentials are correct """
        user = authenticate(**self.user_credentials(attrs))

        if user:
            if user.is_active:
                self.instance = user
            else:
                raise forms.ValidationError("This account is inactive.")
        else:
            error = ("Ivalid login credentials.")
            raise serializers.ValidationError(error)
        return attrs


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
            'profile'
        )

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        User.objects.create(**profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        # Update User data
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.email = validated_data.get('first_name',
                                            instance.email)

        # Update UserProfile data
        if not instance.profile:
            User.objects.create(user=instance, **profile_data)
        instance.save()

        # Check if the password has changed
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()
            update_session_auth_hash(self.context.get('request'), instance)

        return instance
