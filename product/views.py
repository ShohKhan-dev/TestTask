from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer, UserRegistrationSerializer
from django.views import View
from product.documents import ProductDocument


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user_id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        if query:
            products = ProductDocument.search().query("multi_match", query=query, fields=['title', 'description'])
            results = products.to_queryset()
        else:
            results = Product.objects.none()

        serializer = ProductSerializer(results, many=True)
        return Response(serializer.data)