from langchain_groq import ChatGroq
from prompts.cv_prompts import crear_sistema_prompts
from models.cv_model import AnalisisCV

from dotenv import load_dotenv
load_dotenv()

def crear_evaluador_cv():
    modelo_base = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()

    chain_evaluadora = chat_prompt | modelo_estructurado

    return chain_evaluadora

def evaluar_cv(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
      cadena_evaluacion = crear_evaluador_cv()
      resultado = cadena_evaluacion.invoke({
        "texto_cv": texto_cv,
        "descripcion_puesto": descripcion_puesto
      })
      return resultado
    except Exception as e:
      print(f"ERROR REAL: {type(e).__name__}: {str(e)}") 
      return AnalisisCV(
        nombre_candidato="Error al evaluar CV",
        email_candidato="N/A",
        experiencia_laboral=0,
        experiencia_relevante="No se pudo extraer información relevante.",
        percentil_puesto=0.0,
        educacion="No se pudo extraer información educativa.",
        certificaciones=["Sin información de certificaciones."],
        idiomas=["No se pudo extraer información de idiomas."],
        habilidades_clave=["Sin información de habilidades."],
        fortalezas=["Sin información de fortalezas."],
        areas_mejorar=["No se pudo extraer información de áreas de mejora."],
        resumen=f"Error: {str(e)}"
      )
