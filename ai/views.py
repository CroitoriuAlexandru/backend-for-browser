import os
from django.shortcuts import render
import requests


import requests

def chat_with_gpt(api_key, messages):
    url = "https://api.openai.com/v1/chat/completions"  # Updated URL
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # Replace with the correct model name
        "messages": messages                                
    }

    response = requests.post(url, headers=headers, json=data)
    return response


# Create your views here.
def ai_view(request):
    if request.method == 'POST':
        prompt = request.POST.get("prompt", "")  # Safely get the prompt
        api_key = os.environ["API_KEY"]  # Get the API key from the environment variable

        # Construct messages
        messages = [{"role": "user", "content": prompt}]

        responseFromPrompt = chat_with_gpt(api_key, messages)

        if responseFromPrompt.status_code == 200:
            ai_message = responseFromPrompt.json()['choices'][0]['message']['content']
            return render(request, 'ai1.html', {'promptResponse': ai_message})
        else:
            # Handle the error appropriately
            error_message = f"Error: {responseFromPrompt.status_code}"
            return render(request, 'ai1.html', {'promptResponse': error_message})
    else:
        return render(request, 'ai1.html', {'promptResponse': "Awaiting input..."})


# # Replace with your actual OpenAI API key
# api_key = "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"

# # Example messages
# messages = []
# while True:
#     user_message = input("You: ")
#     messages.append({"role": "user", "content": user_message})
#     response = chat_with_gpt(api_key, messages)
#     if response.status_code == 200:
#         ai_message = response.json()['choices'][0]['message']['content']
#         print("AI: " + ai_message)
#         messages.append({"role": "assistant", "content": ai_message})
#     else:
#         print("Error in API request")
#         break
