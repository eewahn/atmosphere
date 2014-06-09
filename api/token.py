"""
Atmosphere service user rest api.

"""
from core.models import AtmosphereUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from threepio import logger

from atmosphere.settings import secrets
from authentication import createAuthToken


from service.accounts.eucalyptus import AccountDriver
from api.permissions import InMaintenance, ApiAuthRequired
from api.serializers import ProfileSerializer
from core.models.provider import Provider

class TokenEmulate(APIView):
    """
    This API allows already-authenticated users
    to request a new token that will emulate a user that is not their own.
    Due to the obvious security concerns, only 'staff' accounts or tokens
    owned by an administrator will be allowed.
    """
    permission_classes = (ApiAuthRequired,)

    def get(self, request, username):
        """
        Create a new token in the database on behalf of 'username'
        Returns success 201 Created - Body is JSON and contains
        """
        params = request.DATA
        user = request.user
        if user.username is not 'admin' and not user.is_superuser:
            logger.error("URGENT! User: %s is attempting to emulate a user!"
                         % user.username)
            return Response('Only admin and superusers can emulate accounts. '
                            'This offense has been reported',
                            status=status.HTTP_401_UNAUTHORIZED)
        if not AtmosphereUser.objects.filter(username=username):
            return Response("Username %s does not exist as an AtmosphereUser"
                            % username, status=status.HTTP_404_NOT_FOUND)

        #User is authenticated, username exists. Make a token for them.
        token = createAuthToken(username)
        expireTime = token.issuedTime + secrets.TOKEN_EXPIRY_TIME
        auth_json = {
            'token': token.key,
            'username': token.user.username,
            'expires': expireTime.strftime("%b %d, %Y %H:%M:%S")
        }
        return Response(auth_json, status=status.HTTP_201_CREATED)
