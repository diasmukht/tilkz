from django.contrib.sites import requests
from django.shortcuts import render

from django.conf import settings
from django.http import JsonResponse

import json
def home(request):
    return render(request, 'index.html')

def gpt_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            print("GROQ RAW RESPONSE:", response.text)
            response.raise_for_status()

            gpt_reply = response.json()['choices'][0]['message']['content']
            return JsonResponse({'response': gpt_reply})

        except Exception as e:
            print("GROQ API ERROR:", e)
            return JsonResponse({'error': 'GPT processing error'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)