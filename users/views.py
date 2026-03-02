from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def register(request):
    phone = request.GET.get('phone', '')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm(initial={'phone': phone})

    return render(request, 'users/register.html', {'form': form})


@login_required
def panel_home(request):
    if request.user.is_nutritionist:
        return redirect('/admin/')
    return redirect('home')
