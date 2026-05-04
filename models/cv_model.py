from pydantic import BaseModel, Field

class AnalisisCV(BaseModel):
  """Modelo de datos para representar el análisis de un CV de un candidato para un cargo específico."""

  nombre_candidato: str = Field(..., description="Nombre del candidato extraido del cv.")
  email_candidato: str = Field(..., description="Correo electrónico del candidato extraido del cv.")

  experiencia_laboral: int = Field(..., description=f"Años de experiencia laboral relevante para el cargo.")
  experiencia_relevante: str = Field(..., description=f"Resumen breve de la experiencia laboral más relevante para el cargo.")

  percentil_puesto: float = Field(..., description=f"Porcentaje de ajuste al puesto (0-100) basado en la experiencia, habilidades, formacion.", ge=0, le=100)

  educacion: str = Field(..., description=f"Nivel educativo mas alto alcanzado por el candidato y especialidad.")
  certificaciones: list[str] = Field(..., description=f"Listado de certificaciones relevantes para el cargo, junto con la institución que las otorgó.")
  idiomas: list[str] = Field(..., description=f"Listado de idiomas que el candidato domina, junto con su nivel de competencia (básico, intermedio, avanzado).")
  
  habilidades_clave: list[str] = Field(..., description=f"Listado de 5 o 7 habilidades relevantes para el cargo.")
  fortalezas: list[str] = Field(..., description=f"Listado de 5 a 7 fortalezas del candidato relacionadas con el cargo con respecto a su perfil.")
  areas_mejorar: list[str] = Field(..., description=f"Listado de 5 a 7 áreas de mejora del candidato relacionadas con el cargo con respecto a su perfil.")
  
  resumen: str = Field(..., description=f"Resumen breve de las conclusiones del análisis del CV, destacando los puntos más importantes y relevantes para el cargo.")
