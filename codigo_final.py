import pandas as pd
import os
from datetime import datetime
import time
import platform
import logging

# Configuración del logging
ruta_final_dir = 'Ruta_final'
os.makedirs(ruta_final_dir, exist_ok=True)
log_path = os.path.join(ruta_final_dir, 'matriculacion.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S', handlers=[
    logging.FileHandler(log_path, encoding='utf-8'),
    logging.StreamHandler()
])

# Obtener detalles del sistema de forma robusta
user = os.getenv('USER') or os.getenv('USERNAME') or 'ColabUser'
system_info = platform.uname()
header_info = f"Usuario: {user}, Sistema operativo: {system_info.system}, Plataforma: {system_info.release}, Versión: {system_info.version}, Máquina: {system_info.machine}, Procesador: {system_info.processor}"

logging.info(header_info)

# Función para registrar el tiempo de ejecución de una operación
def log_timed_operation(operation_name, func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"{operation_name}\tTiempo: {elapsed_time:.6f} segundos")
    return result

logging.info('Cargando datos iniciales y malla curricular...')
DatosIniciales = log_timed_operation('Cargar Datos Iniciales', pd.read_csv, 'https://github.com/JuanDiosa/Trabajo_Final_AyP/raw/213a425e4ee26788abac77401237b4dd377a2ca1/AyP/Estudiantes.csv', encoding='latin1', delimiter=';')
MallaCurricular = log_timed_operation('Cargar Malla Curricular', pd.read_csv, 'https://github.com/JuanDiosa/Trabajo_Final_AyP/raw/213a425e4ee26788abac77401237b4dd377a2ca1/AyP/MallaCurricular.csv', encoding='latin1', delimiter=';')
Datos = DatosIniciales.drop(columns=['Fecha'])
logging.info('Datos cargados con éxito.')

def generar_codigo_asignatura(asignatura, semestre, creditos, consecutivo):
    codigo = f"{asignatura[:3].upper()}{semestre}{creditos}{consecutivo:01d}"
    logging.debug(f'Generado código de asignatura: {codigo}')
    return codigo

def calcular_htd(creditos):
    htd = {4: 96, 3: 64, 2: 32, 1: 16}.get(creditos, 0)
    logging.debug(f'Calculadas horas de trabajo docente (HTD) para {creditos} créditos: {htd}')
    return htd

def calcular_hti(creditos):
    hti = {4: 120, 3: 80, 2: 64, 1: 32}.get(creditos, 0)
    logging.debug(f'Calculadas horas de trabajo independiente (HTI) para {creditos} créditos: {hti}')
    return hti

def crear_directorio_si_no_existe(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        logging.info(f'Directorio creado: {ruta}')
    else:
        logging.info(f'Directorio ya existe: {ruta}')

def guardar_asignaciones(grupo_df, grupo_path, grupo_excel_path):
    grupo_df.to_csv(grupo_path, index=False, encoding='latin1')
    grupo_df.to_excel(grupo_excel_path, index=False)
    logging.info(f'Archivos guardados: {grupo_path}, {grupo_excel_path}')

def generar_consecutivo_por_asignatura(asignaturas_df, nivel):
    asignaturas_nivel = asignaturas_df[asignaturas_df['Nivel'] == nivel]
    consecutivos = {}
    for idx, asignatura in enumerate(asignaturas_nivel.itertuples(), start=0):
        asignatura_nombre = asignatura.Asignatura
        consecutivos[asignatura_nombre] = idx % 10
        logging.debug(f'Asignatura: {asignatura_nombre}, Consec. inicial: {consecutivos[asignatura_nombre]}')
    return consecutivos

def matricular_estudiantes(estudiantes_df, asignaturas_df, semestre, nivel, tamano_grupo):
    logging.info(f'Iniciando matriculación de estudiantes para el semestre {semestre}, nivel {nivel}...')
    estudiantes_semestre = estudiantes_df[estudiantes_df['Semestre'] == semestre]
    total_estudiantes_semestre = len(estudiantes_semestre)
    asignaturas_nivel = asignaturas_df[asignaturas_df['Nivel'] == nivel]
    grupos = [estudiantes_semestre[i:i + tamano_grupo] for i in range(0, len(estudiantes_semestre), tamano_grupo)]

    logging.info(f'Total estudiantes en semestre {semestre}: {total_estudiantes_semestre}')
    logging.info(f'Asignaturas en nivel {nivel}: {len(asignaturas_nivel)}')
    logging.info(f'Número de grupos generados: {len(grupos)}')

    base_dir = os.path.join(ruta_final_dir, f'Asignaciones_Semestre_{semestre}')
    crear_directorio_si_no_existe(base_dir)

    consecutivo_asignatura = generar_consecutivo_por_asignatura(asignaturas_df, nivel)

    for index, asignatura in asignaturas_nivel.iterrows():
        asignatura_nombre = asignatura['Asignatura']
        creditos = asignatura['Creditos']
        total_cursos_asignados = len(grupos)
        fecha_creacion = datetime.now().strftime('%Y%m%d')
        asignatura_dir = os.path.join(base_dir, asignatura_nombre)
        crear_directorio_si_no_existe(asignatura_dir)

        logging.info(f'Procesando asignatura: {asignatura_nombre} - Créditos: {creditos}')

        for numero_grupo, grupo in enumerate(grupos, start=1):
            logging.info(f'Asignando grupo {numero_grupo} para la asignatura {asignatura_nombre}...')
            codigo_asignatura = generar_codigo_asignatura(asignatura_nombre, semestre, creditos, consecutivo_asignatura[asignatura_nombre])
            horas_trabajo_docente = calcular_htd(creditos)
            horas_trabajo_independiente = calcular_hti(creditos)
            cantidad_estudiantes = len(grupo)
            logging.info(f'Grupo {numero_grupo} asignado con {cantidad_estudiantes} estudiantes. Código asignatura: {codigo_asignatura}')

            nombre_curso_formateado = asignatura_nombre.replace(" ", "").capitalize()
            grupo_filename = f"{codigo_asignatura}-{nombre_curso_formateado}-{cantidad_estudiantes}-{numero_grupo}.csv"
            grupo_excel_filename = f"{codigo_asignatura}-{nombre_curso_formateado}-{cantidad_estudiantes}-{numero_grupo}.xlsx"
            grupo_path = os.path.join(asignatura_dir, grupo_filename)
            grupo_excel_path = os.path.join(asignatura_dir, grupo_excel_filename)

            grupo_df = pd.DataFrame({
                'Estudiante': grupo['Nombre'],
                'Codigo Asignatura (CA)': codigo_asignatura,
                'Horas de trabajo docente (HTD)': horas_trabajo_docente,
                'Horas de trabajo independiente (HTI)': horas_trabajo_independiente,
                'Numero total de estudiantes (NTE)': total_estudiantes_semestre,
                'Codigo del curso (CC)': numero_grupo,
                'Total de cursos asignados (TCA)': total_cursos_asignados,
                'Fecha de creacion (FC)': fecha_creacion
            })

            log_timed_operation('Guardar Asignaciones', guardar_asignaciones, grupo_df, grupo_path, grupo_excel_path)

    logging.info(f"Archivos CSV y Excel de asignaciones generados para el semestre {semestre}.")

niveles_semestre = {
    1: (1, 30), 2: (2, 30), 3: (3, 30), 4: (4, 25),
    5: (5, 25), 6: (6, 25), 7: (7, 20), 8: (8, 20),
    9: (9, 20), 10: (10, 10)
}

total_procedures = 0

for semestre, (nivel, tamano_grupo) in niveles_semestre.items():
    log_timed_operation('Matricular Estudiantes', matricular_estudiantes, Datos, MallaCurricular, semestre, nivel, tamano_grupo)
    total_procedures += 1

logging.info(f"Total de procedimientos realizados: {total_procedures}")
logging.info("Tipo de acciones realizadas: cargar datos, generar códigos, calcular HTD/HTI, crear directorios, guardar asignaciones")
