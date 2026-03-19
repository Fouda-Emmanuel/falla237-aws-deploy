from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('about', views.about, name='about'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('found-objects', views.found_view, name='found'),
    path('lost-objects', views.lost_view, name='lost'),
    path('post-lost-objects', views.post_lost_view, name='post_lost'),
    path('post-found-objects', views.post_found_view, name='post_found'),
    path('object-detail/<int:item_id>', views.object_detail_view, name='object_detail'),
    path('update-object/<int:item_id>', views.update_object_view, name='update_object'),
    path('delete-object/<int:item_id>', views.delete_object_view, name='delete_object'),
    
]