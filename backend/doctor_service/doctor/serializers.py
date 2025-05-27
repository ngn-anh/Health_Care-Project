from rest_framework import serializers

class DoctorSerializer(serializers.Serializer):
    id = serializers.CharField()
    user = serializers.CharField()
    specialty = serializers.CharField()
    department = serializers.CharField()
