from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView,UpdateView
from hitcount.views import HitCountDetailView
from django.http import HttpResponseRedirect
from .forms import *
from hitcount.models import HitCount
from django.http import JsonResponse

class NewsDetailView(HitCountDetailView):
	model = News
	template_name = 'news/news.html'
	slug_field = 'slug'
	count_hit = True

class NewsListView(ListView):
    model = News
    template_name = "news/news_list.html"
    paginate_by=3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



class TagNewsListView(ListView):

    model = News
    template_name = "news/tag_news_list.html"
    form_class = TagForm



    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            tag = request.POST.get("tag","")
            self.request.session['tag'] = tag
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        all_tags = Tag.objects.all()

        tag = self.request.session.get('tag',None)
        qs = {}
        print("tag ",tag," ", type(tag))
        if tag:
        	try:
        		tag_obj = Tag.objects.get(title=tag)

		        print("tag ",tag," ", type(tag))
		        print("tag_obj ",tag_obj)
		        
		        
		        if tag_obj:
		        	print('cont '  ,context['object_list'])
		        	qs = context['object_list'].filter(tag=tag_obj)
		        	print("qs ",qs)

        	except:
        		pass

        context = super().get_context_data(**kwargs)
        context['tag']=tag
        context['t_form'] = TagForm()
        context['qs'] = qs
        context['all_tags'] = all_tags

        return context


class HitCountListView(ListView):
    model = HitCount
    template_name = "news/hitcount_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def like_dislike(request):
    user = request.user
    user_id = user.id
    #print("user.id = ",type(user.id))
    #print("user.id = ",type(user_id))
    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        #print("news_id = ",type(news_id))
        news_obj = News.objects.get(id=news_id)

        if user in news_obj.likes.all():
            news_obj.likes.remove(user_id)
        else:

            news_obj.likes.add(user_id)

        like, created = Like.objects.get_or_create(user = user,news=news_obj)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        news_obj.save()
        like.save()

        data = {
            'value':like.value,
            'likes': news_obj.likes.all().count()
        }
        return JsonResponse(data, safe=False)
    return redirect('news:news-list')