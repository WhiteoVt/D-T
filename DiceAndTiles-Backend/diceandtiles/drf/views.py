from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product, Comment, Vote, Profile, Fetched_Product, OwnedProduct, Productweb  
from .serializers import UserSerializer,ProductSerializer, ProductwebSerializer, OwnedProductSerializer, CommentSerializer, VoteSerializer, Fetched_ProductSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count, Sum, F
from rest_framework.exceptions import PermissionDenied

class ProductPagination(PageNumberPagination):
    page_size = 25  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 2000

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    """
    Lista produktów
    """
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    ordering = ['id']
    http_method_names = ['head', 'get']
    lookup_field = "slug"
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Check if a custom sorting parameter is provided in the request
        sort_by = self.request.query_params.get('sort_by', None)
        name = self.request.query_params.get('name')      
        
        if sort_by == 'id_desc':
            queryset = queryset.order_by('-id')
        if sort_by == 'upvotes':
            queryset = queryset.annotate(total_upvotes=Sum('vote__value', filter=F('vote__value') == 2))
            queryset = queryset.order_by('-total_upvotes')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_context(self):
        """
        Additional context provided to the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

   
    @action(detail=False, methods=['get'])
    def sorted_by_id_desc(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-id'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sorted_by_upvotes(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-upvotes'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductwebViewSet(viewsets.ModelViewSet):
    """
    Lista produktów
    """
    
    queryset = Productweb.objects.all()
    serializer_class = ProductwebSerializer
    authentication_classes = [TokenAuthentication]
    ordering = ['id']
    http_method_names = ['head', 'get']
    lookup_field = "slug"
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Check if a custom sorting parameter is provided in the request
        sort_by = self.request.query_params.get('sort_by', None)
        name = self.request.query_params.get('name')      
        
        if sort_by == 'id_desc':
            queryset = queryset.order_by('-id')
        if sort_by == 'upvotes':
            queryset = queryset.annotate(total_upvotes=Sum('vote__value', filter=F('vote__value') == 2))
            queryset = queryset.order_by('-total_upvotes')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        queryset = queryset.filter(is_active=True)
        return queryset

    def get_serializer_context(self):
        """
        Additional context provided to the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

   
    @action(detail=False, methods=['get'])
    def sorted_by_id_desc(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-id'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sorted_by_upvotes(self, request):
        queryset = self.filter_queryset(self.get_queryset().order_by('-upvotes'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class Fetched_ProductViewSet(viewsets.ModelViewSet):
    """
    produkty fetchowane z mikroserwisu fastapi scrapper
    """
    
    queryset = Fetched_Product.objects.all()
    serializer_class =  Fetched_ProductSerializer
    http_method_names = ['head','get']
    lookup_field = "bggid"

class RegisterViewSet(viewsets.ModelViewSet):
    """
    rejestracja uzytkownikow
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'head']

class CommentViewSet(viewsets.ModelViewSet):
    """
    komentarze pod produktami
    """
    http_method_names = ['head', 'get', 'post']

    serializer_class = CommentSerializer
    authentication_class = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
       
        queryset = Comment.objects.all().order_by('-id')
        product = self.request.data.get('product') 
        owner = self.request.data.get('owner') 
        if product is not None: ##do zwracania komentarzy napisanych pod danym produktem
            queryset = queryset.filter(product=product)
        if owner is not None: ##do zwracania komentarzy napisanych tylko przez danego użytk
            queryset = queryset.filter(owner__username=owner)
        return queryset
    


class VoteViewSet(viewsets.ModelViewSet):
    """
    oddawanie glosu na gry
    """
    http_method_names = ['post']

    serializer_class = VoteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        try:
            product = Product.objects.get(pk=self.request.data.get('product'))
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'})
        
        existing_vote = Vote.objects.filter(product=product, owner=self.request.user).first()
        if existing_vote:
            # Update the existing vote
            existing_vote.value = self.request.data.get('value', 0)
            existing_vote.save()
        else:
            # Create a new vote
            Vote.objects.create(product=product, owner=self.request.user, value=self.request.data.get('value', 0))

class OwnedProductViewSet(viewsets.ModelViewSet):
    """
    lista posiadanych gier uzytkownika
    """
    http_method_names = ['get','post', 'delete', 'patch', "put"]

    serializer_class = OwnedProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'product'
    
    def perform_create(self, serializer):
        try:
            product = Product.objects.get(pk=self.request.data.get('product'))
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'})
        
        if OwnedProduct.objects.filter(product=product, owner=self.request.user).first():
            return Response({"message": " product is already on your list"})
        else:
           
            OwnedProduct.objects.create(product=product, owner=self.request.user )
    def get_queryset(self): 
        if self.request.user.is_authenticated:
            return OwnedProduct.objects.filter(owner=self.request.user)
        else:
            #  return OwnedProduct.objects.none()
             raise PermissionDenied(detail="You are not authenticated. Please send auth token in header to access user's game list.")
 #zwróć obiekty gdzie user w modelu zgadza sie z userem z requesta (wymaga tokenu)
    
   

    
   