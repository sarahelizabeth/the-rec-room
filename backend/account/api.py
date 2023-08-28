from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm, ProfileForm
from .models import User
from .serializers import UserSerializer, UserFollowsSerializer

from notification.utils import create_notification


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'username': request.user.username,
        'email': request.user.email,
        'avatar': request.user.get_avatar(),
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'username': data.get('username'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()

        url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'

        send_mail(
            "Please verify your email",
            f"The url for activating your account is: {url}",
            "noreply@watchthisshit.com",
            [user.email],
            fail_silently=False,
        )
    else:
        message = form.errors.as_json()

    print(message)

    return JsonResponse({'message': message}, safe=False)


@api_view(['POST'])
def edit_profile(request):
    user = request.user
    username = request.data.get('username')
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    elif User.objects.exclude(id=user.id).filter(username=username).exists():
        return JsonResponse({'message': 'username already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        return JsonResponse({'message': 'information updated'})


@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)


@api_view(['GET'])
def get_users(request):
    users = User.objects.exclude(id=request.user.id).exclude(id='e39db257-5ad2-429c-9726-de724fdfe3d4')
    serializer = UserSerializer(users, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def follow(request, id):
    user = User.objects.get(pk=id)
    current_user = request.user
    followType = request.data.get('followType')
    message = 'followed'

    if followType == 'follow':
        current_user.follows.add(user)
        create_notification(request, 'new_follow', recipient_id=user.id)
    else:
        current_user.follows.remove(user)
        message = 'unfollowed'

    current_user.save()

    return JsonResponse({'message': message})


@api_view(['GET'])
def get_follows(request, id):
    user = User.objects.get(pk=id)
    current_user = request.user

    serializer_user = UserFollowsSerializer(user)
    serializer_current = UserFollowsSerializer(current_user)

    return JsonResponse({
        'profile': serializer_user.data,
        'user': serializer_current.data,
    }, safe=False)