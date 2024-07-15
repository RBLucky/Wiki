from django.shortcuts import render
from random import choice
from . import util
from markdown2 import Markdown

markdowner = Markdown()
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdown = util.get_entry(title)

    if markdown is not None:
        html = markdowner.convert(markdown)
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "title": title
            })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown,
            "title": title
            })

def search(request):
    if request.method == "POST":
        form = request.POST['q']
        entries = util.list_entries()
        form_entry = util.get_entry(form)
        substring = form
        search_entries = []
        
        if form_entry == None:
            for entry in entries:
                if substring.lower() in entry.lower():
                    search_entries += [entry]
            
            if not search_entries:
                return render(request, "encyclopedia/noresult.html")

            else:
                return render(request, "encyclopedia/search.html", {
                        "entries": search_entries
                        })
        
        elif form is not None:
            markdown = form_entry
            html = markdowner.convert(markdown)
            return render(request, "encyclopedia/entry.html", {
                "entry": html,
                "title": form.capitalize()
            })

    else:
        return render(request, "encyclopedia/index.html")
    

def create(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        entries = util.list_entries()
        exists = util.get_entry(title)

        for i in entries:
            if exists is not None:
                return render(request, "encyclopedia/create.html", {
                    "exists": exists,
                    "title": title
                })
            
            else:
                util.save_entry(title, content)

                return entry(request, title)

    else:
        return render(request, "encyclopedia/create.html")
    

def edit(request):
    if request.method == "POST":
        return render(request, "encyclopedia/edit.html", {
            "title": request.POST['title_edit'],
            "content": util.get_entry(request.POST['title_edit'])
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        util.save_entry(title, content)

        return entry(request, title)


def random(request):
    options = util.list_entries()

    random = choice(options)

    return entry(request, random)