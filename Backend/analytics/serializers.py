from rest_framework import serializers
from .models import Participant, Question, Option, Response

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'label']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'is_multiselect', 'options']
