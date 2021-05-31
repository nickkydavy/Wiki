from random import Random
from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util

markdown = Markdown()
random = Random()

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
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        titleError = ""
        contentError = ""
        if title in util.list_entries():
                titleError = "This entry is already exists."
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
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")
    return render(request, "encyclopedia/add.html")

def editEntry(request):
    if request.method == "GET":
        title = request.GET.get("title")
        if title:
            if title in util.list_entries():
                content = util.get_entry(title)
                return render(request, "encyclopedia/edit.html", {
                    "title": title,
                    "content": content
                })
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            util.save_entry(title, content)
            return HttpResponseRedirect(f"wiki/{title}")

def randomEntry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(f"wiki/{title}")