from django.contrib.sites import requests
from django.shortcuts import render




def home(request):
    return render(request, 'index.html')

GROQ_API_KEY = "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"



import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def gpt_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            headers = {
                'Authorization': f'Bearer {settings.GROQ_API_KEY}',
                'Content-Type': 'application/json',
            }
            payload = {
                "messages": [{"role": "user", "content": user_message}],
                "model": "mixtral-8x7b-32768"
            }

            res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
            res_json = res.json()

            if 'choices' in res_json and len(res_json['choices']) > 0:
                reply = res_json['choices'][0]['message']['content']
                return JsonResponse({"reply": reply})
            else:
                return JsonResponse({"error": "GPT не ответил."}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST required."}, status=400)
