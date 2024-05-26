import pandas as pd
import os
from datetime import datetime
import time
import platform
import logging

CarpetaPrincipal = 'Matriculas'
os.makedirs(CarpetaPrincipal, exist_ok=True)
RutaLog = os.path.join(CarpetaPrincipal, 'matriculacion.txt')

logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S', handlers=[
    logging.FileHandler(RutaLog, encoding='utf-8'),
    logging.StreamHandler()
])

user = os.getlogin()
InfoSistema = platform.uname()
InfoEncabezado = f"Usuario: {user}, Sistema operativo: {InfoSistema.system}, Plataforma: {InfoSistema.release}, Version: {InfoSistema.version}, Máquina: {InfoSistema.machine}, Procesador: {InfoSistema.processor}"

logging.info(InfoEncabezado)

def TiempoDeEjecucion(NombreDeLaOperacion, func, *args, **kwargs):
    TiempoInicial = time.time()
    result = func(*args, **kwargs)
    TiempoFinal = time.time()
    TiempoTranscurrido = TiempoFinal - TiempoInicial
    logging.info(f"{NombreDeLaOperacion}\tTiempo: {TiempoTranscurrido:.6f} segundos")
    return result

logging.info('Cargando datos iniciales y malla curricular...')
DatosIniciales = TiempoDeEjecucion('Cargar Datos Iniciales', pd.read_csv, 'https://github.com/JuanDiosa/Trabajo_Final_AyP/raw/213a425e4ee26788abac77401237b4dd377a2ca1/AyP/Estudiantes.csv', encoding='latin1', delimiter=';')
MallaCurricular = TiempoDeEjecucion('Cargar Malla Curricular', pd.read_csv, 'https://github.com/JuanDiosa/Trabajo_Final_AyP/raw/213a425e4ee26788abac77401237b4dd377a2ca1/AyP/MallaCurricular.csv', encoding='latin1', delimiter=';')
Datos = DatosIniciales.drop(columns=['Fecha'])
logging.info('Datos cargados con éxito.')

def GenerarCodigoDeAsignatura(asignatura, Semestre, Creditos, consecutivo):
    codigo = f"{asignatura[:3].upper()}{Semestre}{Creditos}{consecutivo:01d}"
    logging.debug(f'Generado código de asignatura: {codigo}')
    return codigo

def CalcularHTD(Creditos):
    htd = {4: 96, 3: 64, 2: 32, 1: 16}.get(Creditos, 0)
    logging.debug(f'Calculadas horas de trabajo docente (HTD) para {Creditos} créditos: {htd}')
    return htd

def CalcularHTI(Creditos):
    hti = {4: 120, 3: 80, 2: 64, 1: 32}.get(Creditos, 0)
    logging.debug(f'Calculadas horas de trabajo independiente (HTI) para {Creditos} créditos: {hti}')
    return hti

def CrearDirectorioSiNoExiste(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        logging.info(f'Directorio creado: {ruta}')
    else:
        logging.info(f'Directorio ya existe: {ruta}')

def GuardarArchivos(DataframeDeGrupo, RutaCSV, RutaEXCEL):
    DataframeDeGrupo.to_csv(RutaCSV, index=False, encoding='latin1')
    DataframeDeGrupo.to_excel(RutaEXCEL, index=False)
    logging.info(f'Archivos guardados: {RutaCSV}, {RutaEXCEL}')

def GenerarConsecutivoParaLasAsignaturas(asignaturas_df, nivel):
    AsignaturasPorNivel = asignaturas_df[asignaturas_df['Nivel'] == nivel]
    consecutivos = {}
    for idx, asignatura in enumerate(AsignaturasPorNivel.itertuples(), start=0):
        NombreDeLaAsignatura = asignatura.Asignatura
        consecutivos[NombreDeLaAsignatura] = idx % 10
        logging.debug(f'Asignatura: {NombreDeLaAsignatura}, Consec. inicial: {consecutivos[NombreDeLaAsignatura]}')
    return consecutivos

def MatricularEstudiantes(estudiantes_df, asignaturas_df, Semestre, nivel, MaximoDeEstudiantesPorGrupo):
    logging.info(f'Iniciando matriculación de estudiantes para el semestre {Semestre}, nivel {nivel}...')
    EstudiantesPorSemestre = estudiantes_df[estudiantes_df['Semestre'] == Semestre]
    TotalDeEstudiantesPorSemestre = len(EstudiantesPorSemestre)
    AsignaturasPorNivel = asignaturas_df[asignaturas_df['Nivel'] == nivel]
    Grupos = [EstudiantesPorSemestre[i:i + MaximoDeEstudiantesPorGrupo] for i in range(0, len(EstudiantesPorSemestre), MaximoDeEstudiantesPorGrupo)]

    logging.info(f'Total estudiantes en semestre {Semestre}: {TotalDeEstudiantesPorSemestre}')
    logging.info(f'Asignaturas en nivel {nivel}: {len(AsignaturasPorNivel)}')
    logging.info(f'Número de grupos generados: {len(Grupos)}')

    base_dir = os.path.join(CarpetaPrincipal, f'Semestre_{Semestre}')
    CrearDirectorioSiNoExiste(base_dir)

    consecutivo_asignatura = GenerarConsecutivoParaLasAsignaturas(asignaturas_df, nivel)

    for index, asignatura in AsignaturasPorNivel.iterrows():
        NombreDeLaAsignatura = asignatura['Asignatura']
        Creditos = asignatura['Creditos']
        TotalDeCursosAsignados = len(Grupos)
        FechaDeCreacion = datetime.now().strftime('%Y%m%d')
        DirectorioAsignatura = os.path.join(base_dir, NombreDeLaAsignatura)
        CrearDirectorioSiNoExiste(DirectorioAsignatura)

        logging.info(f'Procesando asignatura: {NombreDeLaAsignatura} - Créditos: {Creditos}')

        for NumeroDeGrupo, grupo in enumerate(Grupos, start=1):
            logging.info(f'Asignando grupo {NumeroDeGrupo} para la asignatura {NombreDeLaAsignatura}...')
            CodigoDeAsignatura = GenerarCodigoDeAsignatura(NombreDeLaAsignatura, Semestre, Creditos, consecutivo_asignatura[NombreDeLaAsignatura])
            HorasDeTrabajoDocente = CalcularHTD(Creditos)
            HorasDeTrabajoIndependiente = CalcularHTI(Creditos)
            CantidadDeEstudiantes = len(grupo)
            logging.info(f'Grupo {NumeroDeGrupo} asignado con {CantidadDeEstudiantes} estudiantes. Código asignatura: {CodigoDeAsignatura}')

            NombreDeAsignaturaFormateado = NombreDeLaAsignatura.replace(" ", "").capitalize()
            NombreArchivoCSV = f"{CodigoDeAsignatura}-{NombreDeAsignaturaFormateado}-{CantidadDeEstudiantes}-{NumeroDeGrupo}.csv"
            NombreArchivoEXCEL = f"{CodigoDeAsignatura}-{NombreDeAsignaturaFormateado}-{CantidadDeEstudiantes}-{NumeroDeGrupo}.xlsx"
            RutaCSV = os.path.join(DirectorioAsignatura, NombreArchivoCSV)
            RutaEXCEL = os.path.join(DirectorioAsignatura, NombreArchivoEXCEL)

            DataframeDeGrupo = pd.DataFrame({
                'Estudiante': grupo['Nombre'],
                'Codigo Asignatura (CA)': CodigoDeAsignatura,
                'Horas de trabajo docente (HTD)': HorasDeTrabajoDocente,
                'Horas de trabajo independiente (HTI)': HorasDeTrabajoIndependiente,
                'Numero total de estudiantes (NTE)': TotalDeEstudiantesPorSemestre,
                'Codigo del curso (CC)': NumeroDeGrupo,
                'Total de cursos asignados (TCA)': TotalDeCursosAsignados,
                'Fecha de creacion (FC)': FechaDeCreacion
            })

            TiempoDeEjecucion('Guardar Asignaciones', GuardarArchivos, DataframeDeGrupo, RutaCSV, RutaEXCEL)

    logging.info(f"Archivos CSV y Excel de asignaciones generados para el semestre {Semestre}.")

DatosParaMatricular = {
    1: (1, 30), 2: (2, 30), 3: (3, 30), 4: (4, 25),
    5: (5, 25), 6: (6, 25), 7: (7, 20), 8: (8, 20),
    9: (9, 20), 10: (10, 10)
}


for Semestre, (nivel, MaximoDeEstudiantesPorGrupo) in DatosParaMatricular.items():
    TiempoDeEjecucion('Matricular Estudiantes', MatricularEstudiantes, Datos, MallaCurricular, Semestre, nivel, MaximoDeEstudiantesPorGrupo)

logging.info("Tipo de acciones realizadas: cargar datos, generar códigos, calcular HTD/HTI, crear directorios, guardar asignaciones")
