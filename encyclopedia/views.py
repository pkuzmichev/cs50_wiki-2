from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from . import util

class NewArticleForm(forms.Form):
    title = forms.CharField(label='title')
    description = forms.CharField(widget=forms.Textarea(), label='desc')
    description.widget.attrs['style'] = 'margin-top: 0px; margin-bottom: 0px; height: 100px;'

class EditArticleForm(forms.Form):
    edit_article = forms.CharField(widget=forms.Textarea(), label='')
    edit_article.widget.attrs['style'] = 'margin-top: 0px; margin-bottom: 0px; height: 100px;'
    edit_article.widget.attrs['label'] = '10'

def index(request):
    q = request.GET.get('q')
    if q:
        if util.get_entry(q):
            return render(request, "encyclopedia/article.html", {
                "heading": q,
                "article": util.get_entry(q)
            })
        elif util.list_search_matches(q):
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_search_matches(q)
            })
        elif util.get_entry(q) == None:
            return render(request, "encyclopedia/article.html", {
                "article": util.get_entry(q)
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def article(request, article):
    return render(request, "encyclopedia/article.html", {
        "heading": article,
        "article": util.get_entry(article)
    })

def new_page(request):
    if request.method == 'POST':
        form = NewArticleForm(request.POST)
        if form.is_valid():
            if util.save_entry(request.POST.get('title'), request.POST.get('description')):
                return HttpResponseRedirect('wiki/' + request.POST.get('title'))
            elif FileExistsError:
                return render(request, "encyclopedia/create.html", {
                    "error": "page exist"
                })
    return render(request, "encyclopedia/create.html", {
        "form": NewArticleForm()
    })

def edit(request, article):
    form = EditArticleForm()
    if request.method == 'GET':
        form.fields['edit_article'].initial = util.get_entry(article)
        return render(request, "encyclopedia/edit.html", {
            "form_edit": form,
            "article": article
        })
    if request.method == 'POST':
        util.update(article, request.POST.get('edit_article'))
        return render(request, "encyclopedia/article.html", {
            "heading": article,
            "article": util.get_entry(article),
            "edit": 'edit'
        })

def random(request):
    article = util.random()
    return render(request, "encyclopedia/article.html", {
        "heading": article,
        "article": util.get_entry(article),
        "edit": 'edit'
    })
