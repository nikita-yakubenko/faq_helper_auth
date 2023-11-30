from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User, Organization, Knowledgedb, QnARelation, Answer, Question


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']


class KnowledgedbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knowledgedb
        exclude = ('is_active', )

    def validate_organization(self, value):
        if value in self.context['request'].user.organization_set.all():
            return value
        raise serializers.ValidationError(f"Доступ к организации id={value.id} запрещен!")


class QnARealtionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnARelation
        fields = '__all__'

    def validate_knowledgedb(self, value):
        if value in Knowledgedb.objects.filter(organization__in=self.context['request'].user.organization_set.all()):
            return value
        raise serializers.ValidationError(f"Доступ к базе знаний id={value.id} запрещен!")


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def validate_qna_relation(self, value):
        if value in QnARelation.objects.filter(knowledgedb__organization__in=self.context['request'].user.organization_set.all()):
            return value
        raise serializers.ValidationError(f"Доступ к связке id={value.id} запрещен!")


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def validate_qna_relation(self, value):
        if value in QnARelation.objects.filter(knowledgedb__organization__in=self.context['request'].user.organization_set.all()):
            return value
        raise serializers.ValidationError(f"Доступ к связке id={value.id} запрещен!")