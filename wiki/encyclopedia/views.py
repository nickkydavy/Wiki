from django.shortcuts import render
from markdown2 import Markdown
from . import util

markdown = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def showEntry(request, title):
    return render(request, "encyclopedia/entry.html",{
        "content": markdown.convert(util.get_entry(title))
    })