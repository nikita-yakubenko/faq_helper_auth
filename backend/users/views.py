from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User, Organization, Knowledgedb, QnARelation, Answer, Question
from users.serializers import RegisterSerializer, OrganizationSerializer, KnowledgedbSerializer, QnARealtionSerializer, AnswerSerializer, QuestionSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class OrganizationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(owner=self.request.user.id)

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        serializer = self.serializer_class(self.get_queryset())
        return Response(serializer.data)

    @swagger_auto_schema(request_body=OrganizationSerializer, responses={200: OrganizationSerializer})
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(request_body=OrganizationSerializer, responses={200: OrganizationSerializer})
    def update(self, request, pk=None):
        org = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(org, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    @swagger_auto_schema(request_body=OrganizationSerializer, responses={200: OrganizationSerializer})
    def partial_update(self, request, pk=None):
        org = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(org, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        org = get_object_or_404(self.get_queryset(), pk=pk)
        deleted = self.perform_destroy(org)
        return Response(status=204)

    def perform_destroy(self, instance):
        return instance.delete()


class KnowledgedbViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = KnowledgedbSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return
        return Knowledgedb.objects.filter(organization__in=self.request.user.organization_set.all())

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=KnowledgedbSerializer, responses={200: KnowledgedbSerializer})
    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        db = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(db)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=KnowledgedbSerializer, responses={200: KnowledgedbSerializer})
    def update(self, request, pk=None):
        db = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(db, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        db = get_object_or_404(self.get_queryset(), pk=pk)
        self.perform_destroy(db)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class QnARelationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QnARealtionSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return
        return QnARelation.objects.filter(knowledgedb__organization__in=self.request.user.organization_set.all())

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=QnARealtionSerializer, responses={200: QnARealtionSerializer})
    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        relation = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(relation)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=QnARealtionSerializer, responses={200: QnARealtionSerializer})
    def update(self, request, pk=None):
        relation = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(relation, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        relation = get_object_or_404(self.get_queryset(), pk=pk)
        self.perform_destroy(relation)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class AnswerViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return
        return Answer.objects.filter(qna_relation__knowledgedb__organization__in=self.request.user.organization_set.all())

    def list(self, request):
        queryset = self.get_queryset()
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AnswerSerializer, responses={200: AnswerSerializer})
    def create(self, request):
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        answer = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AnswerSerializer, responses={200: AnswerSerializer})
    def update(self, request, pk=None):
        answer = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = AnswerSerializer(answer, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        answer = get_object_or_404(self.get_queryset(), pk=pk)
        self.perform_destroy(answer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class QuestionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return
        return Question.objects.filter(qna_relation__knowledgedb__organization__in=self.request.user.organization_set.all())

    def list(self, request):
        queryset = self.get_queryset()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=QuestionSerializer, responses={200: QuestionSerializer})
    def create(self, request):
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        question = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=QuestionSerializer, responses={200: QuestionSerializer})
    def update(self, request, pk=None):
        question = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = QuestionSerializer(question, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def destroy(self, request, pk=None):
        question = get_object_or_404(self.get_queryset(), pk=pk)
        self.perform_destroy(question)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()