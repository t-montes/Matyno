# -*- coding: utf-8 -*-
""" Imports """
from time import localtime
import types

"""Funciones constantes"""

def cargar_constantes(path_constantes:str) -> dict:
    newvars = {}
    var_dt = {"Constants":{}, "Students":{}}
    
    with open(path_constantes, 'r') as file:
        data = [i.rstrip() for i in file.readlines()]
        
        for i in range(len(data)):
            if not data[i].startswith("    "):
                if data[i][:-1] == "Constants":
                    index1 = i
                if data[i][:-1] == "Students":
                    index2 = i
    st_indexes = []
    for i in range(index2+1, len(data)):
        if not data[i].startswith("        "):
            st_indexes.append(i+1)
    
    for i in range(index1+1, index2):
        nm, vl = data[i].split('=')
        nm, vl = nm.replace(' ',''), eval(vl, newvars.copy())
        newvars.update({nm:vl})
        var_dt["Constants"][nm] = vl
    
    while len(st_indexes) > 0:
        newvars = var_dt["Constants"].copy()
        first = st_indexes.pop(0)
        last = st_indexes[0] - 1 if len(st_indexes) > 0 else len(data)
        stud = data[first-1][:-1].replace(' ','')
        for i in range(first, last):
            nm, vl = data[i].split('=')
            nm, vl = nm.replace(' ',''), eval(vl, newvars.copy())
            newvars.update({nm:vl})
            var_dt["Students"][stud] = var_dt["Students"].get(stud, {})
            var_dt["Students"][stud][nm] = vl
    return var_dt

def cargar_colores(path_colores:str, only="") -> dict:
    colors = {}
    with open(path_colores, 'r', encoding="utf-8") as file:
        file.readline()
        for i in file:
            i = i.rstrip().replace('"', '').split(',')
            i[0] = i[0].lower()
            
            if only == "hex":
                colors[i[0]] = i[1].upper()
            elif only == "rgb":
                colors[i[0]] = (int(i[2]), int(i[3]), int(i[4]))
            else:
                colors[i[0]] = colors.get(i[0], {})
                colors[i[0]]["hex"] = i[1].upper()
                colors[i[0]]["rgb"] = (int(i[2]), int(i[3]), int(i[4]))
    return colors

def pastel(hexa:str, n=1) -> str:
    
    for i in range(n):
        #Obtener rgb del color
        rgb = (int(hexa[1:3],16), int(hexa[3:5],16), int(hexa[5:7],16))
        
        #Se promedia con el color blanco (255,255,255)
        past = tuple([(i+255)//2 for i in rgb])
        
        #Se convierte de rgb a hexadecimal
        hexa = "#" + "".join([hex(i)[2:] for i in past]).upper()

    return hexa
    
    

"""Fin Funciones constantes"""

"""Funciones registro"""

def registrar_usuario(correouni:str, path_registro:str, path_constantes:str, nombre_completo: str, codigo: str, correo: str, usuario: str, contrasena: str) -> int:
    if usuario == '':
        usuario = correo[:correo.find('@')]
    
    with open(path_registro, 'r') as file:
        data = file.readlines()
        for i in data:
            if i.split(';')[1] == f'{codigo}':
                return 1
            if i.split(';')[2] == correo:
                return 2
            if i.split(';')[3] == usuario:
                return 3
            if i.split(';')[1] == usuario or i.split(';')[3] == f'{codigo}':
                return 4
            if not correo.endswith("@"+correouni):
                return 5
            if not f'{codigo}'.isdigit() or len(f'{codigo}') < 9:
                return 6
            if usuario.isdigit():
                return 7
            if nombre_completo == '':
                return 8
            if usuario == '':
                return 9
            if correo.count("@") != 1:
                return 10
            if len(contrasena) < 6:
                return 11
    
    ap_str = ''
    ap_str += nombre_completo + ';'
    ap_str += f'{codigo}' + ';'
    ap_str += correo + ';'
    ap_str += usuario + ';'
    ap_str += contrasena + ';'
    
    with open(path_registro, 'a') as file:
        file.write('\n' + ap_str)
        
    with open(f'students/{codigo}_data.csv','w') as file:
        file.write('Nombre materia;Departamento;Número código;Sección;Créditos;Semestre;Profesores;Salones;Horario;Modo calificación;Notas:Porcentajes:Concepto;Estado;Cálculo total')
    
    with open(path_constantes, 'a') as file:
        file.write(f"\n    {codigo}:\n"
                   +"        show_main = 'nombre' # El label principal.\n"
                   +"        bg_color = '#C2F3EF' # Main Site background color.\n"
                   +"        notecolor = 'green'")
    
    return None

def iniciar_sesion(path_registro:str, codigo_correo_o_usuario: str, contrasena: str) -> int:
    codigo_correo_o_usuario = f'{codigo_correo_o_usuario}'
    with open(path_registro, 'r') as file:
        file.readline()
        data = file.readlines()
        index = -1
        for i in range(len(data)):
            a = data[i].split(';')[1]
            b = data[i].split(';')[2]
            c = data[i].split(';')[3]
            if a == codigo_correo_o_usuario or b == codigo_correo_o_usuario or c == codigo_correo_o_usuario:
                index = i
    if index == -1:
        return 1
    if data[index].split(';')[4] == contrasena:
        return data[index].split(';')[1]
    return 2

def dar_usuario_y_demas(path_registro:str, codigo_est: str) -> str:
    with open(path_registro, 'r') as file:
        file.readline()
        data = file.readlines()
        for i in range(len(data)):
            if data[i].split(';')[1] == codigo_est:
                return data[i].rstrip().split(';')
        return None

"""Fin Funciones registro"""

def cargar_materias(codigo_est: str) -> dict:
    #Abrir Archivo y cargar datos.
    nombre_archivo_materias = f'students/{codigo_est}_data.csv'
    with open(nombre_archivo_materias,'r') as file:
        file.readline()
        data = []
        index = 0
        for i in file:
            data.append([])
            for j in i.rstrip().split(';'):
                try:
                    data[index].append(int(j))
                except:
                    try:
                        data[index].append(float(j))
                    except:
                        data[index].append(j)
                        
            index += 1
    del file
    
    #Organizar datos en el formato de retorno (dict).
    mt = {}
    for i in data:
        if i != ['']:
            mt[i[0]] = {}
            if i[1]:
                mt[i[0]]['Código'] = f'{i[1]}{"0"*(4 - len(str(i[2])))}{i[2]}'
            else:
                mt[i[0]]['Código'] = f"{i[2]}"
        
            mt[i[0]]['Sección'] = i[3]
        
            mt[i[0]]['Créditos'] = i[4]
            
            i[5] = "%s"%(i[5])
            try:
                mt[i[0]]['Semestre'] = tuple([int(i[5].split('_')[0]), i[5].split('_')[1]])
            except ValueError:
                try:
                    mt[i[0]]['Semestre'] = tuple([0, i[5].split('_')[1]])
                except IndexError:
                    mt[i[0]]['Semestre'] = (i[5],)
            except IndexError:
                mt[i[0]]['Semestre'] = (i[5],)
            
            mt[i[0]]['Profesores'] = tuple(i[6].split('_'))
        
            mt[i[0]]['Salones'] = tuple(i[7].split('_'))
        
            mt[i[0]]['Horario'] = tuple(i[8].split('_'))
        
            mt[i[0]]['Modo calificación'] = i[9]
        
            mt[i[0]]['Notas'] = []
            index = 0
            for j in i[10].split('_'):
                if not j:
                    continue
                mt[i[0]]['Notas'].append(tuple())
                for k in j.split(':'):
                    try:
                        mt[i[0]]['Notas'][index] += (float(k),)
                    except:
                        mt[i[0]]['Notas'][index] += (k,)
                index += 1
                
            try:
                mt[i[0]]['Estado'] = i[11]
                
                mt[i[0]]['Cálculo total'] = i[12]
            except:
                pass
            
            porc = 0
            prom = 0
            for j in mt[i[0]]['Notas']:
                try:
                    prom += j[0]*j[1]
                    porc += j[1]
                except:
                    pass
            mt[i[0]]['Porcentaje total']= round(porc, 3)
            try:
                mt[i[0]]['Nota promedio'] = round(prom/porc, 2)
            except:
                mt[i[0]]['Nota promedio'] = 0
    
    return mt

def info_PGA(mt:dict, actualsem:str="") -> tuple:
    #perSem - Dict of Tuples
    #Tuple: (suma de notas,  
    #        núm de materias con nota,  
    #        núm de créditos con nota,  
    #        núm créditos totales aprobados,
    #        núm créditos totales)
    
    perSem = {} # Example: {"2020-10":(8.43, 2, 4, 24, 24), ...}
    
    if not actualsem:
        actualsem = semestre_actual()
    
    actualPGA = 0
    actualMat = 0
    actualH = 0
    for i in mt:
        # Obtener semestre
        sem = mt[i]['Semestre'][1]
        if sem.endswith('A') or sem.endswith('B'):
            sem = sem[:-1]
        tup = perSem.get(sem, [0, 0, 0, 0, 0])
        
        # Obtener nota definitiva.
        try: nota = eval(mt[i]['Cálculo total'], {'NP': mt[i]['Nota promedio']}, {})
        except: nota = mt[i]['Nota promedio']
        
        if sem == actualsem:
            if mt[i]['Modo calificación'] == 'NUMERICO':
                actualPGA += nota
                actualMat += 1
            actualH += mt[i]['Créditos']
        
        # Si ya se terminó al 100%
        if round(mt[i]['Porcentaje total'],1) == 1:
            # Si es numérico aporta al PGA.
            if mt[i]['Modo calificación'] == 'NUMERICO':
                tup[0] += nota
                tup[1] += 1
                tup[2] += mt[i]['Créditos']
            
            # Si está aprobado aporta a las horas PGA (aprobadas)
            if nota >= 3.0:
                if type(mt[i]['Créditos']) is int:
                    tup[3] += mt[i]['Créditos']
        
        tup[4] += mt[i]['Créditos']
        
        perSem[sem] = tup
    
    # PGA_semestral = (suma de notas / núm de materias con nota) en el semestre
    # PGA total = SUMA(PGA_semestral * núm de créditos con nota semestral) / suma total de créditos con nota
    
    pgatot = 0
    sumh_con_nota = 0
    sumh_aprobado = 0
    for i in perSem:
        try: pgatot += (perSem[i][0]/perSem[i][1])*perSem[i][2]
        except: pass
    
        sumh_con_nota += perSem[i][2]
        sumh_aprobado += perSem[i][3]
        
    try: pgatot /= sumh_con_nota
    except: pass
        
    try: actualPGA /= actualMat
    except: pass
    
    # XXX Cambiar, que el total se calculé según el total de Pensumanager
    totalSistemasYElectronica = 191
    ssc = round((sumh_aprobado/totalSistemasYElectronica)*10, 3)
    
    return pgatot, sumh_aprobado, ssc, actualPGA, actualH

# def info_PGA(mt: dict) -> tuple:
#     PGA = 0
#     horas_PGA = 0
#     cont = 0
#     horas_pendientes = 0
#     for i in mt:
#         # Obtener nota definitiva.
#         try: nota = eval(mt[i]['Cálculo total'], {'NP': mt[i]['Nota promedio']}, {})
#         except: nota = mt[i]['Nota promedio']
        
#         #Si ya se terminó el 100% del curso
#         if round(mt[i]['Porcentaje total'],1) == 1:
#             # Si es numérico aporta al PGA.
#             if mt[i]['Modo calificación'] == 'NUMERICO':
#                 PGA += nota
#                 cont += 1
                
#             # Si está aprobado aporta a las horas PGA (aprobadas)
#             if nota >= 3.0:
#                 if type(mt[i]['Créditos']) is int:
#                     horas_PGA += mt[i]['Créditos']
#         else:
#             #Si no se ha terminado se suma a las horas pendientes
#             horas_pendientes += mt[i]['Créditos']
    
    
#     try:
#         PGA /= cont
#         PGA = round(PGA, 3)
#     except:
#         PGA = 0
#     
#     totalSistemasYElectronica = 191
#     ssc = round((horas_PGA/totalSistemasYElectronica)*10, 3)
    
#     return (PGA, horas_PGA, ssc, horas_pendientes)

def semestre_actual(actual=localtime()):
    
    if actual.tm_mon == 7:
        nm = 19
    else:
        nm = (((actual.tm_mon - 1)//6) + 1)*10
    return f"{actual.tm_year}-{nm}"

def centrar_texto(cadena: str, ancho_terminal: int, delante:bool=True) -> str:
    cadena = str(cadena)
    if len(cadena) < ancho_terminal:
        spc = ' '*((ancho_terminal - len(cadena))//2)
        cd = spc + cadena + spc
        while len(cd) < ancho_terminal:
            if delante:
                cd = cd + ' '
            else:
                cd = ' ' + cd
    elif len(cadena) == ancho_terminal:
        cd = cadena
    elif len(cadena) > ancho_terminal:
        cd = cadena[:ancho_terminal-1]
        cd = cd + '…'
    return cd
    

"""Funciones agregar"""

def recurrent_tuple_or_str(data, separator:str) -> str:
    st = ''
    if type(data) is tuple:
        for i in data:
            st += "%s"%i + separator
        st = st[:-1]
    else:
        st += f'{data}'
    return st

def agregar_materia(codigo_est: str, nombre: str, codigo: str, seccion: int = '', creditos: int = '', semestreYperiodo: tuple = ('',''), profesores: tuple = '',
                    salones: tuple = '', horario: tuple = '', modo_calificacion: str = '') -> dict:
    nombre_archivo_materias = f'students/{codigo_est}_data.csv'
    with open(nombre_archivo_materias, 'r') as file:
        data = file.readlines()
        for i in data:
            if i not in ('', '\n'):
                if i.split(';')[0] == nombre:
                    raise NameError(f'El nombre de la materia \'{i.split(";")[0]}\' ya existe en el archivo.')
                if f'{i.split(";")[1] + " " if i.split(";")[1] else ""}{i.split(";")[2]}' == codigo:
                    raise NameError('El código de la materia \''
                                    +f'{i.split(";")[1] + " " if i.split(";")[1] else ""}{i.split(";")[2]}\' ya existe en el archivo')
            else:
                l = '\\n' if i == '\n' else '';print(f"Warning. Found line: '{l}'"); del l
    ap_str = ''
    ap_str += nombre + ';'
    if codigo.count(' ') == 1:
        ap_str += codigo[:codigo.find(' ')].upper() + ';' + codigo[codigo.find(' ')+1:].upper() + ';'
    else:
        ap_str += ';' + codigo.upper() + ';'
    ap_str += f'{seccion}' + ';'
    ap_str += f'{creditos}' + ';'
    ap_str += f'{semestreYperiodo[0]}' + '_' + semestreYperiodo[1] + ';'
    ap_str += recurrent_tuple_or_str(profesores, '_') + ';'
    ap_str += recurrent_tuple_or_str(salones, '_') + ';'
    ap_str += recurrent_tuple_or_str(horario, '_') + ';'
    ap_str += modo_calificacion.replace('é', 'e').replace('É', 'E').upper() + ';'
    ap_str += ';'
    ap_str += 'Pendiente;' #Estado
    ap_str += 'NP' #Cálculo total
    
    with open(nombre_archivo_materias, 'a') as file:
        file.write('\n' + ap_str)

def recurrent_agregar_criterio(codigo_est:str, nombre_materia : str, indice_criterio: int, ap_str: str) -> None:
    nombre_archivo_materias = f'students/{codigo_est}_data.csv'
    with open(nombre_archivo_materias, 'r') as file:
        data = []
        cont = 0
        index = -1
        for i in file:
            data.append(i)
            if i.split(';')[0] == nombre_materia:
                index = cont
            cont += 1
        del cont
        if index == -1:
            raise NameError(f'No se encuentra almacenada ninguna materia con el nombre \'{nombre_materia}\'')
    
    line = data[index].split(';')
    
    if indice_criterio == len(line) - 1:
        if line[indice_criterio] == '':
            if index == len(data) - 1:
                data[index] = data[index].rstrip() + ap_str
            else:
                data[index] = data[index].rstrip() + ap_str + '\n'
        else:
            if index == len(data) - 1:
                data[index] = data[index].rstrip() + '_' + ap_str
            else:
                data[index] = data[index].rstrip() + '_' + ap_str + '\n'
    else:
        if line[indice_criterio] == '':
            line[indice_criterio] = ap_str
        else:
            line[indice_criterio] += '_' + ap_str
        data[index] = ';'.join(line)
    
    with open(nombre_archivo_materias, 'w') as file:
        i = 0
        while i < len(data):
            if data[i] == '' or data[i] == '\n':
                del data[i]
            else:
                i += 1
        file.writelines(data)

def agregar_profesores_mt(codigo_est:str, nombre: str, *profesores: str) -> dict:
    ap_str = ''
    for i in profesores:
        ap_str += f'{i}_'
    ap_str = ap_str[:-1]
    
    recurrent_agregar_criterio(codigo_est,nombre,6, ap_str)
    
def agregar_salones_mt(codigo_est:str, nombre: str, *salones: str) -> dict:
    ap_str = ''
    for i in salones:
        ap_str += f'{i}_'
    ap_str = ap_str[:-1]
    
    recurrent_agregar_criterio(codigo_est,nombre,7, ap_str)

def agregar_horario_mt(codigo_est:str, nombre: str, *dias: str) -> dict:
    ap_str = ''
    for i in dias:
        ap_str += f'{i}_'
    ap_str = ap_str[:-1]
    
    recurrent_agregar_criterio(codigo_est,nombre,8, ap_str)

def agregar_notas_mt(codigo_est:str, nombre: str, *nota_porcentaje_concepto:tuple) -> dict:
    ap_str = ''
    for i in nota_porcentaje_concepto:
        ap_str += f'{i[0]}:{i[1]}:{i[2]}_'
    ap_str = ap_str[:-1]
    
    recurrent_agregar_criterio(codigo_est,nombre, 10, ap_str)

"""Fin Funciones agregar"""

"""Funciones cambiar mt"""

def recurrent_cambiar_criterio(codigo_est:str,nombre_materia: str, indice_criterio: int, *nuevo_valor: str, tup=False) -> None:
    nombre_archivo_materias = f'students/{codigo_est}_data.csv'
    with open(nombre_archivo_materias, 'r') as file:
        data = []
        cont = 0
        index = -1
        for i in file:
            data.append(i)
            if i.split(';')[0] == nombre_materia:
                index = cont
            cont += 1
        del cont
        if index == -1:
            raise NameError(f'No se encuentra almacenada ninguna materia con el nombre \'{nombre_materia}\'')
    
    line = data[index].split(';')
    #Si son varios profesores o salones.
    if (indice_criterio == 6 or indice_criterio == 7) and tup:
        existe = False
        for i in line[indice_criterio].split('_'):
            if nuevo_valor[0] == i:
                existe = True
                break
        if existe:
            line[indice_criterio] = line[indice_criterio].replace(nuevo_valor[0],nuevo_valor[1])
        else:
            raise NameError(f'No se encuentra almacenado en la materia \'{nombre_materia}\' el valor a reemplazar \'{nuevo_valor[0]}\'')
    else:
        line[indice_criterio] = f'{nuevo_valor[0]}'
    data[index] = ';'.join(line)
    
    with open(nombre_archivo_materias, 'w') as file:
        i = 0
        while i < len(data):
            if data[i] == '' or data[i] == '\n':
                del data[i]
            else:
                i += 1
        file.writelines(data)

def cambiar_nombre_mt(codigo_est:str, nombre: str, nuevo_nombre: str) -> dict:
    """Cambia el nombre de la materia con el nombre dado por parámetro"""
    recurrent_cambiar_criterio(nombre, 0, nuevo_nombre)

def cambiar_codigo_mt(codigo_est:str, nombre: str, nuevo_codigo: str) -> dict:
    """Cambia el código de la materia con el nombre dado por parámetro"""
    recurrent_cambiar_criterio(nombre, 1, nuevo_codigo[:4])
    recurrent_cambiar_criterio(nombre, 2, nuevo_codigo[4:])

def cambiar_seccion_mt(codigo_est:str, nombre: str, nueva_seccion: int) -> dict:
    """Cambia la sección de la materia con el nombre dado por parámetro"""
    recurrent_cambiar_criterio(nombre,3,nueva_seccion)
    
def cambiar_creditos_mt(codigo_est:str, nombre: str, nuevo_num_creditos: int) -> dict:
    """Cambia los créditos de la materia con el nombre dado por parámetro"""
    recurrent_cambiar_criterio(nombre,4,nuevo_num_creditos)

def cambiar_semestre_mt(codigo_est:str, nombre: str, semestre: int, periodo_semestre: str) -> dict:
    """Cambia el semestre y el periodo de la materia con el nombre dado por parámetro"""
    recurrent_cambiar_criterio(nombre,5,f'{semestre}_{periodo_semestre}')

def cambiar_profesor_mt(codigo_est:str, nombre: str, nuevo_profesor: str, profesor_a_reemplazar: str = '') -> dict:
    """Cambia el profesor indicado de la materia con el nombre dado por parámetro"""
    if profesor_a_reemplazar == '':
        recurrent_cambiar_criterio(nombre,6,nuevo_profesor)
    else:
        recurrent_cambiar_criterio(nombre,6,profesor_a_reemplazar,nuevo_profesor, tup=True)

def cambiar_salon_mt(codigo_est:str, nombre: str, nuevo_salon: str, salon_a_reemplazar: str = '') -> dict:
    """Cambia el salon indicado de la materia con el nombre dado por parámetro"""
    if salon_a_reemplazar == '':
        recurrent_cambiar_criterio(nombre,7,nuevo_salon)
    else:
        recurrent_cambiar_criterio(nombre,7,salon_a_reemplazar,nuevo_salon, tup=True)

def cambiar_horario_mt(codigo_est:str, nombre: str, *horario: str) -> dict:
    """Cambia el horario de la materia con el nombre dado por parámetro"""
    linea = ''
    for i in horario:
        linea += f'{i}_'
    linea = linea[:-1]
    recurrent_cambiar_criterio(nombre,8,linea)

def cambiar_modo_calificacion_mt(codigo_est: str,nombre: str, modo_calificacion: str) -> dict:
    """Cambia el modo de calificación de la materia con el nombre dado por parámetro"""
    recurrent_cambiar_criterio(nombre,9,modo_calificacion)

def cambiar_nota_mt(codigo_est: str, nombre: str, indice_nota: int, nue_nota: float, nue_porcentaje: float, nue_concepto: str) -> dict:
    """Cambia la nota del índice especificado de la materia con el nombre dado por parámetro"""
    nombre_archivo_materias = f'students/{codigo_est}_data.csv'
    with open(nombre_archivo_materias, 'r') as file:
        data = []
        cont = 0
        index = -1
        for i in file:
            data.append(i)
            if i.split(';')[0] == nombre:
                index = cont
            cont += 1
        del cont
        if index == -1:
            raise NameError(f'No se encuentra almacenada ninguna materia con el nombre \'{nombre}\'')
    
    line = data[index].split(';')
    line2 = line[10].split('_')
    del line[10]
    
    if indice_nota > len(line2) - 1:
        raise IndexError(f'Únicamente existen {len(line2)} notas para la materia \'{nombre}\'. Índice {indice_nota + 1} fuera del rango.')
    
    line2[indice_nota] = f'{nue_nota}:{nue_porcentaje}:{nue_concepto}'
    line.insert(10, '_'.join(line2))
    data[index] = ';'.join(line)
    
    with open(nombre_archivo_materias, 'w') as file:
        i = 0
        while i < len(data):
            if data[i] == '' or data[i] == '\n':
                del data[i]
            else:
                i += 1
        file.writelines(data)

"""Fin Funciones cambiar mt"""

"""Funciones quitar"""

def quitar_mt(codigo_est:str, nombre: str) -> dict:
    nombre_archivo_materias = f'students/{codigo_est}_data.csv'
    with open(nombre_archivo_materias, 'r') as file:
        data = []
        cont = 0
        index = -1
        for i in file:
            data.append(i)
            if i.split(';')[0] == nombre:
                index = cont
            cont += 1
        del cont
        if index == -1:
            raise NameError(f'No se encuentra almacenada ninguna materia con el nombre \'{nombre}\'')
    
    del data[index]
    
    with open(nombre_archivo_materias, 'w') as file:
        i = 0
        while i < len(data):
            if data[i] == '' or data[i] == '\n':
                del data[i]
            else:
                i += 1
        file.writelines(data)
    
def recurrent_quitar_criterio(codigo_est:str, nombre_materia: str, indice_criterio: int, indice_quitar: int = -1) -> None:
    nombre_archivo_materias = f'students/{codigo_est}_data.csv'
    with open(nombre_archivo_materias, 'r') as file:
        data = []
        cont = 0
        index = -1
        for i in file:
            data.append(i)
            if i.split(';')[0] == nombre_materia:
                index = cont
            cont += 1
        del cont
        if index == -1:
            raise NameError(f'No se encuentra almacenada ninguna materia con el nombre \'{nombre_materia}\'')
    
    line = data[index].split(';')
    if indice_quitar != -1:
        line2 = line[indice_criterio].split('_')
        del line2[indice_quitar]
        line[indice_criterio] = '_'.join(line2)
    else:
        line[indice_criterio] = ''
    
    data[index] = ';'.join(line)
    
    with open(nombre_archivo_materias, 'w') as file:
        i = 0
        while i < len(data):
            if data[i] == '' or data[i] == '\n':
                del data[i]
            else:
                i += 1
        file.writelines(data)

def quitar_seccion_mt(codigo_est:str, nombre: str) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,3)

def quitar_creditos_mt(codigo_est:str, nombre: str) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,4)

def quitar_semestre_mt(codigo_est:str, nombre: str) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,5)

def quitar_profesor_mt(codigo_est:str, nombre: str, indice: int = -1) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,6, indice)

def quitar_salon_mt(codigo_est:str, nombre: str, indice: int = -1) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,7, indice)

def quitar_dia_mt(codigo_est:str, nombre: str, indice: int = -1) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,8, indice)

def quitar_modo_calificacion_mt(codigo_est:str,nombre: str) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,9)

def quitar_nota_mt(codigo_est:str, nombre: str, indice: int = -1) -> dict:
    recurrent_quitar_criterio(codigo_est,nombre,10, indice)

"""Fin Funciones quitar"""

"""Funciones dar mts por"""

def dar_mt_por_nombre(mt: dict, nombre: str) -> dict:
    """Retorna exclusivamente una materia cuyo nombre coincida con el dado por parámetro"""
    for i in mt:
        if i == nombre:
            return mt[i]
    return {}

def dar_mt_por_codigo(mt: dict, codigo: str) -> dict:
    """Retorna exclusivamente una materia cuyo código coincida con el dado por parámetro"""
    for i in mt:
        if mt[i]['Código'] == codigo:
            return mt[i]
    return {}

def dar_mts_por_departamento(mt: dict, departamento: str) -> dict:
    """Retorna todas las materias que pertenezcan al departamento dado por parámetro"""
    mts_pd = {}
    for i in mt:
        if mt[i]['Código'][:4] == departamento:
            mts_pd[i] = mt[i]
    return mts_pd

def dar_mts_por_creditos(mt: dict, creditos: int) -> dict:
    """Retorna todas las materias que tengan el número de créditos dados por parámetro"""
    mts_pc = {}
    for i in mt:
        if mt[i]['Créditos'] == creditos:
            mts_pc[i] = mt[i]
    return mts_pc

def dar_mts_por_semestre(mt: dict, semestre: str) -> dict:
    """Retorna todas las materias que se hayan cursado en el semestre dado por parámetro"""
    mts_ps = {}
    for i in mt:
        if semestre in mt[i]['Semestre'][1]:
            mts_ps[i] = mt[i]
    return mts_ps
    
def dar_mts_por_profesor(mt: dict, profesor: str) -> dict:
    """Retorna todas las materias que hayan sido dictadas por el profesor dado por parámetro"""
    mts_pp = {}
    for i in mt:
        if profesor in mt[i]['Profesores']:
            mts_pp[i] = mt[i]
    return mts_pp

def dar_mts_por_edificio(mt: dict, edificio: str) -> dict:
    """Retorna todas las materias que hayan sido vistas en el edificio dado por parámetro"""
    mts_pe = {}
    for i in mt:
        for j in mt[i]['Salones']:
            if edificio in j and i not in mts_pe:
                mts_pe[i] = mt[i]
    return mts_pe

def dar_mts_por_dias(mt: dict, *dias: str) -> dict:
    """Retorna todas las materias que se hayan visto en los días dados por parámetro"""
    mts_ph = {}
    for i in mt:
        cont = 0
        for j in dias:
            if j in mt[i]['Horario']:
                cont += 1
        if cont == len(dias):
            mts_ph[i] = mt[i]
    return mts_ph

def dar_mts_por_modo_calificacion(mt: dict, modo_calificacion: str) -> dict:
    """Retorna todas las materias que SI/NO tienen estándar de calificación numérico"""
    mts_pmc = {}
    for i in mt:
        if mt[i]['Modo calificación'] == modo_calificacion:
            mts_pmc[i] = mt[i]
    return mts_pmc
    
def dar_mts_completas(mt: dict) -> dict:
    """Retorna todas las materias que hayan sido finalizadas al 100%"""
    mts_c = {}
    for i in mt:
        if mt[i]['Porcentaje total'] == 1.0:
            mts_c[i] = mt[i]
    return mts_c

def dar_mts_incompletas(mt: dict) -> dict:
    """Retorna todas las materias que NO hayan sido finalizadas al 100%"""
    mts_ic = {}
    for i in mt:
        if mt[i]['Porcentaje total'] < 1.0:
            mts_ic[i] = mt[i]
    return mts_ic

def dar_mts_aprobadas(mt: dict) -> dict:
    """Retorna todas las materias que tengan una nota superior o igual a 3.0"""
    mts_a = {}
    for i in mt:
        if mt[i]['Nota promedio'] >= 3.0:
            mts_a[i] = mt[i]
    return mts_a

def dar_mts_reprobadas(mt: dict) -> dict:
    """Retorna todas las materias que tengan una nota inferior a 3.0"""
    mts_r = {}
    for i in mt:
        if mt[i]['Nota promedio'] < 3.0:
            mts_r[i] = mt[i]
    return mts_r

"""Fin Funciones dar"""

"""Funciones ordenar mts"""

def recurrent_quitar_tildes(e: str):
    e = e.lower().replace(' ','')
    et = ''
    til = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ñ':'n'}
    for i in e:
        if i in til:
            et += til[i]
        else:
            et += i
    return et

def ordenar_mts_nombre(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por orden alfabético del nombre"""
    n_mts = {}
    n_keys = list(mt.keys())
    n_keys.sort(reverse=rev, key=recurrent_quitar_tildes)
    for i in n_keys:
        n_mts[i] = mt[i]
    return n_mts

def recurrent_ordenar_criterio(e: tuple):
    if e[2] == 'Horario':
        return len(e[1][e[0]][e[2]])
    elif type(e[2]) is tuple:
        return e[1][e[0]][e[2]][0]
    else:
        return e[1][e[0]][e[2]]

def ordenar_mts_codigo(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por orden alfabético del código"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Código'))
    n_keys.sort(reverse=rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts

def ordenar_mts_creditos(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por orden de créditos"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Créditos'))
    n_keys.sort(reverse= not rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts
    
def ordenar_mts_semestre(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por semestres"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Semestre'))
    n_keys.sort(reverse= not rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts
    
def ordenar_mts_profesor(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por orden alfabético del primer profesor"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Profesores'))
    n_keys.sort(reverse= rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts

def ordenar_mts_salon(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por orden alfabético del primer salón"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Salones'))
    n_keys.sort(reverse = rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts

def ordenar_mts_modo_calificacion(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por su modo de calificación"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Modo calificación'))
    n_keys.sort(reverse= rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts

def ordenar_mts_nota(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por su orden de notas"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Nota promedio'))
    n_keys.sort(reverse= not rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts

def ordenar_mts_intensidad_horaria(mt: dict, rev: bool = False) -> dict:
    """Retorna el mismo diccionario de materias dado por parámetro, ordenado por el número de veces que se ve la materia en la semana"""
    n_mts = {}
    n_keys = []
    for i in mt:
        n_keys.append((i, mt, 'Horario'))
    n_keys.sort(reverse= not rev, key=recurrent_ordenar_criterio)
    for i in n_keys:
        n_mts[i[0]] = mt[i[0]]
    return n_mts

"""Fin Funciones ordenar mts"""

def print_mt(mt: dict) -> None:
    for i in mt:
        print(f'{i}:')
        for j in mt[i]:
            print(f'\t{j}: {mt[i][j]}')
        print()



"""

#CONSOLA (temporal)
print("Bienvenido a Matyno Uniandes.")
while 1:
    opt = int(input("Digita 0 si deseas registrarte, 1 si deseas iniciar sesión, 2 para salir:\n"))
    if opt == 0:
        nombre = input("Digita tu nombre:\n")
        codigo = input("Digita tu código uniandes:\n")
        correo = input("Digita tu correo uniandes:\n")
        usuario = correo[:correo.find('@')]
        pswrd = input("Digita tu contraseña (No pongas ninguna contraseña real!):\n")
        err_cod = registrar_usuario("config/register.csv", nombre, codigo, correo, usuario, pswrd)
        if err_cod is None:
            print(f"Se ha registrado el usuario '{usuario}'!")
            del nombre, correo, usuario, pswrd, err_cod
            break
        elif err_cod == 1:
            print(f"El código {codigo} ya se encuentra registrado")
        elif err_cod == 2:
            print(f"El correo {correo} ya se encuentra registrado")
        elif err_cod == 3:
            print(f"El usuario {usuario} ya se encuentra registrado")
        elif err_cod == 4:
            print(f"Hubo errores al registrar el usuario:{usuario} y el código:{codigo}")
        elif err_cod == 5:
            print(f"El correo {correo} no es un correo uniandes")
        elif err_cod == 6:
            print(f"El código {codigo} no parece ser un código de estudiante")
        elif err_cod == 7:
            print(f"El usuario no puede ser un número, {usuario} es un número")
    elif opt == 1:
        codigo = input("Digita tu código, correo o usuario:\n")
        pswrd = input("Digita tu contraseña (No pongas ninguna contraseña real!):\n")
        cod_2 = iniciar_sesion("config/registers.csv", codigo, pswrd)
        if cod_2 == 1:
            print(f"No se encontró ninguna coincidencia con {codigo}")
        elif cod_2 == 2:
            print("La contraseña no coincide")
        else:
            codigo = cod_2 
            print(f"Se ha iniciado sesión con el usuario '{dar_usuario(codigo)}'!")
            del pswrd, cod_2
            break
    elif opt == 2:
        print('Gracias por utilizar Matyno Uniandes!')
        if "codigo" in globals():
            del codigo
        break

if "codigo" in globals():
    mt = cargar_materias(codigo)
    PGA_horas_PGA = info_PGA(mt)
    
    #mt = agregar_materia(codigo, 'Hola', 'IELE0001L','3','5',(2,'2020-20A'),'Tony Montes','Au 105',('Lunes','Viernes'),'NUMERICO')
    #mt = agregar_notas_mt(codigo, 'Hola', (5,0.1,'Tarea 1'), (3,0.5,'Parcial 1'), (4,0.3,'Parcial 2'))

"""
