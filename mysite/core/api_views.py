# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Person
# from .serializers import PersonSerializer
# from rest_framework import status
# from rest_framework.views import APIView

# class PersonListAPI(APIView):
#     def get(self, request):
#         people = Person.objects.all()
#         serializer = PersonSerializer(people, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PersonSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PersonDetailAPI(APIView):
#     def get_object(self, id):
#         try:
#             return Person.objects.get(id=id)
#         except Person.DoesNotExist:
#             return None

#     def get(self, request, id):
#         person = self.get_object(id)
#         if person is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = PersonSerializer(person)
#         return Response(serializer.data)

#     def put(self, request, id):
#         person = self.get_object(id)
#         if person is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = PersonSerializer(person, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         person = self.get_object(id)
#         if person is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         person.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics
from .models import Person
from .serializers import PersonSerializer
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
    
class PersonListAPI(generics.ListCreateAPIView):
    queryset = Person.objects.select_related('team','profile').prefetch_related('skills').all()
    serializer_class = PersonSerializer
    filterset_fields = ['team__name','age']
    search_fields = ['name','skills__name']

class PersonDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.select_related('team','profile').prefetch_related('skills').all()
    serializer_class = PersonSerializer
    lookup_field = 'id'
