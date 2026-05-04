import PyPDF2
from io import BytesIO

def ReadPDF(f):
  """Función para leer un archivo PDF y extraer su texto.
  Args: f : Archivo PDF a leer.
  Returns: str: Texto extraído del PDF.
  """
  try:
    pdf_reader = PyPDF2.PdfReader(BytesIO(f.read()))
    full_text = ""
    for n, page in enumerate(pdf_reader.pages, 1):
      texto_pagina = page.extract_text()
      if texto_pagina.strip():  
        full_text += f"\n\n--- Página {n} ---\n\n"  
        full_text += texto_pagina.strip() + "\n"

    full_text = full_text.strip()

    if not full_text:
      return "No se pudo extraer texto del PDF."

    return full_text


  except Exception as e:
    print(f"Error al leer el PDF: {str(e)}")
    return ""
