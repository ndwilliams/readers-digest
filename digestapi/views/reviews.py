from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from digestapi.models import BookReview, Book

class BookReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review
        return self.context['request'].user == obj.user

    class Meta:
        model = BookReview
        fields = ['id', 'book', 'user', 'rating', 'comment', 'date', 'is_owner']
        read_only_fields = ['user']

class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        # Get all reviews
        reviews = BookReview.objects.all()
       
        # Serialize the objects, and pass request to determine owner
        serializer = BookReviewSerializer(reviews, many=True, context={'request': request})

        # Return the serialized data with 200 status code
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            # Get the requested review
            review = BookReview.objects.get(pk=pk)
            # Serialize the object (make sure to pass the request as context)
            serializer = BookReviewSerializer(review, context={'request': request})
            # return the review with 200 status code 
            return Response(serializer.data, status=status.HTTP_200_OK)

        except BookReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Create a new instance of a review and assign property
        # values from the request payload using `request.data`

        chosen_book = Book.objects.get(pk=request.data['book'])

        rating = request.data.get('rating')
        comment = request.data.get('comment')

        review = BookReview.objects.create(
            user=request.user,
            book=chosen_book,
            rating=rating,
            comment=comment
        )
        # Save the review
        review.save()
        try:
            # Serialize the objects, and pass request as context
            serializer = BookReviewSerializer(review, context={'request': request})
            # Return the serialized data with 201 status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        try:
            # Get the requested review
            review = BookReview.objects.get(pk=pk)

            # Check if the user has permission to delete
            # Will return 403 if authenticated user is not author
            if review.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            # Delete the review
            review.delete()

            # Return success but no body
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except BookReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)