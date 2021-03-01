from rest_framework import serializers

from main.models import RiskType, Field, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True, required=False)

    class Meta:
        """Meta class for the User serializer."""

        model = User
        fields = ('email', 'id')


class FieldSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        """Meta class for the field serializer."""

        model = Field
        fields = '__all__'


class RiskTypeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, required=False)
    fields = FieldSerializer(many=True, allow_empty=True, required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        """Meta class for the risk type serializer."""

        model = RiskType
        fields = ('id', 'name', 'user', 'fields')

    def to_internal_value(self, data):
        """Modify the data value update."""

        if not self.instance:
            return super(RiskTypeSerializer, self).to_internal_value(data)

        risk_type = self.instance
        risk_type.fields.clear()
        fields = data.pop('fields')
        for field in fields:
            field_obj_qs = Field.objects.filter(id=field.get('id'))
            if field_obj_qs.exists():
                risk_type.fields.add(field_obj_qs.first())
        return super(RiskTypeSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        """Create method."""
        fields = validated_data.pop('fields')

        risk_type = RiskType.objects.create(**validated_data)
        for field in fields:
            if field.get('id'):
                try:
                    field_obj = Field.objects.get(id=field['id'])
                except Field.DoesNotExist:
                    field.pop('id')
                    field_obj = Field.objects.create(**field)
            else:
                field_obj = Field.objects.create(**field)
            risk_type.fields.add(field_obj)

        return risk_type
