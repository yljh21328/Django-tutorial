from django.shortcuts import render

from django.shortcuts import get_object_or_404
from musics.models import Music
from musics.serializers import MusicSerializer
from musics.serializers import MusicSerializerV1
from musics.models import fun_raw_sql_query
from musics.models import fun_sql_cursor_update

from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import list_route
from rest_framework.decorators import detail_route


# Create your views here.
def hello_view(request):
    musics = Music.objects.all()
    return render(request, 'hello_django.html', {
        'data': "Hello Django",
        'musics': musics
    })

def index_view(request):

    return render(request, 'index.html', {
        'content': "Home Page",
    })

class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    ## @detail_route(methods=['get'], url_path='detail_self')
    #@detail_route(methods=['get'])
    #def detail(self, request, pk=None):
    #    music = get_object_or_404(Music, pk=pk)
    #    result = {
    #        'singer': music.singer,
    #        'song': music.song
    #    }
    #    return Response(result, status=status.HTTP_200_OK)

    # /api/music/{pk}/detail/
    @detail_route(methods=['get'], url_path='detail_self')
    def detail_self(self, request, pk=None):
        music = get_object_or_404(Music, pk=pk)
        result = {
            'singer': music.singer,
            'song': music.song
        }

        return Response(result, status=status.HTTP_200_OK)

    # api/music/all_singer/
    @list_route(methods=['get'])
    def all_singer(self, request):
        music = Music.objects.values_list('singer', flat=True).distinct()
        return Response(music, status=status.HTTP_200_OK)

    # /api/music/raw_sql_query/
    @list_route(methods=['get'])
    def raw_sql_query(self, request):
        song = request.query_params.get('song', None)
        music = fun_raw_sql_query(song=song)
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # /api/music/{pk}/sql_cursor_update/
    @detail_route(methods=['put'])
    def sql_cursor_update(self, request, pk=None):
        song = request.data.get('song', None)
        if song:
            music = fun_sql_cursor_update(song=song, pk=pk)
            return Response(music, status=status.HTTP_200_OK)

    # /api/music/version_api/
    @list_route(methods=['get'])
    def version_api(self, request):
        music = Music.objects.all()
        if self.request.version == '1.0':
            serializer = MusicSerializerV1(music, many=True)
        else:
            serializer = MusicSerializer(music, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
