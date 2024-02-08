from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)
# Set your OpenAI API key here
def fetch_company_info():
    # Use GPT to fetch company info
    data = "\"date_generale\":{\"Numar mediu de salariati: 25 , cui\":19,\"data\":\"2023-08-23\",\"denumire\":\"BUCUR OBOR S.A.\",\"adresa\":\"MUNICIPIULBUCUREŞTI,SECTOR2,SOS.COLENTINA,NR.2\",\"nrRegCom\":\"J40/365/1991\",\"telefon\":\"0212525934\",\"fax\":\"0212528371\",\"codPostal\":\"21172\",\"act\":\"\",\"stare_inregistrare\":\"INREGISTRATdindata09.02.1991\",\"data_inregistrare\":\"1992-12-10\",\"cod_CAEN\":\"4719\"den_caen\":\"Comert cu amanuntul in magazine nespecializate, cu vanzare predominanta de produse nealimentare iban\":\"\",\"statusRO_e_Factura\":true,\"organFiscalCompetent\":\"AdministraţiaSector2aFinanţelorPublice\",\"forma_de_proprietate\":\"PROPR.PRIVATA-CAPITALPRIVATAUTOHTON\",\"forma_organizare\":\"PERSOANAJURIDICA\",\"forma_juridica\":\"SOCIETATECOMERCIALĂPEACŢIUNI\"},"
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Dupa numarul de angajati creaza departamente necesare pentru firma dupa domeniul de activitate de la den_caen. afiseaza departamentele in json: (Exemplu ""departamente\":\"nume\", \"nume\", \"nume\") Numar mediu de salariati: 25. \"den_caen\": \"Comert cu amanuntul in magazine nespecializate, cu vanzare predominanta de produse nealimentare; la final afiseaza doar json",
            }
        ],
        model="gpt-4-0125-preview",
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

fetch_company_info()