from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.session.get("complete_profile"):
                if request.path != reverse("complete_profile"):
                    return redirect("complete_profile")

        return response
