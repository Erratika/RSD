from rest_framework.serializers import ModelSerializer, SlugRelatedField
from .models import Skills, Ages, Lengths, SkillRequirements, Difficulties, Quests


class SkillsSerializer(ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'


class AgesSerializer(ModelSerializer):

    class Meta:
        model = Ages
        fields = '__all__'


class LengthsSerializer(ModelSerializer):

    class Meta:
        model = Lengths
        fields = '__all__'


class SkillRequirementsSerializer(ModelSerializer):
    skill = SlugRelatedField(slug_field='skill_name', read_only=True)

    class Meta:
        model = SkillRequirements
        exclude = ('id',)


class DifficultiesSerializer(ModelSerializer):
    class Meta:
        model = Difficulties
        fields = '__all__'


class QuestsSerializer(ModelSerializer):
    length = SlugRelatedField(slug_field='length', read_only=True)
    age = SlugRelatedField(slug_field='age', read_only=True)
    difficulty = SlugRelatedField(slug_field='difficulty', read_only=True)
    required_skills = SkillRequirementsSerializer(many=True)
    required_quests = SlugRelatedField(slug_field='title', many=True, read_only=True)

    class Meta:
        model = Quests
        fields = ('title',
                  'members',
                  'difficulty',
                  'length',
                  'age',
                  'required_quests',
                  'required_skills',
                  'questPoints')
