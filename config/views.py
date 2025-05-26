from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, "❌ Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

    
def cerrar_sesion(request):
    logout(request)
    messages.success(request, "🚪 Sesión cerrada correctamente.")
    return redirect('login')
