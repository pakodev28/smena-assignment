from rest_framework import serializers

from .models import Check, Printer


class GetCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ("id",)


class CreateCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = ("point_id",)

    def to_representation(self, value):
        serializer = GetCheckSerializer(value, context=self.context)
        return serializer.data
