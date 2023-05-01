
from django.urls import path
from base import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.Routes, name='Routes'),

    path('register/', views.RegisterUser.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.UserView.as_view(), name='user-profile'),

    path('hack/', views.CreateHackathonView.as_view(), name="create"),
    path('hack/list/', views.ListHackathonsView.as_view(), name='list-hackathons'),
    path('hack/<int:pk>/register/', views.RegisterHackathonView.as_view(),
         name='register-hackathon'),
    path('hack/enrolled/', views.EnrolledHackathonsView.as_view(),
         name='enrolled_hackathons'),


    path('hack/<int:pk>/submissions/',
         views.SubmissionListCreateAPIView.as_view(), name='submission-list-create'),
    path('hack/<int:hackathon_id>/submissionsview/',
         views.UserSubmissionsListAPIView.as_view(), name='user_submissions_list'),

]
