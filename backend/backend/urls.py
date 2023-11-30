from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Faq-helper API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# =================================================================================================
# Настройки версий client urls 

urlpatterns_client_v1 = [
   path('', include('users.urls')),
   path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns_client = [
   path('v1/', include(urlpatterns_client_v1)),
]

# Конец настройки версий client urls
# =================================================================================================


# =================================================================================================
# Настройки версий crosservice urls

urlpatterns_srv_v1 = [
   path('', include('users.srv_urls')),
]
urlpatterns_srv = [
   path('v1/', include(urlpatterns_srv_v1)),
]

# Конец настройки версий crossservice urls
# =================================================================================================


urlpatterns = [
   # Административная панель
   path('admin/', admin.site.urls),

   # Внутреннаяя документация API
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
   # Пользовательские запросы идут на api/client/v*
   path('api/client/', include(urlpatterns_client)),
   
   # Межсервисные запросы идут на api/srv/v*
   path('api/srv/', include(urlpatterns_srv)),
]