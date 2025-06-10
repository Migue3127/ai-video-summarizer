import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class Model:
    @staticmethod
    def google_gemini(transcript: str, prompt: str, extra: str = "") -> str:
        try:
            genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            
            # Configuração para respostas consistentes
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048
            }
            
            response = model.generate_content(
                contents=[prompt + extra + transcript],
                generation_config=generation_config
            )
            
            return response.text if response.text else "Sem resposta válida"
            
        except Exception as e:
            error_msg = f"Erro na API Gemini: {str(e)}"
            print(error_msg)
            return error_msg