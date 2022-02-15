from django.db.models import fields
from rest_framework import serializers
from .models import User
import random
import string


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.referral_id = UserSerializers.referral_code()
        instance.save()
        return instance

    def referral_code():
        referral = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(7))
        referral = 'G4' + referral
        return referral
