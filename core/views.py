from django.shortcuts           import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.template.loader     import render_to_string
from django.utils.http          import urlsafe_base64_encode
from django.utils.encoding      import force_bytes
from django.core.mail           import EmailMultiAlternatives
from django.conf                import settings
from .forms                     import SignUpForm
from django.utils.http          import urlsafe_base64_decode
from django.utils.encoding      import force_str
from django.contrib             import messages
def home(request):
    context = {'page_title': 'Welcome to Travel Buddy'}
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # 1) Create user but don’t activate yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # 2) Build activation link
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token  = default_token_generator.make_token(user)
            protocol = 'https' if request.is_secure() else 'http'
            domain   = request.get_host()
            link = f"{protocol}://{domain}/accounts/activate/{uidb64}/{token}/"

            # 3) Render email templates
            ctx = { 'user': user, 'activation_link': link }
            subject      = 'Confirm your Travel Buddy account'
            from_email   = settings.DEFAULT_FROM_EMAIL
            to           = [user.email]
            text_content = render_to_string('emails/activation_email.txt', ctx)
            html_content = render_to_string('emails/activation_email.html', ctx)

            # 4) Send multipart email
            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)

            # 5) Show a “check your inbox” page
            return render(request, 'registration/activation_sent.html')

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def about(request):
    context = {'page_title': 'About Travel Buddy'}
    return render(request, 'about.html', context)

def activate(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')

