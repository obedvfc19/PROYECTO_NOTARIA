# Fine-Tuning de LLM para Asistencia Especializada

Este proyecto realiza el fine-tuning (ajuste fino) de un modelo de lenguaje pre-entrenado utilizando la técnica de QLoRA (Quantized Low-Rank Adaptation) sobre un dataset personalizado. El objetivo es especializar al modelo para que responda a instrucciones específicas con mayor precisión y estilo.

## 📂 Estructura del Proyecto

* `fine_tune.py`: Script principal para iniciar el proceso de fine-tuning. Carga el dataset, configura el modelo base y el entrenador, y guarda los "adaptadores" del modelo entrenado.
* `backend.py`: Contiene la lógica para cargar el modelo base junto con los adaptadores afinados y generar las respuestas. Separa la lógica del modelo de la interfaz de usuario.
* `main.py`: Lanza la aplicación web utilizando Gradio, proporcionando una interfaz de chat para interactuar con el modelo afinado.
* `dataset.csv`: El conjunto de datos para el entrenamiento. Debe contener las columnas necesarias para el ajuste (ej. `instruction`, `response`).

---

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos para replicar el entorno y ejecutar el proyecto.

### Prerrequisitos

* **Python 3.9+**
* Una **GPU NVIDIA con CUDA** es **altamente recomendada** para el proceso de fine-tuning.
* Conocimientos básicos de la terminal y entornos de Python.

### Pasos

1.  **Clonar el Repositorio**
    ```bash
    git clone <URL-de-tu-repositorio>
    cd <nombre-de-la-carpeta-del-repositorio>
    ```

2.  **Crear y Activar un Entorno Virtual**
    ```bash
    # Crear el entorno
    python3 -m venv venv

    # Activar en Linux / macOS / WSL
    source venv/bin/activate
    ```

3.  **Instalar Dependencias**
    Este proyecto requiere librerías específicas para PyTorch, Transformers y PEFT.
    ```bash
    pip install -r requirements.txt
    ```

---

## ⚙️ Uso del Programa

El flujo de trabajo se divide en dos etapas principales:

### Etapa 1: Fine-Tuning del Modelo

1.  **Prepara tu Dataset:** Asegúrate de que tu archivo `dataset.csv` esté en el directorio principal y tenga el formato esperado por el script `fine_tune.py`.
2.  **Ejecuta el script de Fine-Tuning:** Este proceso entrenará el modelo y puede tardar desde varios minutos hasta horas, dependiendo del tamaño del dataset y la potencia de tu GPU.
    ```bash
    python3 fine_tune.py
    ```
3.  **Verifica los Resultados:** Al finalizar, se habrá creado una nueva carpeta (ej. `./fine_tuned_model`) que contiene los adaptadores LoRA. ¡Este es el resultado de tu entrenamiento!

### Etapa 2: Ejecutar la Aplicación de Chat

Una vez que el modelo ha sido afinado, puedes interactuar con él.

1.  **Inicia la aplicación:**
    ```bash
    python3 main.py
    ```
2.  **Abre la interfaz:** La terminal te mostrará una URL local (ej. `http://12.0.0.1:7860`). Cópiala en tu navegador para empezar a chatear con tu modelo especializado.

---

### Formato del Dataset

El script `fine_tune.py` espera un archivo `dataset.csv` con un formato específico. El formato más común es:

| instruction                             | response                                   |
| --------------------------------------- | ------------------------------------------ |
| "¿Qué es el fine-tuning de un LLM?"     | "El fine-tuning es el proceso de..."       |
| "Resume el siguiente texto: [texto]"    | "El texto trata sobre..."                  |

Si tu dataset tiene columnas con nombres diferentes, deberás ajustar las referencias dentro de `fine_tune.py`.
