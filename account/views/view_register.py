from rest_framework.views import APIView
from ..serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Invalid data',
                'error_fields': {
                    'error': serializer.errors,
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            'message': 'Register successfully',
            'data': {
                'user': serializer.data
            }
        }, status=status.HTTP_200_OK)
