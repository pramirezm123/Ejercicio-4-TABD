# =========================================================
# Sistema de Recomendación de Cursos - EPIS
# Autor: Paolo
# Descripción:
# Sistema que utiliza ChromaDB para recomendar cursos
# universitarios usando búsqueda semántica con persistencia.
# =========================================================

import chromadb
from chromadb.utils import embedding_functions


# =========================================================
# 1. INICIALIZACIÓN DE BASE DE DATOS PERSISTENTE
# =========================================================

client = chromadb.PersistentClient(path="./db_cursos")

embedding_function = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="cursos_epis",
    embedding_function=embedding_function
)


# =========================================================
# 2. CARGA DE DATOS (SOLO UNA VEZ)
# =========================================================

def cargar_datos():
    """
    Inserta cursos solo si la colección está vacía.
    Evita duplicados en ejecuciones futuras.
    """

    if len(collection.get()["ids"]) > 0:
        print("✅ Datos ya cargados, no se duplican.")
        return

    cursos = [
        ("Algoritmos", "Estudia estructuras de datos y algoritmos eficientes. Se analizan complejidades. Base fundamental para programación.", 4, "III", "básica", "Programación básica"),
        ("Base de Datos", "Diseño de bases de datos relacionales. Consultas SQL avanzadas. Normalización de datos.", 4, "IV", "especialidad", "Algoritmos"),
        ("Inteligencia Artificial", "Introducción a IA, aprendizaje automático. Modelos predictivos. Aplicaciones modernas.", 4, "VII", "especialidad", "Probabilidad"),
        ("Redes", "Fundamentos de redes de computadoras. Protocolos y arquitectura. Configuración básica.", 4, "VI", "especialidad", "Sistemas Operativos"),
        ("Seguridad Informática", "Protección de sistemas. Criptografía básica. Gestión de riesgos.", 3, "VIII", "especialidad", "Redes"),
        ("Programación I", "Introducción a programación. Variables, estructuras de control. Resolución de problemas.", 4, "I", "básica", "Ninguno"),
        ("Programación II", "Programación orientada a objetos. Clases y herencia. Buenas prácticas.", 4, "II", "básica", "Programación I"),
        ("Ingeniería de Software", "Metodologías de desarrollo. UML. Gestión de proyectos.", 4, "V", "especialidad", "Programación II"),
        ("Machine Learning", "Modelos supervisados y no supervisados. Evaluación de modelos. Aplicaciones reales.", 4, "VIII", "especialidad", "IA"),
        ("Minería de Datos", "Extracción de conocimiento. Análisis de datos. Técnicas estadísticas.", 4, "VII", "especialidad", "Base de Datos"),
        ("Sistemas Operativos", "Procesos, memoria y concurrencia. Administración del sistema.", 4, "IV", "básica", "Programación II"),
        ("Desarrollo Web", "Frontend y backend. HTML, CSS, JS. Aplicaciones web completas.", 3, "V", "electivo", "Programación II"),
        ("Cloud Computing", "Servicios en la nube. Virtualización. Arquitecturas distribuidas.", 3, "IX", "electivo", "Redes"),
        ("Big Data", "Procesamiento de grandes volúmenes de datos. Hadoop y Spark. Casos reales.", 3, "IX", "electivo", "Minería de Datos"),
        ("DevOps", "Integración y despliegue continuo. Automatización. Herramientas modernas.", 3, "X", "electivo", "Ingeniería de Software"),
        ("Ciberseguridad", "Ataques y defensas. Ethical hacking. Seguridad avanzada.", 4, "IX", "especialidad", "Seguridad Informática"),
        ("Visión Computacional", "Procesamiento de imágenes. Reconocimiento visual. IA aplicada.", 3, "VIII", "especialidad", "IA"),
        ("Compiladores", "Análisis léxico y sintáctico. Traducción de lenguajes. Teoría formal.", 4, "VII", "especialidad", "Algoritmos"),
        ("Matemática Discreta", "Lógica, conjuntos, grafos. Base teórica de computación.", 4, "II", "básica", "Ninguno"),
        ("Probabilidad", "Estadística y probabilidad. Modelos matemáticos. Aplicaciones.", 4, "III", "básica", "Matemática Discreta")
    ]

    documentos = [c[1] for c in cursos]

    metadatos = [{
        "nombre": c[0],
        "creditos": c[2],
        "semestre": c[3],
        "area": c[4],
        "prerequisitos": c[5]
    } for c in cursos]

    ids = [f"curso{i}" for i in range(len(cursos))]

    collection.add(documents=documentos, metadatos=metadatos, ids=ids)

    print("✅ Cursos insertados correctamente.")


# =========================================================
# 3. FUNCIONES PRINCIPALES
# =========================================================

def recomendar_cursos(intereses_alumno, semestre_actual, top_k=5):
    """
    Recomienda cursos según intereses y semestre.
    """

    resultados = collection.query(
        query_texts=[intereses_alumno],
        n_results=top_k,
        where={"semestre": semestre_actual}
    )

    print(f"\n🎯 Recomendaciones para: {intereses_alumno}")

    for i in range(len(resultados['ids'][0])):
        print(f"\nCurso: {resultados['metadatas'][0][i]['nombre']}")
        print("Similitud:", round(1 - resultados['distances'][0][i], 4))
        print("Descripción:", resultados['documents'][0][i])


def cursos_similares(nombre_curso, n=3):
    """
    Encuentra cursos similares a uno dado.
    """

    data = collection.get()

    descripcion = None
    for i, meta in enumerate(data["metadatas"]):
        if meta["nombre"].lower() == nombre_curso.lower():
            descripcion = data["documents"][i]
            break

    if descripcion is None:
        print("❌ Curso no encontrado")
        return

    resultados = collection.query(
        query_texts=[descripcion],
        n_results=n + 1
    )

    print(f"\n🔗 Cursos similares a {nombre_curso}:")

    for i in range(1, len(resultados['ids'][0])):
        print(resultados['metadatas'][0][i]['nombre'])


def buscar_por_perfil(habilidades_lista, area="especialidad"):
    """
    Busca cursos según habilidades.
    """

    query = " ".join(habilidades_lista)

    resultados = collection.query(
        query_texts=[query],
        n_results=5,
        where={"area": area}
    )

    print(f"\n🧑‍💻 Cursos para perfil: {habilidades_lista}")

    for i in range(len(resultados['ids'][0])):
        print(resultados['metadatas'][0][i]['nombre'])


# =========================================================
# 4. MENÚ INTERACTIVO
# =========================================================

def menu():
    """
    Menú principal del sistema.
    """

    while True:
        print("\n=== SISTEMA DE RECOMENDACIÓN ===")
        print("1. Recomendar cursos")
        print("2. Cursos similares")
        print("3. Buscar por perfil")
        print("4. Salir")

        op = input("Seleccione opción: ")

        if op == "1":
            intereses = input("Intereses: ")
            semestre = input("Semestre (I-X): ")
            recomendar_cursos(intereses, semestre)

        elif op == "2":
            nombre = input("Nombre del curso: ")
            cursos_similares(nombre)

        elif op == "3":
            habilidades = input("Habilidades (separadas por coma): ").split(",")
            buscar_por_perfil(habilidades)

        elif op == "4":
            print("👋 Saliendo...")
            break

        else:
            print("❌ Opción inválida")


# =========================================================
# 5. MAIN
# =========================================================

if __name__ == "__main__":
    cargar_datos()
    menu()
