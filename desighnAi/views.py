import os
from dotenv import load_dotenv
from django.shortcuts import render
import openai
import requests
from PIL import Image
from io import BytesIO

load_dotenv()

def get_text_input(prompt):
    return input(prompt)

def create_prompt(company_domain, most_used_product, favorite_season, color_theme1, color_theme2, color_theme3, target_audience, key_words, place_of_activity, product_description):
    return f"Create an artistic image that captures the essence of {company_domain}, prominently featuring {most_used_product}. The color scheme should blend {color_theme1}, {color_theme2}, and {color_theme3}, drawing inspiration from the {favorite_season} season. The image should cater to {target_audience}, incorporating {key_words} that resonate with this demographic. Set the scene in {place_of_activity}, ensuring it complements the product and the overall theme. The depiction of {most_used_product} should align with {product_description}, showcasing its unique qualities and appeal. The composition should be harmonious and engaging, encapsulating the brand's ethos and the lifestyle of the {favorite_season}, while appealing directly to the {target_audience}. Remember, the focus is on visual storytelling, so avoid including text in the image."



# Create your views here.
def ai_view(request):
    context = {"data": "data"}
    
    if request.method == 'POST':
        company_domain =  request.POST.get("company_domain", "")
        most_used_product =  request.POST.get("most_used_product", "")
        favorite_season =  request.POST.get("favorite_season", "")
        color_theme1 =  request.POST.get("color_theme1", "")
        color_theme2 =  request.POST.get("color_theme2", "")
        color_theme3 =  request.POST.get("color_theme3", "")
        target_audience =  request.POST.get("target_audience", "")
        key_words =  request.POST.get("key_words", "")
        place_of_activity =  request.POST.get("place_of_activity", "")
        product_description =  request.POST.get("product_description", "")

        context["company_domain"] = company_domain
        context["most_used_product"] = most_used_product
        context["favorite_season"] = favorite_season
        context["color_theme1"] = color_theme1
        context["color_theme2"] = color_theme2
        context["color_theme3"] = color_theme3
        context["target_audience"] = target_audience
        context["key_words"] = key_words
        context["place_of_activity"] = place_of_activity
        context["product_description"] = product_description
    
        client = openai.OpenAI(
            # This is the default and can be omitted
            api_key = os.environ["API_KEY"]  # Get the API key from the environment variable

        )
        prompt = create_prompt(company_domain, most_used_product, favorite_season, color_theme1, color_theme2, color_theme3, target_audience, key_words, place_of_activity, product_description)
        response = client.images.generate(prompt=prompt, size="1024x1024")
        
        response = client.images.generate(prompt=prompt, size="1024x1024")
        print((response.data[0].url))
        context["image"] = (response.data[0].url)
        
    else:
        print("get")
    
    return render(request, "desighn-ai.html", context)
