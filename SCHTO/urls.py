"""
URL configuration for SCHTO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from SCHTO import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
app_name = 'SCHTO'
urlpatterns = [
    path('', views.index, name='home'),
    path('adminold/', admin.site.urls),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('t&c/', views.tc, name='tc'),
    path('r&c/', views.rc, name='rc'),
    path('sendmail/', views.sendmail, name='sendmail'),
    path('store-payment-data', views.payment_store, name='store-payment-data'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', login_required(views.show_blog_list), name='admin_home'),
    path('blogs/',views.blog_index , name='blog'),
    path('blog/<int:id>/', views.blog_single, name='blog_detail'),

    path('admin/blogs/', views.show_blog_list, name='blogs'),
    path('admin/blogs/create/', views.blog_show_create, name='blogs_create'),
    # URL for editing an existing blog (id is optional)
    path('admin/blogs/create/<int:id>/', views.blog_show_create, name='blogs_create_with_id'),
    path('admin/blogs/delete/<int:id>/', views.blog_delete, name='blogs_delete'),
    path('admin/blogs/edit/<int:id>/', views.blog_show_edit, name='blogs_edit'),
    path('admin/blogs/status/<int:id>/', views.blog_activate_deactivate, name='blogs_status'),

    path('admin/boards/', views.show_board_list, name='boards'),
    path('admin/boards/create/', views.board_show_create, name='boards_create'),
    path('admin/boards/create/<int:id>', views.board_show_create, name='boards_create_with_id'),
    path('admin/boards/delete/<int:id>/', views.board_delete, name='boards_delete'),
    path('admin/boards/edit/<int:id>/', views.board_show_edit, name='boards_edit'),

    path('admin/sponsors/', views.show_sponsor_list, name='sponsors'),
    path('admin/sponsors/create/', views.sponsor_show_create, name='sponsors_create'),
    path('admin/sponsors/create/<int:id>', views.sponsor_show_create, name='sponsors_create_with_id'),
    path('admin/sponsors/delete/<int:id>/', views.sponsors_delete, name='sponsors_delete'),
    path('admin/sponsors/edit/<int:id>/', views.sponsor_show_edit, name='sponsors_edit'),

    path('admin/testimonials/', views.show_testimonial_list, name='testimonials'),
    path('admin/testimonials/create/', views.testimonial_show_create, name='testimonials_create'),
    path('admin/testimonials/create/<int:id>', views.testimonial_show_create, name='testimonials_create_with_id'),
    path('admin/testimonials/delete/<int:id>/', views.testimonial_delete, name='testimonials_delete'),
    path('admin/testimonials/edit/<int:id>/', views.testimonial_show_edit, name='testimonials_edit'),

    # path('login/', LoginView.as_view(), name='login'),
    # path('post-login/', PostLoginView.as_view(), name='login_post'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]

