import streamlit as st
from models.cv_model import AnalisisCV
from services.pdf_processor import ReadPDF
from services.cv_evaluator import evaluar_cv
from services.save_pdf import generar_pdf_analisis

logo = "assets/logo.png"
def main():
    """Función principal que define la interfaz de usuario de Streamlit"""
    
    st.set_page_config(
        page_title="Sistema de Evaluación de CVs",
        page_icon="🤖",
        layout="wide", # Opciones: "centered", "wide" // "wide" para aprovechar todo el ancho de la pantalla
        initial_sidebar_state="expanded" # Opciones: "auto", "expanded", "collapsed"
    )
    
    st.title("🤖 Sistema de Evaluación de CVs con IA")
    st.markdown("""
    **Analiza currículums y evalúa candidatos de manera objetiva usando IA**
    
    Este sistema utiliza inteligencia artificial para:
    - Extraer información clave de currículums en PDF
    - Analizar la experiencia y habilidades del candidato
    - Evaluar el ajuste al puesto específico
    - Proporcionar recomendaciones objetivas de contratación
    """)
    
    st.divider() # Línea divisoria para separar secciones
    
    col_entrada, col_resultado = st.columns([1, 1], gap="large") 
    # Dos columnas iguales con espacio entre ellas
    # col_entrada: Área para subir el CV y describir el puesto
    # col_resultado: Área para mostrar los resultados del análisis

    # gap="large" para un espacio amplio entre columnas
    # gap="medium" para un espacio moderado
    # gap="small" para un espacio reducido

    with col_entrada:
        procesar_entrada()
    
    with col_resultado:
        mostrar_area_resultados()

def procesar_entrada():
    """Maneja la entrada de datos del usuario"""
    
    st.header("📋 Datos de Entrada")
    
    # Subir el archivo PDF del CV
    archivo_cv = st.file_uploader( 
        "**1. Sube el CV del candidato (PDF)**",
        type=['pdf'],
        help="Selecciona un archivo PDF que contenga el currículum a evaluar. Asegúrate de que el texto sea legible y no esté en formato de imagen."
    )
    
    if archivo_cv is not None:
        st.success(f"✅ Archivo cargado: {archivo_cv.name}")
        st.info(f"📊 Tamaño: {archivo_cv.size:,} bytes")
    
    st.markdown("---")
    
    st.markdown("**2. Descripción del puesto de trabajo**")
    # El área de texto para la descripción del puesto es más grande para permitir detalles extensos
    descripcion_puesto = st.text_area(
        "Detalla los requisitos, responsabilidades y habilidades necesarias:",
        height=250,
        placeholder="""Ejemplo detallado:

          **Puesto:** Desarrollador Frontend Senior

          **Requisitos obligatorios:**
          - 3+ años de experiencia en desarrollo frontend
          - Dominio de React.js y JavaScript/TypeScript
          - Experiencia con HTML5, CSS3 y frameworks CSS (Bootstrap, Tailwind)
          - Conocimiento de herramientas de build (Webpack, Vite)

          **Requisitos deseables:**
          - Experiencia con Next.js o similares
          - Conocimientos de testing (Jest, Cypress)
          - Familiaridad con metodologías ágiles
          - Inglés intermedio-avanzado

          **Responsabilidades:**
          - Desarrollo de interfaces de usuario responsivas
          - Colaboración con equipos de diseño y backend
          - Optimización de rendimiento de aplicaciones web
          - Mantenimiento de código legacy""",
        help="Sé específico sobre requisitos técnicos, experiencia requerida y responsabilidades del puesto."
    )# help para mostrar un mensaje de ayuda al usuario al pasar el mouse sobre el área de texto
              
    st.markdown("---")
    
    # Botones para analizar o limpiar la entrada
    col_btn1, col_btn2 = st.columns([1, 1])
    
    # boton "Analizar Candidato"
    with col_btn1:
        analizar = st.button(
            "🔍 Analizar Candidato", 
            type="primary",# type="primary" para resaltar el botón como acción principal
            use_container_width=True # use_container_width=True para que el botón ocupe todo el ancho de la columna
        )
    
    # boton "Limpiar"
    with col_btn2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.rerun()
    
    # session_state para almacenar los datos de entrada y el estado del análisis
    st.session_state['archivo_cv'] = archivo_cv
    st.session_state['descripcion_puesto'] = descripcion_puesto
    st.session_state['analizar'] = analizar

def mostrar_area_resultados():
    """Muestra el área de resultados del análisis"""
    
    st.header("📊 Resultado del Análisis")
    
    # si se ha hecho clic en el botón de analizar, procesar el análisis
    if st.session_state.get('analizar', False):
        archivo_cv = st.session_state.get('archivo_cv')
        descripcion_puesto = st.session_state.get('descripcion_puesto', '').strip()
        
        # Comprobar si hay un cv cargado
        if archivo_cv is None:
            st.error("⚠️ Por favor sube un archivo PDF con el currículum")
            return

        # Comprobar si se a proporcionado una descripcion del puesto   
        if not descripcion_puesto:
            st.error("⚠️ Por favor proporciona una descripción detallada del puesto")
            return
        
        # Si todo está correcto, procesar el análisis del CV
        procesar_analisis(archivo_cv, descripcion_puesto)
    else:
        # st.info permiten mostrar un mensaje informativo al usuario con formato Markdown
        st.info("""
        👆 **Instrucciones:**
        
        1. Sube un CV en formato PDF en la columna izquierda
        2. Describe detalladamente el puesto de trabajo
        3. Haz clic en "Analizar Candidato"
        4. Aquí aparecerá el análisis completo del candidato
        
        **Consejos para mejores resultados:**
        - Usa CVs con texto seleccionable (no imágenes escaneadas)
        - Sé específico en la descripción del puesto
        - Incluye tanto requisitos obligatorios como deseables
        """)

def procesar_analisis(archivo_cv, descripcion_puesto):
    """Procesa el análisis completo del CV"""
    
    # Mostrar spinner y barra de proceso
    with st.spinner("🔄 Procesando currículum..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📄 Extrayendo texto del PDF...")
        progress_bar.progress(25)
        
        # Extraer texto del CV
        texto_cv = ReadPDF(archivo_cv)
        
        if texto_cv.startswith("Error"):
            st.error(f"❌ {texto_cv}")
            return
        
        status_text.text("🤖 Preparando análisis con IA...")
        progress_bar.progress(50)
        
        status_text.text("📊 Analizando candidato...")
        progress_bar.progress(75)
        
        resultado = evaluar_cv(texto_cv, descripcion_puesto)
        
        status_text.text("✅ Análisis completado")
        progress_bar.progress(100)
        
        # Limpiar el área de progreso y estado antes de mostrar los resultados
        # .empty() para limpiar el contenido de los elementos de Streamlit
        progress_bar.empty()
        status_text.empty()
        
        # Mostrar los resultados del análisis de manera estructurada y profesional
        mostrar_resultados(resultado)

def mostrar_resultados(resultado: AnalisisCV):
    """Muestra los resultados del análisis de manera estructurada y profesional"""
    
    # Título y resumen del resultado
    # .subheader para un título de sección más pequeño que el header principal
    st.subheader("🎯 Evaluación Principal")
    
    if resultado.percentil_puesto >= 80:
        color = "🟢"
        nivel = "EXCELENTE"
        mensaje = "Candidato altamente recomendado"
    elif resultado.percentil_puesto >= 60:
        color = "🟡"
        nivel = "BUENO"
        mensaje = "Candidato recomendado con reservas"
    elif resultado.percentil_puesto >= 40:
        color = "🟠"
        nivel = "REGULAR"
        mensaje = "Candidato requiere evaluación adicional"
    else:
        color = "🔴"
        nivel = "BAJO"
        mensaje = "Candidato no recomendado"
    
    col1, col2, col3 = st.columns([1, 2, 1])

    # Mostrar el porcentaje de ajuste al puesto con un indicador visual y un mensaje claro
    with col2:
        st.metric(
            label="Porcentaje de Ajuste al Puesto",
            value=f"{resultado.percentil_puesto}%",
            delta=f"{color} {nivel}"
        )
        st.markdown(f"**{mensaje}**")
    
    st.divider()
    
    # Titulo -> Perfil del Candidato
    st.subheader("👤 Perfil del Candidato")
    
    col1, col2 = st.columns(2)

    #columna perfil
    with col1:
        st.info(f"**👨‍💼 Nombre:** {resultado.nombre_candidato}")
        st.info(f"**📧 Email:** {resultado.email_candidato}")
        st.info(f"**⏱️ Experiencia:** {resultado.experiencia_laboral} años")
    
    #columna educacion
    with col2:
        st.info(f"**🎓 Educación:** {resultado.educacion}")
    
    # Titulo -> Experiencia relevante
    st.subheader("💼 Experiencia Relevante")
    st.info(f"📋 **Resumen de experiencia:**\n\n{resultado.experiencia_relevante}")
    
    st.divider()
    
    # Titulo -> Habilidades Técnicas Clave
    st.subheader("🛠️ Habilidades Técnicas Clave")
    if resultado.habilidades_clave:
        cols = st.columns(min(len(resultado.habilidades_clave), 4))
        # min para limitar a 4 columnas 
        # len para crear una columna por cada habilidad, pero no más de 4 para mantener la legibilidad
        for i, habilidad in enumerate(resultado.habilidades_clave):
            # Distribuir las habilidades en las columnas de manera equitativa
            # i % 4 porque de esta manera se asigna cada habilidad a una columna de forma cíclica (0, 1, 2, 3, luego vuelve a 0)
            with cols[i % 4]:
                # Mostrar cada habilidad con un ícono de éxito para resaltar su importancia
                # success para resaltar cada habilidad como un punto fuerte del candidato
                st.success(f"✅ {habilidad}")
    else:
        st.warning("No se identificaron habilidades técnicas específicas")
    
    st.divider()
    
    col_fortalezas, col_mejoras = st.columns(2)
    # columna de fortalezas
    with col_fortalezas:
        st.subheader("💪 Fortalezas Principales")
        if resultado.fortalezas:
            for i, fortaleza in enumerate(resultado.fortalezas, 1):
                st.markdown(f"**{i}.** {fortaleza}")
        else:
            st.info("No se identificaron fortalezas específicas")
    # columna de mejoras
    with col_mejoras:
        st.subheader("📈 Áreas de Desarrollo")
        if resultado.areas_mejorar:
            for i, area in enumerate(resultado.areas_mejorar, 1):
                st.markdown(f"**{i}.** {area}")
        else:
            st.info("No se identificaron áreas de mejora específicas")
    
    st.divider()
    
    # Titulo -> Recomendación Final
    st.subheader("📋 Recomendación Final")
    
    if resultado.percentil_puesto >= 70:
        st.success("""
        ✅ **CANDIDATO RECOMENDADO**
        
        El perfil del candidato está bien alineado con los requisitos del puesto. 
        Se recomienda proceder con las siguientes etapas del proceso de selección.
        """)
    elif resultado.percentil_puesto >= 50:
        st.warning("""
        ⚠️ **CANDIDATO CON POTENCIAL**
        
        El candidato muestra potencial pero requiere evaluación adicional. 
        Se recomienda una entrevista técnica para validar competencias específicas.
        """)
    else:
        st.error("""
        ❌ **CANDIDATO NO RECOMENDADO**
        
        El perfil no se alinea suficientemente con los requisitos del puesto. 
        Se recomienda continuar la búsqueda de candidatos más adecuados.
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      pdf_bytes = generar_pdf_analisis(resultado)
      st.download_button(
        label="💾 Guardar Análisis",
        data=pdf_bytes,
        file_name=f"analisis_{resultado.nombre_candidato.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
