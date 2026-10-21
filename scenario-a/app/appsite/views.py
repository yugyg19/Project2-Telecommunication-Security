from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST


@require_GET
def health(request):
    return JsonResponse({
        "service": "project2-django",
        "status": "ok",
        "project": "Telecommunication Security",
    })


@require_GET
def api_status(request):
    return JsonResponse({
        "service": "project2-django",
        "status": "ok",
        "network": "5G",
        "project": "Telecommunication Security",
    })


@require_GET
def home(request):
    return render(request, "appsite/home.html")


@login_required
@require_GET
def profile(request):
    return HttpResponse(
        f"<h1>Profile</h1><p>Welcome, {request.user.username}.</p>"
        '<p><a href="/">Home</a></p>'
    )


@login_required
def feedback(request):
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if not message:
            return HttpResponse("Feedback message is required.", status=400)
        return HttpResponse("Feedback submitted successfully.", status=200)

    return render(request, "appsite/feedback.html")
@require_GET
def search(request):
    query = request.GET.get("q", "").strip()

    return JsonResponse({
        "service": "project2-django",
        "endpoint": "search",
        "query": query,
        "status": "ok",
    })
