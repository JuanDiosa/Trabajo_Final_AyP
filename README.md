# Trabajo_Final_AyP

![REGIPRO](https://github.com/JuanDiosa/Trabajo_Final_AyP/blob/c20201435f4ed296c3eefe9141a305ba67b3891d/AyP/_a6202790-ec4f-4c3b-a003-40656dd2559e.jpg)


# Programa académico:
Ingeniería Industrial Presencial

# Integrantes: 

- Juan Esteban Diosa 
- Maria Isabel Buitrago
- Juliana Hurtado

# Matriculación de Estudiantes

Este proyecto automatiza el proceso de matriculación de estudiantes utilizando datos de estudiantes y una malla curricular.

## Descripción

El código proporcionado en este repositorio realiza las siguientes acciones:

- Carga datos iniciales de estudiantes y una malla curricular desde archivos CSV. (Se añaden los links de ambos archivos para la ejecucion del script, los cuales pueden ser reemplazados)
- Para cada asignatura genera un codigo único de 6 caracteres los cuales son una combinación compuesta por las tres primeras letras de la asignatura en mayúscula, el número del semestre, el número de créditos y un número consecutivo desde 0 para cada asignatura en un semestre que se reinicia para el semestre siguiente.
- Crea directorios para guardar asignaciones de estudiantes.
- Asigna grupos de estudiantes a las asignaturas según el tamaño especificado para los grupos.
- Guarda los detalles de la asignación en archivos CSV y Excel.
- Registra información detallada sobre cada operación en un archivo de registro.

## Dependencias

- pandas: Utilizado para la manipulación y análisis de datos.
- openpyxl: Utilizado para la escritura de archivos Excel.

## Instrucciones de Uso

1. **Preparación del Entorno:**
   - Asegúrese de tener Python instalado en su sistema.
   - Instala las dependencias necesarias utilizando pip:
     ```
     pip install pandas
     pip install openpyxl
     ```

2. **Ejecución del Código:**
   - Ejecuta el script `Regipro.py` para iniciar el proceso de matriculación.
   - Ajusta los parámetros según sea necesario en el script principal.

3. **Verificación de Resultados:**
   - Verifica la generación de archivos de asignación en el directorio especificado.

## Importante:
Recomendamos hacer la ejecución en Visual Studio Code, ya que fue donde hicimos las pruebas del código y garantizamos su compatibilidad y funcionamiento óptimo en este entorno de desarrollo.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).
