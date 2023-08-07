from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Book, User
from .serializers import BookSerializer, UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

class BookListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    
    def get(self, request):
        user_id = request.META.get('HTTP_USER_ID')
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        user_id = request.META.get('HTTP_USER_ID')
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request):
        user_id = request.META.get('HTTP_USER_ID')

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, book_id):
        user_id = request.META.get('HTTP_USER_ID')
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrowBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id, *args, **kwargs):
        user_id = request.META.get('HTTP_USER_ID')
        book = get_object_or_404(Book, pk=book_id)

        if book.status == 'BORROWED':
            return Response({'message': 'Book is already borrowed.'}, status=status.HTTP_400_BAD_REQUEST)

        book.status = 'BORROWED'
        book.save()

        return Response({'message': 'Book successfully borrowed.'}, status=status.HTTP_200_OK)

class ReturnBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id, *args, **kwargs):
        user_id = request.META.get('HTTP_USER_ID')
        book = get_object_or_404(Book, pk=book_id)

        if book.status == 'AVAILABLE':
            return Response({'message': 'Book is already available.'}, status=status.HTTP_400_BAD_REQUEST)

        book.status = 'AVAILABLE'
        book.save()

        return Response({'message': 'Book successfully returned.'}, status=status.HTTP_200_OK)
    
class MemberDetailUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, member_id):
        user_id = request.META.get('HTTP_USER_ID')
        member = get_object_or_404(Member, pk=member_id)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteUser(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, *args, **kwargs):
        user_id = request.META.get('HTTP_USER_ID')
        user = get_object_or_404(User, pk=user_id)

        if user != request.user:
            return Response({'message': 'You do not have permission to delete this user.'}, status=status.HTTP_403_FORBIDDEN)

        user.delete()

        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class SignUp(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        password = make_password(data['password'])

        user = User.objects.create(
            username=data['username'],
            password=password,
            role=data['role']
        )
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

class SignIn(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print('Received data:', data)
        user = User.objects.filter(username=data['username']).first()

        if user and check_password(data['password'], user.password):
            print('User found and password matched')
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            role = user.role
            user_id = user.id
            print('Access Token:', access_token)  # Print the access token
            print('User Role:', role)
            print('User Id:', user_id)
            return Response({'access_token': access_token, 'role': role, 'user_id': user_id}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
