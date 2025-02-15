# apps/redirects/serializers/redirect_rule.py
from rest_framework import serializers
from apps.redirects.models.redirect_rule import RedirectRule


class RedirectRuleSerializer(serializers.ModelSerializer):
    """
    Serializer for RedirectRule model
    """
    created_by = serializers.ReadOnlyField(source='created_by.username')
    url = serializers.SerializerMethodField()

    class Meta:
        model = RedirectRule
        fields = (
            'id', 'redirect_url', 'redirect_identifier',
            'is_private', 'is_active', 'created_by',
            'created', 'modified', 'click_count', 'url'
        )
        read_only_fields = (
            'id', 'redirect_identifier', 'created_by',
            'created', 'modified', 'click_count'
        )

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None

        path = 'private' if obj.is_private else 'public'
        return request.build_absolute_uri(f'/redirect/{path}/{obj.redirect_identifier}')

    def validate_redirect_url(self, value):
        """
        Validate the redirect URL
        """
        if value.startswith('javascript:'):
            raise serializers.ValidationError(
                "JavaScript URLs are not allowed"
            )
        return value

    def create(self, validated_data):
        """
        Create a new redirect rule
        """
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
