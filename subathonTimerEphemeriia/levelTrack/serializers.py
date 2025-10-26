from rest_framework import serializers
from .models import LevelTracker

class LevelTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelTracker
        fields = ['id', 'current_level', 'target_level', 'started_at']
