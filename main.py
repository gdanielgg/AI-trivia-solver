import os
import pyautogui
import pytesseract
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CHEIE_GROQ = os.getenv("GROQ_API_KEY")

if not CHEIE_GROQ:
    print("EROARE: Variabila GROQ_API_KEY nu a fost gasita. Verifica fisierul .env!")
    exit()

# Schimba in functie de unde vrei sa citeasca intrebarile
ZONA = (65, 322, 861, 200)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Daca textul nu contine unul din aceste cuvinte, botul il ignora.
CUVINTE_CHEIE = [
    "cine", "cum", "ce", "care", "cand", "unde", "cati", "cate", 
    "in", "din", "numeste", "anul", "tara", "orasul", 
    "personajul", "completeaza", "semnifica", "reprezinta", "?"
]

try:
    client = Groq(api_key=CHEIE_GROQ)
    print("Conectat la AI")
except Exception as e:
    print("Eroare conectare:", e)

ultimul_text = ""

while True:
    try:
        # Captura
        poza = pyautogui.screenshot(region=ZONA)
        text_brut = pytesseract.image_to_string(poza, lang='ron')
        
        text_curat = " ".join(text_brut.split())
        text_mic = text_curat.lower()

        # FILTRU
        if len(text_curat) > 10 and text_curat != ultimul_text:
            
            # Aici verificam daca exista vreun cuvant cheie in text
            este_intrebare = any(cuvant in text_mic for cuvant in CUVINTE_CHEIE)
            
            if este_intrebare:
                print(f"\n[!] INTREBARE DETECTATA: {text_curat[:50]}...") 
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Esti un expert Trivia. Primesti textul OCR.\n"
                                "1. Daca sunt variante (nume/cuvinte), alege-o pe cea corecta.\n"
                                "2. Daca e intrebare de estimare (fara variante), scrie numarul.\n"
                                "Raspunde DOAR cu rezultatul."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Intrebare: '{text_curat}'"
                        }
                    ],
                    model="llama-3.3-70b-versatile", 
                    temperature=0.0,
                    max_tokens=30
                )
                
                raspuns = chat_completion.choices[0].message.content
                print(">>> RASPUNS:", raspuns)
                print("--------------------------------")
                
                ultimul_text = text_curat
                time.sleep(2)
            else:
                pass

        time.sleep(0.1)

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Eroare:", e)
        time.sleep(1)
