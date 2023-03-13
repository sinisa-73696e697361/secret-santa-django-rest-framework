"""
Serializers for user APIs
"""
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model
    """

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """
        Creates and returns user
        :param validated_data:
        :return: user
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Updates and returns user
        :param validated_data:
        :return: user
        """
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for user's token
    """

    email = serializers.EmailField()

    # input type will be only visible in documentation
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, parameters):
        """
        Validation and authentication of user
        :param parameters:
        :return:
        """
        email = parameters.get("email")
        password = parameters.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            message = _("Provided credentials are not correct")
            raise serializers.ValidationError(message, code="authorization")

        parameters["user"] = user
        return parameters
