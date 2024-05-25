# Trabajo_Final_AyP
# Matriculación de Estudiantes

Este proyecto automatiza el proceso de matriculación de estudiantes utilizando datos de estudiantes y una malla curricular.

## Descripción

El código proporcionado en este repositorio realiza las siguientes acciones:

- Carga datos iniciales de estudiantes y una malla curricular desde archivos CSV.
- Genera códigos de asignatura y calcula horas de trabajo docente e independiente.
- Crea directorios para guardar asignaciones de estudiantes.
- Asigna grupos de estudiantes a asignaturas según el tamaño especificado.
- Guarda los detalles de la asignación en archivos CSV y Excel.
- Registra información detallada sobre cada operación en un archivo de registro.

## Dependencias

- pandas: Utilizado para la manipulación y análisis de datos.
- openpyxl: Utilizado para la escritura de archivos Excel.

## Instrucciones de Uso

1. **Preparación del Entorno:**
   - Asegúrate de tener Python instalado en tu sistema.
   - Instala las dependencias necesarias utilizando pip:
     ```
     pip install pandas openpyxl
     ```

2. **Ejecución del Código:**
   - Ejecuta el script `matriculacion.py` para iniciar el proceso de matriculación.
   - Ajusta los parámetros según sea necesario en el script principal.

3. **Verificación de Resultados:**
   - Verifica la generación de archivos de asignación en el directorio especificado.

## Estructura del Proyecto

- `matriculacion.py`: El script principal que realiza la matriculación de estudiantes.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).
