from rest_framework import serializers
from .models import *


class CrisisAffectedLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisAffectedLocation
        fields = ('lat', 'lng')


class CrisisSerializer(serializers.ModelSerializer):

    affected_locations = CrisisAffectedLocationSerializer(many=True)

    class Meta:
        model = Crisis
        fields = ('id', 'title', 'description', 'scale', 'resolve', 'cmo_crisis_id', 'created_datetime', 'affected_locations')


class CrisisDetailSerializer(serializers.ModelSerializer):

    affected_locations = CrisisAffectedLocationSerializer(many=True)

    class Meta:
        model = Crisis
        fields = ('title', 'description', 'scale', 'resolve', 'cmo_crisis_id', 'created_datetime', 'affected_locations')


class UserGroupSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = ('id', 'rolename', 'image_url', 'get_readable_rolename')

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


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInstruction
        fields = ('text', 'force_lat', 'force_lng', 'created_datetime', 'created_by')


class CombatStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = CombatStrategy
        fields = ('detail', 'created_datetime', 'updated_datetime', 'has_read')
