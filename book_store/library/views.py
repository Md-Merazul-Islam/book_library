from django.shortcuts import render
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .utils.custom_pagination import CustomPageNumberPagination


class AuthorCreateView(APIView):
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Author created",
                    "author": serializer.data
                },    
                status=201
            )
        return Response({"message": "Author not created", "errors": serializer.errors}, status=400)


class BookCreateView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Book created",
                    "book": serializer.data
                },
                status=201
            )
        return Response({"message": "Book not created", "errors": serializer.errors}, status=400)



class BookListView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author__name']
    search_fields = ['title', 'author__name']
    ordering_fields = ['published_date', 'created_at'] 
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):

        return Book.objects.select_related('author').filter(is_archived=False)


class AuthorListView(ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
    
        return Author.objects.all().prefetch_related('book_set')