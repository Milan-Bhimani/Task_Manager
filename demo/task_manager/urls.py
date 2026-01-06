from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import ProjectViewSet, TaskViewSet, dashboard, project_detail, signup
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('project/<int:pk>/', project_detail, name='project_detail'),
    path('signup/', signup, name='signup'),
    path('api/',include(router.urls)),
    path('api/login/', obtain_auth_token, name = 'api_login'),
    path('accounts/', include('django.contrib.auth.urls')),
]
