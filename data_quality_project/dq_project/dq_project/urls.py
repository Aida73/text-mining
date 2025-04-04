"""dq_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from dq_app import views
from prediction import views as predict_views

schema_view = get_schema_view(
    openapi.Info(
        title="Text Mining api",
        default_version='v1',
        description="Ceci montre l'ensemble des endpoints disponible pour notre projet",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sowaida@ept.sn"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/correction', views.DatasetCorrectionView.as_view()),
    path('api/categorization', views.DatasetCategorizationView.as_view()),
    path('api/model', predict_views.PredictionProfession.as_view()),
    path('', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
