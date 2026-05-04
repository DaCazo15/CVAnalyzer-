# CVAnalyzer 

Aplicación web para analizar currículums vitae de forma automática utilizando inteligencia artificial. Permite cargar un CV en formato PDF y obtener un análisis detallado generado por un modelo de lenguaje (LLM) a través de Groq.

---

## 🚀 Características

- 📥 Carga de CVs en formato PDF
- 🤖 Análisis inteligente con LLM mediante LangChain + Groq
- 📊 Generación de reportes en PDF con los resultados del análisis
- 🖥️ Interfaz web interactiva con Streamlit
- 🧩 Arquitectura modular (modelos, prompts, servicios, UI)

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Descripción |
|---|---|
| [Streamlit](https://streamlit.io/) | Interfaz web |
| [LangChain](https://www.langchain.com/) | Orquestación del LLM |
| [Groq](https://groq.com/) | Proveedor del modelo de lenguaje |
| [PyPDF2](https://pypdf2.readthedocs.io/) | Extracción de texto de PDFs |
| [ReportLab](https://www.reportlab.com/) | Generación de reportes en PDF |
| [Pydantic](https://docs.pydantic.dev/) | Validación de datos |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gestión de variables de entorno |

---

## 📁 Estructura del proyecto

```
Analisis-CV/
│
├── app.py                  # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
│
├── models/                 # Modelos de datos (Pydantic)
├── prompts/                # Plantillas de prompts para el LLM
├── services/               # Lógica de negocio (extracción, análisis, reporte)
└── ui/
    └── streamlit_ui.py     # Interfaz de usuario con Streamlit
```

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/DaCazo15/Analisis-CV.git
cd Analisis-CV
```

### 2. Crear y activar un entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto con tu clave de API de Groq:

```env
GROQ_API_KEY=tu_clave_api_aqui
```

> Puedes obtener tu API key en [console.groq.com](https://console.groq.com/).

---

## ▶️ Uso

```bash
streamlit run app.py
```

Abre tu navegador en `http://localhost:8501`, sube un CV en PDF y obtén el análisis generado por IA.

---

## 📦 Dependencias

```
pyPDF2
pydantic
langchain
langchain-core
langchain-groq
python-dotenv
streamlit
reportlab
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un *issue* o un *pull request* con tus sugerencias o mejoras.

---

## 📄 Licencia

Este proyecto no tiene licencia definida aún. Consulta al autor para más información.
