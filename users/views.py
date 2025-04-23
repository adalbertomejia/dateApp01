from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    phone = request.GET.get('phone', '')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # o a donde quieras
    else:
        form = CustomUserCreationForm(initial={'phone': phone})

    return render(request, 'users/register.html', {'form': form})
