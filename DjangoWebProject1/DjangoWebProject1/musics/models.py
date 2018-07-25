from django.db import models
from collections import namedtuple

from django.db import connection

TYPE_CHOICES = (
    ('T1', 'type 1'),
    ('T2', 'type 2'),
    ('T3', 'type 3'),
    ('T4', 'type 4'),
)


# Create your models here.
class Music(models.Model):
    song = models.TextField(default="song")
    singer = models.TextField(default="AKB48")
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default="T1"
    )

    class Meta:
        db_table = "music"

    def display_type_name(self):
        return self.get_type_display()

def fun_raw_sql_query(**kwargs):
    song = kwargs.get('song')
    if song:
        result = Music.objects.raw('SELECT * FROM music WHERE song = %s', [song])
    else:
        result = Music.objects.raw('SELECT * FROM music')
    return result

def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def fun_sql_cursor_update(**kwargs):
    song = kwargs.get('song')
    pk = kwargs.get('pk')

    '''
    Note that if you want to include literal percent signs in the query, you have to double them in the case you are passing parameters:
    '''
    with connection.cursor() as cursor:
        cursor.execute("UPDATE music SET song = %s WHERE id = %s", [song, pk])
        cursor.execute("SELECT * FROM music WHERE id = %s", [pk])
        # cursor.execute("SELECT * FROM music")
        # result = cursor.fetchone()
        result = namedtuplefetchall(cursor)
    result = [
        {
            'id': r.id,
            'song': r.song,
            'singer': r.singer,
            'last_modify_date': r.last_modify_date,
            'created': r.created,
        }
        for r in result
    ]

    return result