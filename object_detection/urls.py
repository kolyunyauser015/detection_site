from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views
from detection_site import settings
from django.conf.urls.static import static


app_name = 'object_detection'

urlpatterns = ([
    path('', views.home_page, name='home'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/',
         PasswordChangeDoneView.as_view(template_name="object_detection/password_change_done.html"),
         name="password_change_done"
         ),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="object_detection/password_reset_form.html",
             email_template_name="object_detection/password_reset_email.html",
             success_url=reverse_lazy("object_detection:password_reset_done")
                                   ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="object_detection/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="object_detection/password_reset_confirm.html",
             success_url=reverse_lazy("object_detection:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="object_detection/password_reset_complete.html"),
         name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-image-feed/', views.add_image_feed, name='add_image_feed'),
    path('logout/', views.logout_user, name='logout'),
    path('process/<int:feed_id>/', views.process_image_feed, name='process_feed'),
    path('image/delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
