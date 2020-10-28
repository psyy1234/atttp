import itertools
import django_tables2 as tables
from .models import GameHead, GameDetail, Igrisce
from .methods import get_concat, get_niz_data

#table style template
template = "django_tables2/semantic.html"

'''
class GameDetailTable(tables.Table):
    #linkify to game_detail (from urls.py)
    counter = tables.TemplateColumn("{{ row_counter }}", verbose_name="Igra", linkify=('atttp:game_detail', {'pk': tables.A('igra__pk')}))
    datum = tables.DateTimeColumn(format="d/m/Y H:i", accessor="igra.datum", linkify=('atttp:game_detail', {'pk': tables.A('igra__pk')}))
    igrisce = tables.Column(accessor="igra.igrisce")
    igralca = tables.Column(accessor='players_string', verbose_name='Igralca')
    niz = tables.Column()
    rezultat = tables.Column(accessor='score_string', verbose_name='Rezultat')
    
    class Meta:
        model = GameDetail
        template_name = template
        fields = ['counter', 'datum', 'igrisce', 'igralca', 'niz', 'rezultat']
'''

class IgrisceTable(tables.Table):
    naziv = tables.Column(verbose_name="Naziv")
    telefon = tables.Column(verbose_name="Tel.")

    class Meta:
        model = Igrisce
        template_name = template
        fields = ['naziv', 'telefon']
        attrs = {"class": "table table-hover",
                "style": "white-space:nowrap"}

class GameHeadTable(tables.Table):
    datum = tables.DateTimeColumn(verbose_name="Datum")
    igrisce = tables.Column(verbose_name="Igrišče")
    igralca = tables.Column(accessor='players_string2', verbose_name='Igralca', orderable=False)

    class Meta:
        model = GameHead
        template_name = template
        fields = ['datum', 'igrisce']
        attrs = {"class": "table table-hover",
                "style": "white-space:nowrap"}


class StandingsTable(tables.Table):
    first_name = tables.Column(verbose_name="Ime", orderable=False)
    points = tables.Column(verbose_name="Točke", orderable=False, attrs={"td": {"class": "font-weight-bold text-center"}, "th": {"class": "text-center"}})
    nr_games = tables.Column(verbose_name="Št. iger", orderable=False, attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
    wins = tables.Column(verbose_name="Zmag", orderable=False, attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
    ties = tables.Column(verbose_name="Izenačenj", orderable=False, attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
    loss = tables.Column(verbose_name="Izgub", orderable=False, attrs={"td": {"class": "text-center"}, "th": {"class": "text-center"}})
    

    class Meta:
        template_name = template
        attrs = {"class": "table table-hover",
                "style": "white-space:nowrap"}

class GameTable(tables.Table):
    counter = tables.Column(empty_values=(), verbose_name="#", linkify=('atttp:game_detail', {'pk': tables.A('pk')}))
    datum = tables.DateTimeColumn(format="d/m/Y", verbose_name='Datum')
    igralca = tables.Column(accessor='players_string2', verbose_name='Igralca')
    niz_1 = tables.Column(verbose_name='1. niz', accessor='gamehead')
    niz_2 = tables.Column(verbose_name='2. niz', accessor='gamehead')
    niz_3 = tables.Column(verbose_name='3. niz', accessor='gamehead')
    igrisce = tables.Column(accessor="igrisce", verbose_name='Igrišče')

    #initialize row counter
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_by=('datum', )
        self.orderable = False
        self.counter = itertools.count()
        next(self.counter) #start with 1
    
    def render_counter(self):
        return "%d" % next(self.counter)

    #render game sets into columns from GameDetail
    def render_niz_1(self, value, record):
        return get_niz_data(record.id, 1)
    
    def render_niz_2(self, value, record):
        return get_niz_data(record.id, 2)
    
    def render_niz_3(self, value, record):
        return get_niz_data(record.id, 3)

    class Meta:
        model = GameHead
        template_name = template
        fields = ['counter',
                'datum',
                'igralca',
                'niz_1',
                'niz_2',
                'niz_3',
                'igrisce']
        attrs = {"class": "table table-hover",
                "style": "white-space:nowrap"}