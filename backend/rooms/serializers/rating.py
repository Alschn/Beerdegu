from rest_framework import serializers

from rooms.models import Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = (
            'color', 'foam', 'smell', 'taste', 'opinion', 'note', 'beer'
        )

    def to_representation(self, instance: Rating):
        my_fields = self.Meta.fields
        data = super().to_representation(instance)

        # Replace None with empty string, so that client does not receive nulls
        for field in my_fields:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
