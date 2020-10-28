import django_filters as df
from django import forms
from django.contrib.auth.models import Group, User
from .models import GameHead
import datetime
from django.db.models import Q


def get_groups(request):
    if request is None:
        return Group.objects.none()
    
    return Group.objects.filter(user=request.user)

class GameHeadFilter(df.FilterSet):
    SEASON_CHOICES = ((2019, '2019'), (2020, '2020'))
    starting_season = 2019

    #start with this year season
    initial_season = datetime.datetime.now().year

    #for year_iter in range(starting_season, datetime.datetime.now().year):
    #    SEASON_CHOICES += (year_iter, str(year_iter))

    club = df.ModelChoiceFilter(field_name='oseba_1__groups__name', label='Klub', method="filter_osebe", empty_label=None, queryset=get_groups)
    #club = df.ModelChoiceFilter(field_name='oseba_1__groups__name', lookup_expr='in', label='Klub', empty_label=None, queryset=Group.objects.all())
    season = df.ChoiceFilter(field_name='datum', lookup_expr='year', label='Sezona', choices=SEASON_CHOICES, empty_label=None, initial=initial_season)
    #df.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
    #    widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = GameHead
        fields = ['club',
                  'season']
    
    def filter_osebe(self, queryset, name, value):
        return GameHead.objects.filter(
            Q(oseba_1__groups__name__in=[value.name]) & Q(oseba_2__groups__name__in=[value.name])
        ).order_by("datum")
    
    

    # set initial 
    def __init__(self, data=None, *args, **kwargs):
        # pylint: disable=E1101
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                if name == 'season':
                    initial = f.extra.get('initial_season')
                else:
                    initial = None

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)
    
    #override queryset when querying empty string
    @property
    def qs(self):
        parent = super(GameHeadFilter, self).qs
        if self.request.GET:
            return parent
        else:
            group = Group.objects.filter(user=self.request.user).first()
            return parent.filter(datum__year=self.initial_season).filter(oseba_1__groups__id=group.id).filter(oseba_2__groups__id=group.id)