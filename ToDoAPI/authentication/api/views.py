from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        """
        Custom ObtainAuthToken that returns more information about the user.

        :param request:
            {
                'username': str,
                'password': str
            }
        :return:
            {
                'token': str,
                'user_id': int,
                'email': str
            }
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.username
        })