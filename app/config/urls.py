from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView

from config.schema import schema

urlpatterns = [
    path('', include('courses.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('contactus/', include('contactus.urls')),
    path('api/', include('api.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('frontend/', include('frontend.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
