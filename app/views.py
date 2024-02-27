from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *
import json
# aba para criação de metodos = ao controler do projeto

class LivroView(APIView):
    #funções para chamar as classes, o request é do que ele está requisitando
    def get(self, request, id=''):

        if id:
            
            livros = Livros.objects.filter(id=id).first()

            if not livros:
                return Response(status=404, data={'mensagem': 'livro nao encontrado'})

            serializer = LivroSerializer(livros, many=False)
            return Response(status=200, data=serializer.data)
        else:

            livros = Livros.objects.all()
            serializer = LivroSerializer(livros, many=True)
            return Response(status=201, data=serializer.data)
        
    def post(self, request):
        #o body é o corpo da requisição
        # body = json.loads(request.body)
        #o loads ele converte bytes, strings e arrey de bytes para json (o documennto precisa estar em formato json)
        # serializer = LivroSerializer(body, many=False)
        body = request.data
        serializer = LivroSerializer(data=body, many=False)

        if not serializer.is_valid():
             return Response(status=400, data={'mensagem': 'dado ruim'})
        serializer.save()
        # print(serializer)

        return Response(status=201, data=serializer.data)
    
    def put(self, request, id):
        #verificando que o livro existe no banco de dados
        #aqui estamos tentando encontrar um livro no bancos de dados com o ID fornecido  
        livro = Livros.objects.filter(id=id).first()
        if not livro:
            #se nenhum livro for encontrado ele retornara um erro 404
            return Response(status=404, data={'mensagem': 'livro nao encontrado'})
        
        serializer = LivroSerializer(livro, data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data={'mensagem': 'dados invalidos'})
        
        serializer.save()
        return Response(status=200, data=serializer.data)
       