from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util

markdown = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def showEntry(request, title):
    content = markdown.convert(util.get_entry(title))
    return render(request, "encyclopedia/entry.html",{
        "title": title,
        "content": content
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

def addEntry(request):
    if request.method == "GET":
        title = "" or request.GET.get('title')
        
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        titleError = ""
        contentError = ""
        if not title or not content:
            if not title:
                titleError = "Please enter your title"
            if not content:
                contentError = "Please enter some content"
            return render(request, "encyclopedia/add.html", {
                "title" : title,
                "content" : content,
                "titleError" : titleError,
                "contentError" : contentError
            })
        else:
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/add.html", {
                    "titleError" : "This entry is already exists"
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")
    title = "" or request.GET.get('title')
    return render(request, "encyclopedia/add.html")