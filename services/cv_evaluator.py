import os

from langchain_openai import ChatOpenAI

from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts


def crear_evaluador_cv():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "Falta la variable de entorno OPENAI_API_KEY. "
            "Créala en tu entorno o en un archivo .env"
        )

    modelo_base = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key,
    )

    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion


def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        cadena_evaluacion = crear_evaluador_cv()
        resultado = cadena_evaluacion.invoke(
            {
                "texto_cv": texto_cv,
                "descripcion_puesto": descripcion_puesto,
            }
        )
        return resultado

    except Exception as e:
        return AnalisisCV(
            nombre_candidato="Error en procesamiento",
            experiencia_años=0,
            habilidades_clave=["No se pudo completar el análisis"],
            education="No se pudo determinar",
            experiencia_relevante=f"Error durante el análisis: {str(e)}",
            fortalezas=["Requiere revisión manual del CV"],
            areas_mejora=[
                "Verificar la API key de OpenAI",
                "Revisar formato y legibilidad del PDF",
            ],
            porcentaje_ajuste=0,
        )