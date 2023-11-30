from django.contrib import admin

from users.models import Organization, Knowledgedb, QnARelation, Answer, Question, User

admin.site.register(Organization)
admin.site.register(Knowledgedb)
admin.site.register(QnARelation)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(User)
