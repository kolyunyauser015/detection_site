from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import LoginUserForm, RegisterUserForm, ImageFeedForm, ProfileUserForm, UserPasswordChangeForm
from .models import ImageFeed
from .utils import process_image


def home_page(request):
    return render(request, 'object_detection/home.html')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'object_detection/login.html'

    def get_success_url(self):
        return reverse_lazy('object_detection:dashboard')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('object_detection:login')
    template_name = 'object_detection/register.html'


@login_required
def dashboard(request):
    image_feeds = ImageFeed.objects.filter(user=request.user)
    return render(request,
                  'object_detection/dashboard.html',
                  {'image_feeds': image_feeds}
                  )


@login_required
def add_image_feed(request):
    if request.method == 'POST':
        form = ImageFeedForm(request.POST, request.FILES)
        if form.is_valid():
            image_feed = form.save(commit=False)
            image_feed.user = request.user
            image_feed.save()
            return redirect('object_detection:dashboard')
    else:
        form = ImageFeedForm()
    return render(request,
                  'object_detection/add_image_feed.html',
                  {'form': form})


@login_required
def process_image_feed(request, feed_id):
    get_object_or_404(ImageFeed, id=feed_id, user=request.user)
    process_image(feed_id)
    return redirect('object_detection:dashboard')


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ImageFeed, id=image_id, user=request.user)
    image.delete()
    return redirect('object_detection:dashboard')


@login_required
def logout_user(request):
    logout(request)
    return render(request, 'object_detection/home.html')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'object_detection/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('object_detection:dashboard')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("object_detection:password_change_done")
    template_name = "object_detection/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}
