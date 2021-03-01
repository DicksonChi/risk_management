from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.constants import SUCCESS_CODE, ERROR_CODE
from main.models import RiskType, Field, User
from main.serializers import UserSerializer, RiskTypeSerializer, FieldSerializer


class UserCreateView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        """Handle the posting of data."""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = {'code': SUCCESS_CODE,
                        'id': user.id,
                        'email': serializer.validated_data['email'],
                        }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            'code': ERROR_CODE,
            'errors': serializer.errors
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

    def get(self, request, *args, **kwargs):
        """Handle retrieving user."""
        res = super(UserRetrieveView, self).get(request, *args, **kwargs)
        data = res.data
        data['code'] = SUCCESS_CODE
        data['id'] = self.get_object().id
        return Response(data)


class RiskTypeRetrieveView(generics.RetrieveAPIView):
    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """Handle retrieving single risk type."""
        res = super(RiskTypeRetrieveView, self).get(request, *args, **kwargs)
        data = res.data
        data['code'] = SUCCESS_CODE
        return Response(data)


class AllRiskTypeRetrieveView(generics.ListAPIView):
    serializer_class = RiskTypeSerializer

    def list(self, request, *args, **kwargs):
        """List the list of risk type."""
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        res = {
            'code': SUCCESS_CODE,
            'risk_types': serializer.data
        }
        return Response(res)

    def get_queryset(self):
        """Queryset of all the risk type for a user."""
        user_id = self.kwargs['user_id']
        get_object_or_404(User, pk=user_id)
        return RiskType.objects.filter(user_id=user_id)


class RiskTypeView(APIView):
    serializer_class = RiskTypeSerializer

    def post(self, request):
        """Handle the posting of data."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code': SUCCESS_CODE,
                'message': 'Success'
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            'code': ERROR_CODE,
            'errors': serializer.errors
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RiskTypeRetrieveUpdateView(generics.UpdateAPIView):
    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        """Update the particular record."""
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Http404:
            response = {
                "code": ERROR_CODE,
                "errors": "not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                "code": SUCCESS_CODE,
                "status": "Updated the record"
            }

            return Response(response, status=status.HTTP_200_OK)

        response = {
            "code": ERROR_CODE,
            "errors": serializer.errors
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AllFieldRetrieveView(generics.ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def list(self, request, *args, **kwargs):
        """List of fields."""
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        res = {
            'code': SUCCESS_CODE,
            'fields': serializer.data
        }
        return Response(res)


class FieldView(APIView):
    serializer_class = FieldSerializer

    def post(self, request):
        """Handle the posting of data."""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'code': SUCCESS_CODE,
                'message': 'Success'
            }
            return Response(response, status=status.HTTP_201_CREATED)

        response = {
            'code': ERROR_CODE,
            'errors': serializer.errors
        }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
