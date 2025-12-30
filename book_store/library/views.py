from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import filters
from .utils.custom_pagination import CustomPageNumberPagination
from django.db.models import Q

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



class BookListAPIView(APIView):
    pagination_class = CustomPageNumberPagination

    def get(self, request):
        qs = Book.objects.select_related("author").filter(is_archived=False)

        if author := request.query_params.get("author"):
            qs = qs.filter(author__name__icontains=author)

        if search := request.query_params.get("search"):
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(author__name__icontains=search)
            )

        ordering = request.query_params.get("ordering", "-created_at")
        if ordering in ["published_date", "-published_date", "created_at", "-created_at"]:
            qs = qs.order_by(ordering)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        return paginator.get_paginated_response(
            BookSerializer(page, many=True).data
        )

class AuthorListView(ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
    
        return Author.objects.all().prefetch_related('book_set')