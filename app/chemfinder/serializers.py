from rest_framework import serializers


class NERSerializer(serializers.Serializer):
    TYPE_CHOICES = ('ner', 'chemner', 'trained_ner')
    type = serializers.ChoiceField(choices=TYPE_CHOICES)
