from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#class based view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins
from rest_framework import viewsets

#Authentification
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
      serializer_class = PostSerializer
      queryset = Post.objects.all()


# class PostViewSet(viewsets.ViewSet):
#       def list(self, request):
#             posts = Post.objects.all() #QuerySet
#             serializer = PostSerializer(posts, many=True)
#             return Response(serializer.data)
      
#       def create(self, request):
#             serialzer = PostSerializer(data=request.data)

#             if serialzer.is_valid():
#                   serialzer.save()
#                   return Response(serialzer.data, status=status.HTTP_201_CREATED)
#             return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
      



class genericApiView(generics.GenericAPIView, mixins.ListModelMixin, 
mixins.CreateModelMixin, mixins.UpdateModelMixin,
 mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
      serializer_class = PostSerializer
      queryset = Post.objects.all()

      lookup_field = 'id'

      authentication_classes = [SessionAuthentication, BasicAuthentication]
      # authentification_classes = [TokenAuthentification]
      permission_classes = [IsAuthenticated]
      def get(self, request, id):
            if id:
                  return self.retrieve(request)
            return self.list(request)
      
      def post(self, request):
            return self.create(request)
      
      def put(self, request, id=None):
            return self.update(request, id)
      
      def delete(self, request, id=None):
            return self.destroy(request, id)


class PostsAPIView(APIView):
      
      def get(self, request):
            posts = Post.objects.all() #QuerySet
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

      def post(self,request):
            serialzer = PostSerializer(data=request.data)

            if serialzer.is_valid():
                  serialzer.save()
                  return Response(serialzer.data, status=status.HTTP_201_CREATED)
            return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
      

@api_view(['GET', 'POST'])
def PostsView(request):
      if request.method == 'GET':
            posts = Post.objects.all() #QuerySet
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)

      elif request.method == 'POST':
            serializer = PostSerializer(data=request.data)

            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class postDetailsAPIView(APIView):
    def get_object(self, id):
        try:
            return Post.objects.get(pk=id) #instance
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, id):
        post = self.get_object(id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self,request, id):
        post = self.get_object(id)
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)#

    def delete(self, request, id):
        post = self.get_object(id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def post_detail(request, id):
      try:
            post = Post.objects.get(pk=id) #Instance
      except post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
      
      if request.method == 'GET':
            serializer = PostSerializer(post)
            return Response(serializer.data)
      elif request.method == 'PUT':
            serializer = PostSerializer(post,data = request.data)

            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
      elif request.method == 'DELETE':
            post.delete()
            return Response(status=204)
