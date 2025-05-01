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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get("message")

            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15
            )
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)