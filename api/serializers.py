from rest_framework import serializers
import website

class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = website.models.Campus
        fields = '__all__'

    def get_name(self, obj):
        return str(obj)

    name = serializers.SerializerMethodField()


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = website.models.Course
        fields = '__all__'


class YearSerializer(serializers.ModelSerializer):

    class Meta:
        model = website.models.Year
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = website.models.Category
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = website.models.Participant
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = website.models.Team
        fields = '__all__'


class ProblemTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = website.models.ProblemType
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = website.models.Match
