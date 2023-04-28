from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from .models import Url
from .forms import UrlForm
from .utils import Shortener


def index(request):
    form = UrlForm(request.POST)
    token = ""
    if request.method == "POST":
        print("######## New post request ########")
        if form.is_valid():
            print("asdasdasd", form.cleaned_data)
            long_url = form.cleaned_data.get("url")
            token = Shortener().generate_token()
            url = Url(url=long_url, short_url=token)
            url.save()
        else:
            print("form is not valid")
    context = {
        "form": form,
        "token": token
    }
    return render(request, "index.html", context)


def redirect_to(request, token):
    url = Url.objects.get(short_url=token)
    url.click_count += 1
    url.save()
    return HttpResponseRedirect(url.url)

def get(request, token):
    try:
        url = Url.objects.get(short_url=token)
        data = {"short_url": token, "long_url": url.url, "click_count": str(url.click_count),
                "created_at": url.created_at.strftime("%Y-%m-%d %H:%M:%S")}
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)})


def create(request, long_url):
    try:
        data = {}
        token = Shortener().generate_token()
        url = Url(url=long_url, short_url=token)
        url.save()
        data["token"] = token
        data["short_url"] = "http://{}/{}".format(request.get_host(), token)
        data["long_url"] = url.url
        data["click_count"] = str(url.click_count)
        data["created_at"] = url.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": str(e)})
