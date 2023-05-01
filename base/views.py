from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Hackathon, Submissions
from . serializers import UserSerializer, HackathonSerializer, SubmissionSerializer

# Create your views here.


@api_view(['GET'])
@permission_classes((AllowAny, ))
def Routes(request):
    routes = [
        'GET 127.0.0.1:8000/api/',
        'All OPERATIONS',
        '/register/ : Register a User',
        '/login/ : Get the jwt token for authentication and authorization purposes',
        '/user/ : View the authenticated User profile',
        '/hack/ : Create a Hackathon by the authenticated User by giving all the necessary details. ',
        '/hack/list/ : Listing of hackathons can be viewed by the authenticated user',
        '/hack/<int:hackathon_id>/register/ : Register for the hackathon mentioned in the URL id by the authenticated user',
        '/hack/<int: hackathon_id>/submissions/ : Make Submissions to the hackathon mentioned in the URL only if the authenticated user has registered for the respective hackathon.',
        '/hack/enrolled/: Authenticated Users are be able to list the hackathons they are enrolled to',
        'hack/<int: hackathon_id>/submissionsview/ : Authenticated Users are be able to view their submissions in the hackathon they were enrolled in.'

    ]
    return Response(routes)


class RegisterUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    # Add this line to allow unauthenticated requests
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully. Now perform Login to get your token",
        })


class UserView(APIView):
    def get(self, request):
        responseData = {
            'name': request.user.name,
            'email': request.user.email,

        }
        return JsonResponse(responseData)


class CreateHackathonView(APIView):
    def post(self, request):
        serializer = HackathonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListHackathonsView(generics.ListAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer


class RegisterHackathonView(generics.GenericAPIView):
    serializer_class = HackathonSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        hackathon = get_object_or_404(Hackathon, pk=pk)
        request.user.hackathons.add(hackathon)
        response = {

            "Hackathon": HackathonSerializer(hackathon, context=self.get_serializer_context()).data,
            "Message": "Registation done successfully",

        }
        return JsonResponse(response)


class SubmissionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Submissions.objects.filter(hackathon_id=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        # Retrieve the current user and hackathon object
        user = self.request.user
        hackathon = Hackathon.objects.get(pk=self.kwargs.get('pk'))

        # Check if the user is registered for the hackathon
        if user not in hackathon.participants.all():
            raise PermissionDenied(
                detail='You must be registered for this hackathon to submit a response.')

        # hackathon = Hackathon.objects.get(pk=self.kwargs.get('pk'))
        submission_type = serializer.validated_data['submission_type']

        # Check if the user has already submitted a submission of this type
        user = self.request.user
        if Submissions.objects.filter(hackathon=hackathon, user=user, submission_type=submission_type).exists():
            raise serializers.ValidationError(
                f'You have already submitted a {submission_type} for this hackathon.')

        serializer.save(hackathon=hackathon, user=user)


class EnrolledHackathonsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        hackathons = user.enrolled_hackathons()
        serializer = HackathonSerializer(hackathons, many=True)
        return Response(serializer.data)


class UserSubmissionsListAPIView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        hackathon_id = self.kwargs.get('hackathon_id')
        return Submissions.objects.filter(hackathon_id=hackathon_id, user=user)


# class LogoutView(APIView):
#     def post(self,request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             "message": 'Logout success'
#         }
#         return response

# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def revoke_token(request):
#     token = request.data.get('token')
#     if token:
#         # Remove the token from the blacklist or set its expiration time to 0
#         # Return a success response
#         return Response({'message': 'Token revoked successfully'})
#     else:
#         return Response({'error': 'Token is required'})
