from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin
from .methods import get_standings, get_upcomming
from .models import GameHead, GameDetail, Igrisce
from .forms import GameHeadForm, GameDetailInlineFormSet
from .tables import StandingsTable, GameTable, IgrisceTable, GameHeadTable
from .fliters import GameHeadFilter
import datetime
from crispy_forms.layout import Layout, Fieldset, Field, Div, ButtonHolder, Submit, HTML, Row, Column
from crispy_forms.bootstrap import InlineRadios, UneditableField
#from .custom_layout_object import Formset


'''
def manage_gamedetail(request, head_id):

    if id:
        game_head = GameHead.objects.get(pk=head_id)
    else:
        game_head = GameHead()
    
    gamehead_form = GameHeadForm(instance=game_head)

    formset = GameDetailInlineFormSet(instance=game_head)

    if request.method == "POST":
        gamehead_form = GameHeadForm(request.POST)

        if id:
            gamehead_form = GameHeadForm(request.POST, instance=game_head)
        
        formset = GameDetailInlineFormSet(request.POST,request.FILES)

        if gamehead_form.is_valid():
            created_gamehead = gamehead_form.save(commit=False)
            formset = GameDetailInlineFormSet(request.POST, request.FILES, instance=created_gamehead)

            if formset.is_valid():
                created_gamehead.save()
                formset.save()
                return HttpResponseRedirect(created_gamehead.get_absolute_url)
    
    return render(request, "atttp/chall2.html", {
        "gamehead_form": gamehead_form,
        "formset": formset
    })
'''
#################################################################################
#################################################################################
#################################################################################
#################################################################################

'''
TODO:
- on player click, redirect to personal page
- formhelper
'''
class StandingsFilteredTableView(FilterView, SingleTableView):

    def get_table_data(self):
        data = super(StandingsFilteredTableView, self).get_table_data()
        return data if self.object_list is None else self.object_list

    '''
    Fets
    '''
    def get_context_data(self, **kwargs):
        context = super(StandingsFilteredTableView, self).get_context_data(**kwargs)

        if self.request.GET and self.request.GET['season'] and self.request.GET['club']:
            standings = get_standings(self.request.GET['season'], self.request.GET['club'])
        else:
            initial_group = Group.objects.filter(user=self.request.user).first()
            if initial_group:
                standings = get_standings(datetime.datetime.now().year, initial_group.id)
            else:
                standings = get_standings(datetime.datetime.now().year)

        context.update({"standings_table": StandingsTable(standings, template_name="django_tables2/semantic.html")})

        if self.request.GET and self.request.GET['club']:
            upcomming_games = get_upcomming(self.request.GET['club'])
        else:
            upcomming_games = get_upcomming()
        context.update({"upcomming_games": upcomming_games})
        return context

class StandingsTableView(LoginRequiredMixin, StandingsFilteredTableView):
    model = GameHead
    table_class = GameTable
    template_name = 'atttp/season_stats.html'
    filterset_class = GameHeadFilter

##########################################################
#  GameCreate View
##########################################################

class GameCreate(CreateView):
    model = GameHead
    template_name = 'atttp/game_create.html'
    form_class = GameHeadForm
    success_url = None

    # Sending user object to the form, to verify which fields to display/remove (depending on group)
    def get_form_kwargs(self):
        kwargs = super(GameCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):

        with transaction.atomic():
            self.object = form.save()
            if self.object:
                for i in range(3):
                    detail = GameDetail(igra_id=self.object.pk, niz=(i+1))
                    detail.save()

        return super(GameCreate, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('atttp:game_detail', kwargs={'pk': self.object.pk})

##########################################################
#  GameUpdate View
##########################################################
def game_update(request, pk):
    gamehead = GameHead.objects.get(pk=pk)

    #table = GameHeadTable(GameHead.objects.filter(pk=pk))

    if request.method == "POST":
        formset = GameDetailInlineFormSet(request.POST, instance=gamehead)
        if formset.is_valid():
            formset.save()

            return HttpResponseRedirect(reverse_lazy('atttp:game_detail', kwargs={'pk': pk}))
    
    else:
        formset = GameDetailInlineFormSet(instance=gamehead)
    
    return render(request, 'atttp/game_update.html', 
        {'gamehead': gamehead,
         'details': formset,
         })


'''
TODO:
- do not give user an option to select 'niz'. Make it disabled and just enter scores
'''
class GameUpdateView(UpdateView):
    model = GameHead
    form_class = GameHeadForm
    template_name = 'atttp/game_update.html'

    def get_context_data(self, **kwargs):
        data = super(GameUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['details'] = GameDetailInlineFormSet(self.request.POST, instance=self.object)
        else:
            data['details'] = GameDetailInlineFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        #TODO: Check if niz already 
        context = self.get_context_data(form=form)
        details = context['details']

        with transaction.atomic():
            self.object = form.save()
            if details.is_valid():
                details.instance = self.object
                details.save()

        
        return super(GameUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('atttp:game_detail', kwargs={'pk': self.object.pk})

##########################################################
#  GameDelete View
##########################################################

class GameDelete(DeleteView):
    model = GameHead
    template_name = 'atttp/confirm_delete.html'
    success_url = reverse_lazy('game:home')

##########################################################
#  Igrisce View
##########################################################

class IgrisceDetail(LoginRequiredMixin, SingleTableView):
    model = Igrisce
    table_class = IgrisceTable
    template_name = 'atttp/court_detail.html'

##########################################################
#  AJAX Requests
##########################################################

def get_users_by_group(request):
    club = request.GET.get('club', None)

    users_qs = User.objects.filter(groups__name__in=[club])
    user_list = list(users_qs.values('id', 'first_name'))

    return JsonResponse(user_list, safe=False)