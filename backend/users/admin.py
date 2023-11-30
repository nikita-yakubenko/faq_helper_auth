from django.contrib import admin

from users.models import Organization, Knowledgedb, QnARelation, Answer, Question

admin.site.register(Organization)
admin.site.register(Knowledgedb)
admin.site.register(QnARelation)
admin.site.register(Answer)
admin.site.register(Question)
