from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util

markdown = Markdown()

class searchEntry(forms.Form):
    q = forms.CharField(label="q")



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchEntry()
    })

def showEntry(request, title):
    return render(request, "encyclopedia/entry.html",{
        "content": markdown.convert(util.get_entry(title))
    })

def searchForm(request):
    if request.method == "POST":
        word = request.POST.get("q")
        if word:
            entries = util.list_entries()
            if word in entries:
                return HttpResponseRedirect(f"/wiki/{word}")

            foundEntry = [x for x in entries if word in x]
            if foundEntry:
                return render(request, "encyclopedia/search.html", {
                    "word": word,
                    "foundWord": True,
                    "entries": foundEntry
            })

            return render(request, "encyclopedia/search.html", {
                "word": word,
                "foundWord": False
            })