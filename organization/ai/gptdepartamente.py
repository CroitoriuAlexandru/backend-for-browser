import os
import openai
import json
from dotenv import load_dotenv
load_dotenv()


def get_response_from_openai(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def generate_departments(caen_code, employee_count):
    # Set your OpenAI API key
    openai.api_key =  os.environ.get("OPENAI_GPT_KEY")
    caen_descr = find_description_for_caen(caen_code)
    try:
        # Prepare the conversation messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Crează o listă cu departamente specifice pentru o afacere specializată în domeniul {caen_descr}, care are {employee_count} angajați. Asigură-te că departamentele sunt direct relevante pentru acest tip de afacere și numărul de departamente nu depășește numărul de angajați. Fiecare departament ar trebui să fie unic și necesar pentru funcționarea afacerii. Formatează răspunsul ca 'departament: descriere' pentru fiecare departament, folosind diacriticele atunci când este necesar."}
        ]

        # Get response from OpenAI
        response = get_response_from_openai(messages)

        # Process the response
        lines = response.strip().split('\n')
        departments_json = []
        for line in lines:
            # print(line)
            if ':' in line:
                name, description = line.split(':', 1)
                departments_json.append({"name": name.strip(), "description": description.strip()})
            else:
                print(f"Skipping line, not in expected format: '{line}'")

        return json.dumps(departments_json, indent=4)

    except Exception as e:
        print("An error occurred:", e)
        return None

def find_description_for_caen(caen_code):
    try:
        with open("./organization/ai/file.txt", 'r') as file:
            for line in file:
                if line.strip().startswith(caen_code + " -"):
                    return line.strip().split(" - ", 1)[1]  # Splitting at " - " to get the description
        return "Unknown"  # Default if the code is not found
    except FileNotFoundError:
        print("File file.txt not found.")
        return "Unknown"




# caen_code = "19"
# employee_count = "5"
# departments_json = generate_departments(caen_code, employee_count)
# print(departments_json)

