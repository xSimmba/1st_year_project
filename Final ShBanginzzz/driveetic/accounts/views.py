from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView,FormView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required, user_passes_test

from updownfunks.models import File

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm


class index_view(TemplateView):
    template_name = 'index.html'


class SignupView(FormView):
    template_name="auth/signup.html"
    form_class=UserCreationForm
    redirect_authenticated_user = True

    def post(self, request: HttpRequest, *args: str, **kwargs: reverse_lazy) -> HttpResponse: # type: ignore 'reverse_lazy'
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            if request.user.is_staff:
                return redirect('admin/')
            
            if request.user.is_authenticated:
                return redirect('cdashboard')


        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return redirect('/admin')        
        
            return redirect('cdashboard')
    
                
        return super(SignupView,self).get(request, *args, **kwargs)


def login(request):
    template_name = "auth/login.html"

    if request.method == "POST":
   
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if request.user.is_staff:
                
                return redirect(reverse('admin:index'))
            if request.user.is_authenticated:
                
                return redirect('cdashboard')
            
    return render(request, template_name)
   
    
def logout_view(request):
    logout(request)
    return redirect('login')





@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard_view(request):
    files = File.objects.all()
    return render(request, 'staff_dashboard.html', {'files': files})

@login_required
@user_passes_test(lambda u: u.is_staff)
def file_detail_view(request, pk):
    file = File.objects.get(pk=pk)
    return render(request, 'file_detail.html', {'file': file})

@login_required
@user_passes_test(lambda u: u.is_staff)
def file_delete_view(request, pk):
    file = File.objects.get(pk=pk)
    file.delete()
    return redirect('staff_dashboard.html')