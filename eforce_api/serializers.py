from rest_framework import serializers
from .models import *


class CrisisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crisis
        fields = ('id', 'title')


class CrisisDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crisis
        fields = ('title', 'description', 'scale', 'resolve', 'cmo_crisis_id', 'created_datetime')


class UserGroupSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = ('id', 'rolename', 'image_url', )

    def get_image_url(self, user_group):
        if not user_group.image:
            return None
        return user_group.image.url


class CrisisUpdateSerializer(serializers.ModelSerializer):

    by_group = UserGroupSerializer()

    class Meta:
        model = CrisisUpdate
        fields = ('description', 'created_datetime', 'force_lat',
                  'force_lng', 'force_size', 'force_casualty', 'known_casualty',
                  'known_dead', 'for_crisis', 'get_readable_sent_by', 'by_group')


class UserGroupImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('image', )
