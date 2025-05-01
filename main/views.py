from django.contrib.sites import requests
from django.shortcuts import render
import requests

from django.conf import settings
from django.http import JsonResponse

import json

from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'index.html')


@csrf_exempt
def gpt_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("message", "")

        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "mixtral-8x7b-32768"
        }

        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        reply = res.json()["choices"][0]["message"]["content"]

        return JsonResponse({"response": reply})