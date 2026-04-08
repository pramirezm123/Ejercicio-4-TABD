Sistema de Recomendación de Cursos - EPIS

Requisitos:
- Python 3.x
- chromadb

Instalación:
pip install chromadb

Ejecución:
Ejecutar el script o notebook.
La base de datos se guarda automáticamente en ./db_cursos.

Funciones:
1. Recomendar cursos según intereses
2. Buscar cursos similares
3. Buscar cursos por perfil de habilidades

Características:
- Uso de embeddings para búsqueda semántica
- Persistencia de datos con ChromaDB
- Filtros por semestre y área

Limitaciones:
- Dataset pequeño (20 cursos)
- No considera historial académico real
- Embeddings genéricos

Mejoras futuras:
- Integrar historial del alumno
- Interfaz web
- Más datos reales
