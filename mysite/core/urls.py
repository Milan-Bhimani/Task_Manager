# from django.urls import path
# from . import views
# from . import api_views
# from rest_framework.authtoken.views import obtain_auth_token

# # Define URL patterns for the core app
# urlpatterns = [
#     path('',views.home),
#     path('hello/<str:name>/',views.hello),
#     path('add_person/',views.add_person),
#     path("edit-person/<int:id>/", views.edit_person, name="edit_person"),
#     path('delete-person/<int:id>/',views.delete_person,name='delete_person'),
#     path('signup/',views.signup,name='signup'),
#     path('login/',views.signin,name='signin'),
#     path('api/people/', api_views.PersonListAPI.as_view(), name='person_list_api'),
#     path('api/people/<int:id>/', api_views.PersonDetailAPI.as_view(), name='person_detail_api'),        
#     path('api/login/',obtain_auth_token, name= 'api_token_auth'),
# ]

from django.urls import path,include
from . import views
from .api_views import PersonViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'api/people', PersonViewSet, basename='person')

urlpatterns = [
    path('', views.home),
    path('hello/<str:name>/', views.hello),
    path('add_person/', views.add_person),
    path("edit-person/<int:id>/", views.edit_person, name="edit_person"),
    path('delete-person/<int:id>/', views.delete_person, name='delete_person'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='signin'),
    path('', include(router.urls)),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
]
