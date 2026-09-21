from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'htmx_practice/index.html')


def hello(request):
    return HttpResponse("<p class='text-success'> Hello HTMX! </p>")


def char_count(request):
    text=request.GET.get('text','')
    return HttpResponse(f"<small> Count Digit: {len(text)}</small>")


def like_button(request):
    likes=request.session.get('likes',0)
    likes+=1
    request.session['likes']=likes
    return render(request,'htmx_practice/__like.html',{'likes':likes})


def toggle(request):
    is_on=request.session.get('is_on',False)
    is_on=not is_on
    request.session['is_on']=is_on
    return render(request,'htmx_practice/_toggle.html',{'is_on':is_on})


def delete_item(request):
    if request.method == 'POST':
        return HttpResponse("")
    return render(request,'htmx_practice/_confirm_delete.html')


def search(request):
    query = request.GET.get('q', '')
    # ডেমো ডাটা
    all_items = ['রবীন্দ্রনাথ', 'শরৎচন্দ্র', 'বিভূতিভূষণ', 'সৈয়দ ওয়ালীউল্লাহ', 'মানিক বন্দ্যোপাধ্যায়']
    if query:
        items = [i for i in all_items if query in i]
    else:
        items = all_items
    return render(request, 'htmx_practice/_search_results.html', {'items': items, 'query': query})
