from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from.import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.Login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('content/', views.content, name="content"),
    path('content_detail/<int:id>/', views.content_detail, name='content_detail'),
    path('legal/<int:law_id>/', views.legal_case_scenario, name='legal_case_scenario'),
    path('user/', views.user, name="user"),
    path('user/update/', views.update_Profile, name='update_Profile'),
    path('about/', views.about_us, name='about_us'),
     path('quizzes/<int:id>/', views.quizzes, name='quizzes'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)