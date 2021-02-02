from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .models import Post
from itertools import chain
from .models import Profile
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import pandas as pd

def Home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/postlist/')
    else:
        return render(request, 'Home.html')



@login_required
def ProfileListView(request):
    profiles =Profile.objects.all()
    posts = Post.objects.all()
    me = Profile.objects.get(user=request.user)
    context = {
        'u': me,
        'profiles':profiles,
        'posts':posts
    }

    return render(request, 'Postlist.html', context)

@method_decorator(login_required, name='dispatch')
class CreatePost(CreateView):
    model = Post
    fields = ['title', 'overview','thumbnail',]
    template_name = 'createpost.html'
    success_url = '/postlist/'
    context_object_name = 'form'

    def form_valid(self, form):
        user = Profile.objects.get(user=self.request.user)
        form.instance.Author = user
        return super(CreatePost, self).form_valid(form)



@login_required
def Visualization(request):
    countryNameSe = request.POST.get('country')
    Corona_update = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        encoding='utf-8', na_values=None)
    last_column = Corona_update[Corona_update.columns[-1]]
    totalcase = last_column.sum()
    CountryAndNumber = Corona_update[['Country/Region', Corona_update.columns[-1]]].groupby('Country/Region').sum()

    CountryAndNumber = CountryAndNumber.reset_index()
    CountryAndNumber.columns = ['Country/Region', 'cases']
    CountryAndNumber = CountryAndNumber.sort_values(by='cases', ascending=False)
    countryName = CountryAndNumber['Country/Region'].values.tolist()
    countryCase = CountryAndNumber['cases'].values.tolist()

    countryDataSpe = pd.DataFrame(Corona_update[Corona_update['Country/Region'] == countryNameSe][
                                      Corona_update.columns[4:-1]].sum()).reset_index()

    countryDataSpe.columns = ['Country/Region', 'values']
    countryDataSpe['logVal'] = countryDataSpe['values'].shift(1).fillna(0)
    countryDataSpe['incrementVal'] = countryDataSpe['values'] - countryDataSpe['logVal']
    countryDataSpe['rollingMean'] = countryDataSpe['incrementVal'].rolling(window=4).mean()
    showMap = 'false'
    axisvalues = countryDataSpe.index.tolist()
    countryDataSpe = countryDataSpe.fillna(0)
    y = countryDataSpe['values'].values.tolist()

    datasetsForLine = [
        {'label': 'Daily Cumulated Data', 'data': countryDataSpe['values'].values.tolist(), 'borderColor': 'red',
         'backgroundColor': 'red', 'fill': 'false'},
        {'label': 'Rolling Mean 4 days', 'data': countryDataSpe['rollingMean'].values.tolist(), 'borderColor': 'blue',
         'backgroundColor': 'blue', 'fill': 'false'}

    ]

    context = {
        'totalcase': totalcase,
        'Name': countryName,
        'Case': countryCase,
        'showMap': showMap,
        'datasetsForLine': datasetsForLine,
        'countryName': countryNameSe,
        'axisvalues': axisvalues,
        'y': y

    }
    return render(request, 'visualization.html', context)


@login_required
def Myprofile(request):
    me = Profile.objects.get(user=request.user)
    context = {
        'u': me,

    }

    return render(request, 'profile.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileList(ListView):
    model = Profile
    template_name = 'people.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'userprofile.html'
    context_object_name = 'profiles'

@login_required
def search(request):
    searchfor = request.GET.get('find')
    posts = Post.objects.filter(
        Q(title__icontains = searchfor) |
        Q(overview__icontains = searchfor) |
        Q(Author__user__username__icontains = searchfor)

        ).distinct()
    contex = {
    'posts':posts,
    'title':f'Searching result for {searchfor}'
    }
    return render(request,'search.html',contex)


