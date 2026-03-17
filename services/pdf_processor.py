from io import BytesIO

import PyPDF2


def extraer_texto_pdf(archivo_pdf):
    try:
        archivo_pdf.seek(0)
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        texto_completo = ""

        for numero_pagina, pagina in enumerate(pdf_reader.pages, start=1):
            texto_pagina = pagina.extract_text()
            if texto_pagina and texto_pagina.strip():
                texto_completo += f"\n--- PÁGINA {numero_pagina} ---\n"
                texto_completo += texto_pagina.strip() + "\n"

        texto_completo = texto_completo.strip()

        if not texto_completo:
            return "Error: El PDF parece estar vacío o contener solo imágenes."

        return texto_completo

    except Exception as e:
        return f"Error al procesar el archivo PDF: {str(e)}"