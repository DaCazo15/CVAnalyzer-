from models.cv_model import AnalisisCV
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

def _estilos():
    styles = getSampleStyleSheet()
    return {
        "titulo":   ParagraphStyle('titulo',   fontSize=18, fontName='Helvetica-Bold', spaceAfter=6,  textColor=colors.HexColor('#1a1a2e')),
        "subtitulo":ParagraphStyle('subtitulo',fontSize=13, fontName='Helvetica-Bold', spaceAfter=4,  textColor=colors.HexColor('#16213e')),
        "normal":   styles['Normal']
    }

def _seccion(story, titulo, contenido, estilo_subtitulo, estilo_normal):
    story.append(Paragraph(titulo, estilo_subtitulo))
    if isinstance(contenido, list):
        for item in contenido:
            story.append(Paragraph(f"• {item}", estilo_normal))
    else:
        story.append(Paragraph(contenido, estilo_normal))
    story.append(Spacer(1, 10))

def generar_pdf_analisis(resultado: AnalisisCV) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=40, bottomMargin=40)
    estilos = _estilos()
    story = []

    story.append(Paragraph("Reporte de Evaluacion de CV", estilos["titulo"]))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 12))

    _seccion(story, "Perfil del Candidato", "\n".join([
        f"<b>Nombre:</b> {resultado.nombre_candidato}",
        f"<b>Email:</b> {resultado.email_candidato}",
        f"<b>Experiencia:</b> {resultado.experiencia_laboral} años",
        f"<b>Educacion:</b> {resultado.educacion}",
    ]), estilos["subtitulo"], estilos["normal"])

    _seccion(story, "Ajuste al Puesto",
        f"<b>Porcentaje de ajuste:</b> {resultado.percentil_puesto}%",
        estilos["subtitulo"], estilos["normal"])

    _seccion(story, "Experiencia Relevante",   resultado.experiencia_relevante, estilos["subtitulo"], estilos["normal"])
    _seccion(story, "Habilidades Clave",        resultado.habilidades_clave,    estilos["subtitulo"], estilos["normal"])
    _seccion(story, "Fortalezas",               resultado.fortalezas,           estilos["subtitulo"], estilos["normal"])
    _seccion(story, "Areas de Mejora",          resultado.areas_mejorar,        estilos["subtitulo"], estilos["normal"])
    _seccion(story, "Resumen Final",            resultado.resumen,              estilos["subtitulo"], estilos["normal"])

    doc.build(story)
    return buffer.getvalue()
