from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from digestapi.models import Category, Book

class CategoryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']

class CategorySerializer(serializers.ModelSerializer):
    books = CategoryBookSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'books']


class CategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)