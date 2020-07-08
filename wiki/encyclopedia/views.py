from django.shortcuts import render
import markdown2, sys
from random import choice
from . import util
from django.shortcuts import redirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    md=markdown2.Markdown()
    res=util.get_entry(title)
    if res is None:
        return render(request,"encyclopedia/error.html",{
            "msg": "entry does not exist."
        })
    else:
        k=md.convert(res)
        return render(request,"encyclopedia/info.html",{
            "detail": k,
            "title": title
        })

def check(request):
    title=request.POST["q"]
    md=markdown2.Markdown()
    res=util.get_entry(title)
    if res is None:
        match=[x for x in util.list_entries() if title in x]
        print(match,file=sys.stdout)
        return render(request,"encyclopedia/search.html",{"entries": match})
    else:
        return redirect("/wiki/"+title)

def add(request):
    if request.method == "GET":
        return render(request,"encyclopedia/addpage.html")
    else:
        title=request.POST["title"]
        content=request.POST["content"]
        res=util.get_entry(title)
        if res is None:
            file=open('entries/'+title+'.md','w')
            file.write("# "+title+"\n")
            file.write(content)
            return redirect("/wiki/"+title)
        else:
            return render(request,"encyclopedia/error.html",{
                "msg": "Page already exists."
            })

def random(request):
    all=util.list_entries()
    c=choice(all)
    return redirect("/wiki/"+c)
