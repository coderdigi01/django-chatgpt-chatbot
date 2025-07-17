# views.py
from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

from .models import Chat

def chat_view(request):
    chats = Chat.objects.order_by('-timestamp')[:10]
    if request.method == 'POST':
        user_input = request.POST.get('message')

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response.choices[0].message.content.strip()

        # Save to DB
        Chat.objects.create(user_message=user_input, bot_response=answer)

        return JsonResponse({'response': answer})

    return render(request, 'chatbot/chat.html', {'chats': chats})

