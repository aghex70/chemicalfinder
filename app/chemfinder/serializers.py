# from rest_framework import serializers
# from .models import (Company, Position, Opinion)
#
#
# class PositionSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Position
#         # fields = ('pk', 'name', 'email', 'document', 'phone', 'registrationDate')
#
#
# class PositionQuerySerializer(serializers.Serializer):
#     role = serializers.CharField(default="Python")
#     location = serializers.CharField(default="Madrid")
#
#     def save(self):
#         position = {
#             "role": "Python" if self.validated_data['role'] == "string" else self.validated_data['role'],
#             "location": "Madrid" if self.validated_data['location'] == "string" else self.validated_data['location'],
#         }
#
#         return position
