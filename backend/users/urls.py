from django.urls import path

from users.views import RegisterView, OrganizationViewSet, KnowledgedbViewSet, QnARelationViewSet, AnswerViewSet, QuestionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('organizations', OrganizationViewSet, basename='organization')
router.register('knowledgedbs', KnowledgedbViewSet, basename='knowledgedb')
router.register('qnarelations', QnARelationViewSet, basename='qnarelation')
router.register('answers', AnswerViewSet, basename='answer')
router.register('questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='user_register'),
]
urlpatterns += router.urls