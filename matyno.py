# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import matyno_module as mod
from functools import partial
import time
import os

# TODO - Error: al poner '\n' el programa crashea.
# TODO - Error: al poner separadores: ';', '_', ':' el programa crashea.

"""Create Folders"""
parent_dir = "./"
try:    
    directory = "config"
    path = os.path.join(parent_dir, directory) 
    os.mkdir(path) 
    print("Directory '% s' created" % directory) 
except FileExistsError:
    pass

try:
    directory = "students"
    path = os.path.join(parent_dir, directory) 
    os.mkdir(path) 
    print("Directory '% s' created" % directory) 
except FileExistsError:
    pass

"""Paths"""

path_register = "config/registers.csv"
path_configs  = "config/config.txt"
path_colors = "colors.csv"

"""Tkinter Functions and Classes"""

def round2(number:float, ndigits:int=0):
    n = int(number*(10**ndigits))
    n /= (10**ndigits)
    return n

class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", title_frame_opts={}, *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = tk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.label = tk.Label(self.title_frame, text=text, **title_frame_opts)
        self.label.pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=1, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwentryargs):
        super().__init__(master, **kwentryargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.bind("<Key>", self.foc_in)
        
        self.isput = False
        
    def put_placeholder(self, *args):
        self.delete('0', 'end')
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.isput = True

    def quit_placeholder(self, *args):
        self.delete('0', 'end')
        self['fg'] = self.default_fg_color
        self.isput = False
    
    def foc_in(self, *args):
        if self.isput:
            self.quit_placeholder()

    def foc_out(self, *args):
        if not self.isput:
            if not self.get():
                self.put_placeholder()
                
    def grid(self, **kwargs):
        self.put_placeholder()
        super().grid(**kwargs)
        
        
class EntryWithListbox(tk.Entry):
    def __init__(self, master=None, options=tuple(), listboxkwargs={}, **kwentryargs):
        super().__init__(master, **kwentryargs)
        
        widthchange = 6/5
        
        self.listbox = tk.Listbox(master, width=int(round(self['width']*widthchange)), height=len(options), **listboxkwargs)
        
        self.listbox.bind('<<ListboxSelect>>', self.cambiar_estado)
        self.bind('<FocusOut>', lambda evt: self.listbox.grid_forget())
        
        self.options = options
        self.listbox.insert(1, *options)

    def changeopts(self, options=tuple()):
        self.options = options
        self.listbox.delete(0, "end")
        self.listbox.insert(1, *options)
    
    def cambiar_estado(self, evt):
        try: 
            index = int(evt.widget.curselection()[0])
            new = self.options[index]
            self.delete(0,"end")
            self.insert(0, new)
        except: pass
    
    def grid(self, **kwargs):
        if 'lbkw' in kwargs:
            lbkw = kwargs['lbkw']
            del kwargs['lbkw']
        else:
            lbkw = {}
        
        if 'side' in kwargs:
            side = kwargs['side']
            del kwargs['side']
        else:
            side = 'down'
        
        row = kwargs['row']
        column = kwargs['column']
        super().grid(**kwargs)
        
        if side not in ['n', 's', 'e', 'w', 'nw', 'ne', 'sw', 'se']:
            raise TypeError(f"Side '{side}' not expected; expected 'n', 's', 'e', 'w' ,'nw', ...")
        if 's' in side:
            row += 1
        if 'n' in side:
            row -= 1
        if 'w' in side:
            column -= 1
        if 'e' in side:
            column += 1
        
        self.bind('<FocusIn>', lambda evt:self.listbox.grid(row=row, column=column, **lbkw))
    
    def grid_forget(self):
        super().grid_forget()
        self.delete('0', 'end')
        self.listbox.grid_forget()

def login_button() -> None:
    err_code = mod.iniciar_sesion(path_register, login_varNombre.get(), login_varPass.get())
    if err_code == 1:
        login_labelAlarm.config(text=f"No está registrado el usuario o código: {login_varNombre.get()}")
        login_labelAlarm.grid(row=8)
    elif err_code == 2:
        login_labelAlarm.config(text="Contraseña Incorrecta")
        login_labelAlarm.grid(row=8)
    else:
        code = err_code
        login_labelAlarm.grid_forget()
        register_entryNombre.delete(0, "end")
        register_entryCodigo.delete(0, "end")
        register_entryCorreo.delete(0, "end")
        register_entryPass.delete(0, "end")
        login_entryNombre.delete(0, "end")
        login_entryPass.delete(0, "end")
        change_screen("register", code)

def register_button() -> None:
    err_code = mod.registrar_usuario(cts["Constants"]["correouni"], path_register, path_configs, register_varNombre.get(),
                                     register_varCodigo.get(), register_varCorreo.get(),
                                     register_varCorreo.get()[:register_varCorreo.get().find('@')],
                                     register_varPass.get())
    if err_code is None:
        code = register_varCodigo.get()
        register_labelAlarm.grid_forget()
        register_entryNombre.delete(0, "end")
        register_entryCodigo.delete(0, "end")
        register_entryCorreo.delete(0, "end")
        register_entryPass.delete(0, "end")
        login_entryNombre.delete(0, "end")
        login_entryPass.delete(0, "end")
        change_screen("register", code)
    elif err_code == 1:
        register_labelAlarm.config(text=f"El código '{register_varCodigo.get()}' ya se encuentra registrado")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 2:
        register_labelAlarm.config(text=f"El correo '{register_varCorreo.get()}' ya se encuentra registrado")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 3:
        register_labelAlarm.config(text=f"El usuario '{register_varCorreo.get()[:register_varCorreo.get().find('@')]}' ya se encuentra registrado")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 4:
        register_labelAlarm.config(text="Hubo errores al registrar el usuario: '{register_varCorreo.get()[:register_varCorreo.get().fin('@')]}'"
              +f" y el código: '{register_varCodigo.get()}'")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 5:
        register_labelAlarm.config(text=f"El correo debe tener el formato '{cts['Constants']['correouni']}'")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 6:
        register_labelAlarm.config(text=f"El código {register_varCodigo.get()} no parece ser un código de estudiante")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 7:
        register_labelAlarm.config(text=f"El usuario no puede ser un número, {register_varCorreo.get()[:register_varCorreo.get().find('@')]}"
              +" es un número")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 8:
        register_labelAlarm.config(text="Todos los campos deben estar llenados.")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 9:
        register_labelAlarm.config(text="El usuario del correo no es válido.")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 10:
        register_labelAlarm.config(text="El correo no es válido.")
        register_labelAlarm.grid(row=13, pady=20)
    elif err_code == 11:
        register_labelAlarm.config(text="La contraseña debe tener más de 5 dígitos.")
        register_labelAlarm.grid(row=13, pady=20)

def tryset(entname:str, alert:str) -> str:
    ent = globals()['opt_%s'%(entname)]
    var = globals()['%s'%(entname)]
    if ent['fg'] == "SystemWindowText" and var.get():
        return var.get()
    else:
        raise Exception(alert)

def command_agregar_materia():
    try:
        #Campos obligatorios
        nombre = tryset("entryNombreMateria", "El nombre de la materia debe ser llenado")
        assert not nombre.isdigit(), ("El nombre de la materia no puede ser un número")
        
        codigomt = tryset("entryCodigo", "El código de la materia debe ser llenado")
        
        creditos = tryset("entryCreditos", "Los créditos de la materia deben ser llenados")
        assert creditos.isdigit(), ("Los créditos deben ser un número")
        
        semestre = (tryset("entrySemestre1", "Ambos campos del semestre deben ser llenados"),)
        assert semestre[0].isdigit(), ("El primer campo de semestre debe ser un número")
        semestre += (tryset("entrySemestre2", "Ambos campos del semestre deben ser llenados"),)
        assert '-' in semestre[1], "El formato del segundo campo del semestre es erróneo"
        
        calif = tryset("entryCalif", "El modo de calificación debe ser llenado")
        assert calif in ("NUMERICO", "A/R", "NO CALIFICABLE"), (f"No existe el modo de calificación '{calif}'")
    except Exception as e:
        opt_alerta.config(text=e.args[0])
        opt_alerta.grid(row=5, column=6, columnspan=10)
        return 
    
    #Campos opcionales
    try:
        seccion = tryset("entrySeccion", "")
        assert seccion.isdigit(), ("La sección debe ser un número")
    except Exception as e:
        if e.args[0]:
            opt_alerta.config(text=e.args[0])
            opt_alerta.grid(row=5, column=6, columnspan=10)
            return
        seccion = ""
    try:
        profesor = (tryset("entryProfesor1", ""), )
        if entryProfesor2.get():
            profesor += (entryProfesor2.get(),)
    except Exception as e:
        if e.args[0]:
            opt_alerta.config(text=e.args[0])
            opt_alerta.grid(row=5, column=6, columnspan=10)
            return
        profesor = ()
    try:
        salon = (tryset("entrySalon1", ""), )
        if entrySalon2.get():
            salon += (entrySalon2.get(),)
    except Exception as e:
        if e.args[0]:
            opt_alerta.config(text=e.args[0])
            opt_alerta.grid(row=5, column=6, columnspan=10)
            return
        salon = ()
    
    horario = ()
    if chkLunes.get():
        horario += ("Lunes",)
    if chkMartes.get():
        horario += ("Martes",)
    if chkMiercoles.get():
        horario += ("Miércoles",)
    if chkJueves.get():
        horario += ("Jueves",)
    if chkViernes.get():
        horario += ("Viernes",)
    if chkSabado.get():
        horario += ("Sábado",)
    if chkDomingo.get():
        horario += ("Domingo",)
    
    opt_alerta.grid_forget()
    
    try:
        mod.agregar_materia(codigo, nombre, codigomt, seccion, creditos, semestre, profesor, 
                        salon, horario, calif)        
    except NameError as e:
        opt_alerta.config(text=e.args[0])
        opt_alerta.grid(row=5, column=6, columnspan=10)
        return
    except Exception as e2:
        raise e2
    
    subj = mod.cargar_materias(codigo)[nombre]
    add_subject(nombre, subj, mt_index=0)
    
    print("La materia '%s' ha sido agregada"%(nombre))
    actualizar_st()
    limpiar_st("clean opt", "hide opt")


def agregar_materia_bt():
    limpiar_st("clean opt")
        
    opt_quitar.grid(row=1, column=0, padx=20, pady=5, ipadx=5, ipady=5, rowspan=2)    
    
    opt_lblNombreMateria.grid(row=1, column=1)
    opt_entryNombreMateria.grid(row=2, column=1, padx=2)
    opt_lblCodigo.grid(row=1, column=2)
    opt_entryCodigo.grid(row=2, column=2, padx=2)
    opt_lblCreditos.grid(row=1, column=3)
    opt_entryCreditos.grid(row=2, column=3, padx=2)
    opt_lblSeccion.grid(row=1, column=4)
    opt_entrySeccion.grid(row=2, column=4, padx=2)
    
    opt_lblSemestre.grid(row=3, column=0)
    opt_entrySemestre1.grid(row=4, column=0, padx=2)
    opt_entrySemestre2.grid(row=5, column=0, padx=2, pady=2)
    opt_lblProfesores.grid(row=3, column=1)
    opt_entryProfesor1.grid(row=4, column=1, padx=2)
    opt_entryProfesor2.grid(row=5, column=1, padx=2, pady=2)
    opt_lblSalones.grid(row=3, column=2)
    opt_entrySalon1.grid(row=4, column=2, padx=2)
    opt_entrySalon2.grid(row=5, column=2, padx=2, pady=2)
    
    opt_lblCalif.grid(row=1, column=5)
    opt_entryCalif.grid(row=2, column=5, padx=2, lbkw={'rowspan':3}, side='s')
    
    #opt_lblEstado.grid(row=3, column=3, columnspan=2)
    #opt_entryEstado.grid(row=4, column=3, padx=2, columnspan=2, lbkw={'rowspan':3, "columnspan":2}, side='ne')
    #opt_entryEstado.config(state="normal")
    #opt_entryEstado.delete(0, "end")
    #opt_entryEstado.insert('0', "PENDIENTE")
    #opt_entryEstado.config(state="disabled")
    
    opt_lblHorario.grid(row=1, column=6, columnspan=7)
    opt_chkLunes.grid(row=2, column=6)
    opt_chkMartes.grid(row=2, column=7)
    opt_chkMiercoles.grid(row=2, column=8)
    opt_chkJueves.grid(row=2, column=9)
    opt_chkViernes.grid(row=2, column=10)
    opt_chkSabado.grid(row=2, column=11)
    opt_chkDomingo.grid(row=2, column=12)
    
    opt_buttonAgregar.grid(row=4, column=6, columnspan=10, ipadx=10)
    
    optframe.pack(fill="x", side="bottom")


def command_eliminar_materia(materia:str):
    mod.quitar_mt(codigo, materia)
    ct = 0
    for i in materias:
        if i[2] == materia:
            idx = ct
            
            del_subject(idx)
            return 
        ct += 1
    
    print(f"La materia '{materia}' ha sido eliminada")
    actualizar_st()
    limpiar_st("clean opt", "hide opt")

def command_agregar_nota(materia:str):
    if entrynota.get():
        try:
            newnota = eval(entrynota.get())
            opt_alerta.config(text="")
        except:
            opt_alerta.config(text="La nota debe ser un número, una operación (ej: 5/7) o  ir vacía")
            opt_alerta.grid(row=3, column=6)
            return
    else:
        newnota = ''
    
    if entrypctj.get():
        try:
            newpctj = eval(entrypctj.get())/100
            opt_alerta.config(text="")
        except:
            opt_alerta.config(text="El porcentaje debe ser un número, una operación (ej: 5/7) o  ir vacío")
            opt_alerta.grid(row=3, column=6)
            return
    else:
        newpctj = ''
    
    if entryconcep.get():
        newconcep = entryconcep.get()
    else:
        opt_alerta.config(text="El concepto de la nota no puede ir vacío")
        opt_alerta.grid(row=3, column=6)
        return
    
    mod.agregar_notas_mt(codigo, materia, (newnota, newpctj, newconcep))
    modify_subject(materia)
    
    print("La nota ha sido agregada")
    actualizar_st()
    limpiar_st("clean opt", "hide opt")

def agregar_nota_materia_bt(materia:str):
    limpiar_st("clean opt")
        
    font = ("",)
    #TODO: Personalizar color para cada materia.
    bgmat = mod.pastel(colors["silver"],1)
    
    opt_entrynota.delete(0,"end")
    opt_entrypctj.delete(0,"end")
    opt_entryconcep.delete(0,"end")
    
    opt_lblmat.config(text=materia, font=font, bg=bgmat)
    opt_lblmat.grid(row=1, column=1, padx=10, pady=10)
    
    opt_entrylblnota.grid(row=1, column=2, padx=10)
    opt_entrylblpctj.grid(row=1, column=3, padx=10)
    opt_entrylblconcep.grid(row=1, column=5, padx=10)
    
    opt_entrynota.grid(row=2, column=2, padx=5)
    opt_entrypctj.grid(row=2, column=3, padx=5)
    opt_lbljustpctj.grid(row=2, column=4)
    opt_entryconcep.grid(row=2, column=5, padx=5)
    
    opt_butfinalizar.config(command=partial(command_agregar_nota, materia))
    
    opt_butfinalizar.grid(row=2, column=6, padx=20)
    
    optframe.pack(fill="x", side="bottom")

def command_eliminar_nota(materia:str, indice:int):
    mod.quitar_nota_mt(codigo, materia, indice)
    modify_subject(materia)
    
    print("La nota ha sido eliminada")
    actualizar_st()
    limpiar_st("clean opt", "hide opt")

def command_editar_nota(materia:str, indice:int):
    if entrynota.get():
        try:
            newnota = eval(entrynota.get())
            opt_alerta.config(text="")
        except:
            opt_alerta.config(text="La nota debe ser un número, una operación (ej: 5/7) o  ir vacía")
            opt_alerta.grid(row=3, column=6)
            return
    else:
        newnota = ''
    
    if entrypctj.get():
        try:
            newpctj = eval(entrypctj.get())/100
            opt_alerta.config(text="")
        except:
            opt_alerta.config(text="El porcentaje debe ser un número, una operación (ej: 5/7) o  ir vacío")
            opt_alerta.grid(row=3, column=6)
            return 
    else:
        newpctj = ''
    
    if entryconcep.get():
        newconcep = entryconcep.get()
    else:
        opt_alerta.config(text="El concepto de la nota no puede ir vacío")
        opt_alerta.grid(row=3, column=6)
        return 
    
    mod.cambiar_nota_mt(codigo, materia, indice, newnota, newpctj, newconcep)
    modify_subject(materia)
    
    print("La nota ha sido cambiada")
    actualizar_st()
    limpiar_st("clean opt", "hide opt")

def editar_nota_materia_bt(materia:str, nota:float, pctj:float, concep:str, indice:int):
    limpiar_st("clean opt")
    
    font = ("",)
    #TODO: Personalizar color para cada materia.
    bgmat = mod.pastel(colors["silver"],1)
    
    opt_lblmat.config(text=materia, font=font, bg=bgmat)
    opt_lblmat.grid(row=1, column=1, padx=10, pady=10)
    
    opt_entrylblnota.grid(row=1, column=2, padx=10)
    opt_entrylblpctj.grid(row=1, column=3, padx=10)
    opt_entrylblconcep.grid(row=1, column=5, padx=10)
    
    opt_entrynota.delete(0,"end")
    opt_entrypctj.delete(0,"end")
    opt_entryconcep.delete(0,"end")
    
    opt_entrynota.insert(0,str(nota))
    opt_entrypctj.insert(0,str(pctj*100))
    opt_entryconcep.insert(0,str(concep))
    
    opt_entrynota.grid(row=2, column=2, padx=5)
    opt_entrypctj.grid(row=2, column=3, padx=5)
    opt_lbljustpctj.grid(row=2, column=4)
    opt_entryconcep.grid(row=2, column=5, padx=5)
    
    opt_butfinalizar.config(command=partial(command_editar_nota, materia, indice))
    opt_butfinalizar.grid(row=2, column=6, padx=20)

def mostrar_nota_bt(materia:str, nota:float, pctj:float, concep:str, indice:int):
    limpiar_st("clean opt")
        
    font = ("",)
    #TODO: Personalizar color para cada materia.
    bgmat = mod.pastel(colors["silver"],1) 
    bgnot = mod.pastel(colors["yellow"],2)
    bgconcep = mod.pastel(colors["red"],2)
    
    try:
        nota_txt = mod.centrar_texto(round(nota, 3), len("   x.xxx   "), True)
    except:
        nota_txt = mod.centrar_texto("Sin nota", 14, True)
    try:
        pctj_txt = mod.centrar_texto(str(round(pctj*100,2))+"%", len("   xx.xx%   "), False)
    except:
        pctj_txt = mod.centrar_texto("Sin Porcentaje", 14, True)
    
    opt_lblmat.config(text=materia, font=font, bg=bgmat)
    opt_lblnota.config(text="%s\n%s"%(nota_txt,pctj_txt) , font=font, bg=bgnot)
    opt_lblconcep.config(text=concep, font=font, bg=bgconcep)
    opt_lblmat.grid(row=1, column=1, padx=10)
    opt_lblnota.grid(row=1, column=2, padx=10, ipadx=5, ipady=5)
    opt_lblconcep.grid(row=1, column=3, padx=10, ipadx=5, ipady=5)
    
    opt_bteditar.config(command=partial(editar_nota_materia_bt, materia, nota, pctj, concep, indice))
    opt_bteditar.grid(row=1, column=4, padx=40, pady=20)
    
    opt_buteliminar.config(command=partial(command_eliminar_nota, materia, indice))
    opt_buteliminar.grid(row=1, column=7, padx=20)
    
    optframe.pack(fill="x", side="bottom")

def modify_subject(name:str):
    mts = mod.cargar_materias(codigo)
    ct = 0
    for i in materias:
        if i[2] == name:
            idx = ct
            
            del_subject(idx)                  #borrar
            add_subject(name, mts[name], idx) #agregar
            return 
        ct += 1
    raise NameError(f"En la lista materias no se encuentra la materia '{name}'")
    
def del_subject(index:int):
    for j in materias[index][0]:
        j.grid_forget()
    del materias[index]

def add_subject(name:str, subj:dict, mt_index:int=-1):
    if mt_index < 0:
        mt_index = len(materias)
    
    # 40 es el máximo espacio destinado para el nombre de la materia.
    mt_text = mod.centrar_texto(name, 40, True)
    
    #Opt1 - Simple Label
    #lbl = tk.Label(sbjframe, text=mt_text, font=("Consolas",10), bd=1, relief="sunken",
    #               bg=mod.pastel(colors["orange"],2))
    
    colorTF = color_semestre[(subj['Semestre'][0]-1)%len(color_semestre)]
    
    #colorTF = mod.pastel(colors["orange"],2)
    
    #Opt2 - Expandable Frame
    lbl = ToggledFrame(sbjframe, text=mt_text,  title_frame_opts={"font":("Consolas",10), "bd":1, "relief":"sunken",
                       "bg":colorTF}, bg=colorTF)
    
    sublabel1 = tk.Label(lbl.sub_frame, text=f"Código: {subj['Código']}")
    sublabel1.grid(row=0, column=0)
    
    sublabel2 = tk.Label(lbl.sub_frame, text=f"Créditos: {subj['Créditos']}")
    sublabel2.grid(row=0, column=1)
    
    sublabel3 = tk.Label(lbl.sub_frame, text=f"Semestre: {subj['Semestre'][1]}")
    sublabel3.grid(row=0, column=2)
    
    sublabel4 = tk.Label(lbl.sub_frame, text=f"Modo Calificación: {subj['Modo calificación']}")
    sublabel4.grid(row=1, column=0, columnspan=2)
    
    if subj['Horario'][0]:
        sublabel5 = tk.Label(lbl.sub_frame, text=','.join([i[:2].lower() for i in subj['Horario']]))
        sublabel5.grid(row=1, column=2)
    
    if subj['Salones'][0]:
        if len(subj['Salones']) > 1:
            sublabel6 = tk.Label(lbl.sub_frame, text=f"Salones: {' - '.join([str(i) for i in subj['Salones']])}")
            sublabel6.grid(row=2, column=0, columnspan=2)
        else:
            sublabel6 = tk.Label(lbl.sub_frame, text=f"Salón: {subj['Salones'][0]}")
            sublabel6.grid(row=2, column=0)
        
        subbutton1 = tk.Button(lbl.sub_frame, text="Eliminar", command=partial(command_eliminar_materia, name))
        subbutton1.grid(row=2, column=2)
    else:
        subbutton1 = tk.Button(lbl.sub_frame, text="Eliminar", command=partial(command_eliminar_materia, name))
        subbutton1.grid(row=2, column=1)
    
    pctj = round(subj['Porcentaje total'],4)
    if pctj == 1.0:
        perc_color = mod.pastel(colors["green"],3)
    elif pctj < 1.0:
        perc_color = mod.pastel(colors["brown"],1)
    else:
        perc_color = mod.pastel(colors["red"],1)
    perc_text = mod.centrar_texto(f"{pctj*100}% Completado", len("100.0% Completado"), True)        
    
    lblPerc = tk.Label(sbjframe, text=perc_text, bg=perc_color, font=("Consolas",8))
    
    nota = round(subj['Nota promedio'],2)
    if nota < 3:
        aver_color = mod.pastel(colors["red"],1)
    elif nota <= 3.25:
        aver_color = mod.pastel(colors["beaver"],0)
    elif nota <= 4:
        aver_color = mod.pastel(colors["yellow"],2)
    else:
        aver_color = mod.pastel(colors["beau blue"],0)
    
    aver_text = mod.centrar_texto(f"Promedio: {nota}", len("Promedio: x.xx"), True)
    lblAver = tk.Label(sbjframe, text=aver_text, bg=aver_color, font=("Consolas",8))
    
    modo = subj['Modo calificación']
    final = subj['Nota promedio']*subj['Porcentaje total']
    
    try:
        final = eval(subj['Cálculo total'], {'NP':final}, {})
    except:
        pass
    finally:
        final = round(final, 2)
    
    if modo == 'A/R':
        final = 'A' if final >= 3 else 'R'
        final_text = f"ND: {final}"
    elif modo == 'NO CALIFICABLE':
        final_text = '-'
    elif modo == 'NUMERICO':
        final_text = f"ND: {final}"
    final_text = mod.centrar_texto(final_text, len("ND: x.xx"))
    
    lblFinal = tk.Label(sbjframe, text=final_text, bg=mod.pastel(colors["magenta"],2), font=("Consolas",8))
    
    lst = [lbl, lblPerc, lblAver, lblFinal]
    
    grd_opts = [{}, {}, {}, {}]
    
    #máximos y mínimos de porcentajes de notas (para considerarse grandes)
    mn1, mn2, mn3 = 0.25, 0.2, 0.1
    try:
        notecolor = cts["Students"][codigo]["notecolor"]
        if notecolor[0] != "#":
            notecolor = colors[notecolor]
    except:
        notecolor = colors["green"]
    
    cc = 0
    for j in subj['Notas']:
        if type(j[0]) in (float, int):
            nt_text = mod.centrar_texto(f"{round(j[0],2)}", len("x.xx"), True)
            nt_fg = "SystemWindowText"
        elif type(j[0]) is str:
            nt_text = mod.centrar_texto(j[2], len("x.xx"), True)
            nt_fg = mod.pastel(colors["brown"],0)
        
        if type(j[1]) in (float, int):
            if j[1] >= mn1:
                nt_color = mod.pastel(notecolor,1)
            elif j[1] >= mn2:
                nt_color = mod.pastel(notecolor,2)
            elif j[1] >= mn3:
                nt_color = mod.pastel(notecolor,3)
            else:
                nt_color = mod.pastel(notecolor,4)
        elif type(j[1]) is str:
            nt_color = mod.pastel(notecolor,4)
        
        nt = tk.Button(sbjframe, text=nt_text, bg=nt_color, font=("Consolas",8),
                       command=partial(mostrar_nota_bt, name, *j, cc), fg=nt_fg)
        lst.append(nt)
        grd_opts.append({'sticky':'e'})
        
        cc += 1
    
    add_nt = tk.Button(sbjframe, text='+', command=partial(agregar_nota_materia_bt, name))
    
    lst.append(add_nt)
    grd_opts.append({})
    
    materias.insert(mt_index, (lst, grd_opts, name))

def actualizar_st():
    global mts
    data = mod.dar_usuario_y_demas(path_register, codigo)
    reload_constants(path_configs)
    mts = mod.cargar_materias(codigo)
    mts = mod.ordenar_mts_codigo(mts)
    mts = mod.ordenar_mts_semestre(mts)
    
    tm = time.localtime()
    #tm = time.struct_time((2021, 8, 11, 15, 49, 21, 0, 11, 0))
    actsemester = mod.semestre_actual(tm)
    
    try:
        bg_color = cts["Students"][codigo]["bg_color"]
        if bg_color[0] != "#":
            bg_color = colors[bg_color]
    except:
        bg_color = mod.pastel(colors["green"],4)
    
    pga, horas_pga, ssc, actualPGA, actualH = mod.info_PGA(mts, actsemester)
    
    #topframe
    top_mainlabel.config(text=data[0])
    top_general.config(text="General:")
    top_pgalabel.config(text=f"PGA: {round(pga,3)}")
    top_pgahourlabel.config(text=f"Horas PGA: {horas_pga}")
    top_ssclabel.config(text=f"SSC: {ssc}")
    top_actualsem.config(text=f"Periodo Actual ({actsemester}):")
    top_ASpga.config(text=f"Promedio: {round(actualPGA,3)}")
    top_ASpendingh.config(text=f"Créditos inscritos: {actualH}")
    
    top_mainlabel.grid(row=0, column=0, padx=5)
    top_general.grid(row=0, column=1, padx=10)
    top_pgalabel.grid(row=0, column=2, padx=5)
    top_pgahourlabel.grid(row=0, column=3, padx=5)
    top_ssclabel.grid(row=0, column=4, padx=5)
    top_actualsem.grid(row=0, column=5, padx=10)
    top_ASpga.grid(row=0, column=6, padx=5)
    top_ASpendingh.grid(row=0, column=7, padx=5)
    
    st_frame.config(bg=bg_color)
    
    sbjframe.config(bg=bg_color)
    sbjcanvas.config(bg=bg_color)
    
    st_agregar_mt_but.grid(row=0, column=0) 
    
    st_instruct.config(bg=bg_color)
    
    st_instruct.grid(row=0, column=1, columnspan=3, sticky='w')
    
    if len(materias) == 0:
        contmt = 0
        for i in mts:
            add_subject(i, mts[i])
            contmt += 1
    else:
        contmt = len(materias)
    
    row_cont = 1
    for i in materias:
        column_cont = 0
        # i[0] -> Lista con Widgets
        # i[1] -> Diccionario con kwargs para .grid()
        # i[2] -> Nombre de la materia
        for j in range(len(i[0])):
            i[0][j].grid(row=row_cont, column=column_cont, **i[1][j])
            column_cont += 1
                
        row_cont += 1
    
    try:
        sbjframe.columnconfigure(column_cont-1, weight=1)
    except:
        pass
    
    #mxrow_sub = 2
    #este Label tiene el fin de que se puedan expandir la mayoría de materias, mediante el Scrollbar
    #tk.Label(sbjframe, text="\n"*contmt*(mxrow_sub*2), bg=bg_color).grid(row=row_cont, column=0)
    
    st_frame.pack(fill="both", expand=True)
    

def change_screen(_from:str, _to:str) -> None:
    global codigo
    if _from == "register":
        if _to.isdigit():
            codigo = _to
            register.pack_forget()
            data = mod.dar_usuario_y_demas(path_register, codigo)
            print(f"Signed up as {data[0]}.")
            actualizar_st()
        else:
            raise Exception("An exception occured. The code charged is not a number.")
    elif _from.isdigit():
        if _to == "register":
            codigo = None
            limpiar_st("all")
            materias.clear()
            st_frame.pack_forget()
            register.pack()
    

def screen_root(master:tk.Tk, pad:int=3):
    master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
    
def switch_text(lbl:tk.Widget, newtxt:str, text2:str):
    if lbl['text'] == newtxt:
        lbl['text'] = text2
    else:
        lbl['text'] = newtxt

"""App"""

def reload_constants(path_constants:str) -> None:
    global cts
    cts = mod.cargar_constantes(path_constants)

""" Verifications and configs """
#Verificar que exista el documento de registros y de configuracion

try:
    k = open(path_register, 'r')
    k.close()
    del k
except:
    with open(path_register, 'w') as file:
        file.write("Nombre completo;Código;Correo;Usuario;Contraseña;Datos")
    del file

try:
    k = open(path_configs, 'r')
    k.close()
    del k
except:
    with open(path_configs, 'w') as file:
        file.write("Constants:\n"
                  +"    entryfont = 'Bookman Old Style' # Alguna fuente de word.\n"
                  +"    entryjustify = 'center' # 'left', 'right' o 'center'.\n"
                  +"    correouni = 'uniandes.edu.co' # Terminación correo universitario.\n"
                  +"    icodir = 'uniandes.ico' #Dirección del ícono de la universidad\n"
                  +"Students:")
    del file

#Inicializar Ventana

root = tk.Tk()
root.title("Matyno")
root.resizable(width=True, height=True)
screen_root(root, pad=100)

scrW = root.winfo_screenwidth()
scrH = root.winfo_screenheight()

#Configure constants
reload_constants(path_configs)

if "entryfont" not in cts["Constants"]:
    cts["Constants"]["entryfont"] = 'Bookman Old Style'
print(f"Entry font set to '{cts['Constants']['entryfont']}'")

if "entryjustify" not in cts["Constants"]:
    cts["Constants"]["entryjustify"] = 'center'
print(f"Entry justify set to '{cts['Constants']['entryjustify']}'")

if "icodir" not in cts["Constants"]:
    cts["Constants"]["icodir"] = ""
try:
    root.iconbitmap(cts["Constants"]["icodir"])
except:
    print(f"No iconbitmap at dir '{cts['Constants']['icodir']}'")

if "correouni" not in cts["Constants"]:
    cts["Constants"]["correouni"] = "gmail.com"


colors = mod.cargar_colores(path_colors, "hex")

color_semestre = [
    mod.pastel(colors["red"],2),
    mod.pastel(colors["green"],2),
    mod.pastel(colors["orange"],2)
    ]


""" Registro """

bg_register = mod.pastel(colors["blue"],3)
register = tk.Frame(root, bg=bg_register, bd=20, relief="sunken")

#arriba - mainlabel
subframe = tk.Frame(register, bg=bg_register)
tk.Label(subframe, text="Matyno", font=('Harlow Solid Italic', 40), bg=mod.pastel(colors["yellow"],3)
         ).pack(fill="x", padx=20, pady=20)
subframe.pack(side="top", fill="x")

#izquierda - registro
subframe = tk.Frame(register, bg=bg_register)
tk.Label(subframe, text="Registro", font=('Harlow Solid Italic', 30), bg=bg_register
         ).grid(row=0)
tk.Label(subframe, text="\nNombre", font=('Bahnschrift Light', 14), bg=bg_register
         ).grid(row=3)
tk.Label(subframe, text="\nCódigo de Universidad", font=('Bahnschrift Light', 14), 
         bg=bg_register
         ).grid(row=5)
tk.Label(subframe, text="\nCorreo de Universidad", font=('Bahnschrift Light', 14), 
         bg=bg_register
         ).grid(row=7)
tk.Label(subframe, text="\nContraseña", font=('Bahnschrift Light', 14), bg=bg_register
         ).grid(row=9)
tk.Label(subframe, text="No digite ninguna contraseña real\n", font=('Bahnschrift Light', 8), 
         bg=bg_register, fg=colors["gray"]
         ).grid(row=11)

register_varNombre = tk.StringVar()
register_varCodigo = tk.StringVar()
register_varCorreo = tk.StringVar()
register_varPass   = tk.StringVar()

register_entryNombre = tk.Entry(subframe, textvariable=register_varNombre, 
        width=45, font=(cts["Constants"]["entryfont"], 10), bd=2,
        justify=cts["Constants"]["entryjustify"])
register_entryCodigo = tk.Entry(subframe, textvariable=register_varCodigo, 
        width=45, font=(cts["Constants"]["entryfont"], 10), bd=2,
        justify=cts["Constants"]["entryjustify"])
register_entryCorreo = tk.Entry(subframe, textvariable=register_varCorreo, 
        width=45, font=(cts["Constants"]["entryfont"], 10), bd=2,
        justify=cts["Constants"]["entryjustify"])
register_entryPass = tk.Entry(subframe, textvariable=register_varPass, show="\u2022", 
        width=45, font=(cts["Constants"]["entryfont"], 10), bd=2,
        justify=cts["Constants"]["entryjustify"])

tk.Button(subframe, text="Registrar", font=('Harlow Solid Italic', 14), height=1, width=15,
          bg=mod.pastel(colors["green"],1), bd=4, command=register_button
          ).grid(row=12)

register_labelAlarm = tk.Label(subframe, fg=colors["red"], bg=bg_register)

register_entryNombre.grid(row=4)
register_entryCodigo.grid(row=6)
register_entryCorreo.grid(row=8)
register_entryPass.grid(row=10)

subframe.pack(side="left", fill="y",expand=True)

#derecha - login
subframe = tk.Frame(register, bg=bg_register)
tk.Label(subframe, text="Log In", font=('Harlow Solid Italic', 30), bg=bg_register
         ).grid(row=0)
tk.Label(subframe, text="\nCódigo, Correo o Usuario", font=('Bahnschrift Light', 14), 
         bg=bg_register
         ).grid(row=3)
tk.Label(subframe, text="\nContraseña", font=('Bahnschrift Light', 14), bg=bg_register
         ).grid(row=5)

subframe.pack(side="right", fill="y",expand=True)

login_varNombre = tk.StringVar()
login_varPass = tk.StringVar()

login_entryNombre = tk.Entry(subframe, textvariable=login_varNombre, bd=2,
        width=45, font=(cts["Constants"]["entryfont"], 10), 
        justify=cts["Constants"]["entryjustify"])
login_entryPass = tk.Entry(subframe, textvariable=login_varPass, show="\u2022", 
        width=45, font=(cts["Constants"]["entryfont"], 10), bd=2,
        justify=cts["Constants"]["entryjustify"])

tk.Button(subframe, text="Ingresar", font=('Harlow Solid Italic', 14), height=1, width=15,
          bg=mod.pastel(colors["purple"],1), bd=4, command=login_button
          ).grid(row=7, pady=20)

login_labelAlarm = tk.Label(subframe, fg=colors["red"], bg=bg_register)

login_entryNombre.grid(row=4)
login_entryPass.grid(row=6)

register.pack(fill="both", expand=True)

""" Pantalla Principal Estudiante """

st_frame = tk.Frame(root, bd=20, relief="sunken")

def limpiar_st(*command):
    """
    command = 'clean sbj', 'hide opt', 'hide sbj', ...
    
    Esta función corre los comandos 'clean', 'hide' y 'all':
        El comando clean borra todos los objetos del frame.
        El comando hide esconde de la vista el frame.
        El comando all realiza las operaciones que se describen debajo.
    """
    for i in command:
        if i == "all":
            limpiar_st("clean sbj", "clean top", "clean opt", "hide opt")
            return
        
        cmd, frm = i.split()
        if cmd == "clean":
            if frm == "top": #topframe
                top_mainlabel.grid_forget()
                top_general.grid_forget()
                top_pgalabel.grid_forget()
                top_pgahourlabel.grid_forget()
                top_ssclabel.grid_forget()
                top_actualsem.grid_forget()
                top_ASpga.grid_forget()
                top_ASpendingh.grid_forget()
                
                # toDelete
                for i in globals():
                    if i.startswith('top_'):
                        k = i.replace('top_','')
                        if k not in ['mainlabel', 'pgalabel', 'pgahourlabel', 'ssclabel', 'actualsem']:
                            print(f"PROGRAM ALERT topframe; object '{i}' not in 'limpiar_st'")
                
            elif frm == "sbj": #sbjframe
                st_agregar_mt_but.grid_forget()
                st_instruct.grid_forget()
                for i in materias:
                    for j in i[0]:
                        j.grid_forget()
                
            elif frm == "opt": #optframe
                #Always shown
                opt_quitar.grid(row=1, column=0, padx=20, pady=5, ipadx=5, ipady=5)   
                
                opt_alerta.grid_forget()
        
                #mostrar_nota_bt
                opt_lblmat.grid_forget()
                opt_lblnota.grid_forget()
                opt_lblconcep.grid_forget()
                opt_bteditar.grid_forget()
                
                #editar_nota_materia_bt
                opt_entrylblnota.grid_forget()
                opt_entrynota.grid_forget()
                opt_entrylblpctj.grid_forget()
                opt_entrypctj.grid_forget()
                opt_lbljustpctj.grid_forget()
                opt_entrylblconcep.grid_forget()
                opt_entryconcep.grid_forget()
                opt_butfinalizar.grid_forget()
                opt_buteliminar.grid_forget()
                
                #agregar_materia_bt
                opt_lblNombreMateria.grid_forget()
                opt_lblCodigo.grid_forget()
                opt_lblSeccion.grid_forget()
                opt_lblCreditos.grid_forget()
                opt_lblSemestre.grid_forget()
                opt_lblProfesores.grid_forget()
                opt_lblSalones.grid_forget()
                opt_lblHorario.grid_forget()
                opt_lblCalif.grid_forget()
                opt_lblEstado.grid_forget()
                opt_entryNombreMateria.grid_forget()
                opt_entryCodigo.grid_forget()
                opt_entrySeccion.grid_forget()
                opt_entryCreditos.grid_forget()
                opt_entrySemestre1.grid_forget()
                opt_entrySemestre2.grid_forget()
                opt_entryProfesor1.grid_forget()
                opt_entryProfesor2.grid_forget()
                opt_entrySalon1.grid_forget()
                opt_entrySalon2.grid_forget()
                opt_entryEstado.grid_forget()
                opt_chkLunes.grid_forget() ; opt_chkLunes.deselect() ; opt_chkLunes.config(bg=unselectcolor)
                opt_chkMartes.grid_forget() ; opt_chkMartes.deselect() ; opt_chkMartes.config(bg=unselectcolor)
                opt_chkMiercoles.grid_forget() ; opt_chkMiercoles.deselect() ; opt_chkMiercoles.config(bg=unselectcolor)
                opt_chkJueves.grid_forget() ; opt_chkJueves.deselect() ; opt_chkJueves.config(bg=unselectcolor)
                opt_chkViernes.grid_forget() ; opt_chkViernes.deselect() ; opt_chkViernes.config(bg=unselectcolor)
                opt_chkSabado.grid_forget() ; opt_chkSabado.deselect() ; opt_chkSabado.config(bg=unselectcolor)
                opt_chkDomingo.grid_forget() ; opt_chkDomingo.deselect() ; opt_chkDomingo.config(bg=unselectcolor)
                opt_entryCalif.grid_forget()
                opt_buttonAgregar.grid_forget()
                
                # toDelete
                for i in globals():
                    if i.startswith('opt_'):
                        k = i.replace('opt_','')
                        if k not in ['alerta', 'lblmat', 'lblnota', 'lblconcep', 'bteditar', 'entrylblnota',
                                     'entrynota', 'entrylblpctj', 'entrypctj', 'lbljustpctj', 'entrylblconcep',
                                     'entryconcep', 'butfinalizar', 'buteliminar', 'lblNombreMateria', 
                                     'lblCodigo', 'lblSeccion', 'lblCreditos', 'lblSemestre', 'lblProfesores',
                                     'lblSalones', 'lblHorario', 'lblCalif', 'lblEstado', 'entryNombreMateria',
                                     'entryCodigo','entrySeccion','entryCreditos','entrySemestre1','entrySemestre2',
                                     'entryProfesor1','entryProfesor2','entrySalon1','entrySalon2','entryEstado',
                                     'chkLunes', 'chkMartes', 'chkMiercoles', 'chkJueves', 'chkViernes', 'chkSabado',
                                     'chkDomingo', 'entryCalif', 'lboxCalif', 'lboxEstado', 'buttonAgregar'] and k != 'quitar':
                            print(f"PROGRAM ALERT optframe; object '{i}' not in 'limpiar_st'")
            
            else:
                raise NameError(f"No frame in st named {frm}")
        elif cmd == "hide":
            if frm == "top":
                topframe.pack_forget()
            elif frm == "sbj":
                sbjframe.pack_forget()
            elif frm == "opt": 
                optframe.pack_forget()
            else:
                raise NameError(f"No frame in st named '{frm}'")
        else:
            raise TypeError(f"No command recognized by '{cmd}'")

#Top Frame Student
topframe = tk.Frame(st_frame, bg=mod.pastel(colors["gray"], 1)) #mainframe

top_mainlabel = tk.Label(topframe, bg=topframe['bg'])
top_general = tk.Label(topframe, bg=topframe['bg'], font=("Bookman Old Style", 13, 'bold'))
top_pgalabel = tk.Label(topframe, bg=topframe['bg'])
top_pgahourlabel = tk.Label(topframe, bg=topframe['bg'])
top_ssclabel = tk.Label(topframe, bg=topframe['bg'])
top_actualsem = tk.Label(topframe, bg=topframe['bg'], font=("Bookman Old Style", 12, 'bold'))
top_ASpga = tk.Label(topframe, bg=topframe['bg'])
top_ASpendingh = tk.Label(topframe, bg=topframe['bg'])

#Subjects Frame Student

subframe = tk.Frame(st_frame)
sbjcanvas = tk.Canvas(subframe)
sbjcanvas.pack(side="left", fill="both", expand=True)

yscrollbar = tk.Scrollbar(subframe, orient="vertical", command=sbjcanvas.yview)
yscrollbar.pack(side="right", fill="y")

sbjcanvas.config(yscrollcommand=yscrollbar.set)

def sbjcanvas_configure(event):
    sbjcanvas.config(scrollregion=sbjcanvas.bbox("all"))
    sbjframe.config(width=event.width)
    #sbjcanvas.itemconfigure("sbjframe", width=event.width)

sbjframe = tk.Frame(sbjcanvas) #mainframe

sbjcanvas.create_window((0,0), window=sbjframe, anchor="nw")
sbjcanvas.bind('<Configure>', sbjcanvas_configure)

st_agregar_mt_but = tk.Button(sbjframe, text='  Agregar Materia  +  ',
                                  command=agregar_materia_bt)

st_instruct = tk.Label(sbjframe, text="*ND = Nota Definitiva (sobre 100%)", #": 'A' (Aprobado), 'R' (Reprobado), '-' (Sin Nota)",
                       font=("Consolas",10))

#Options Frame Student
optframe = tk.Frame(st_frame, bg=mod.pastel(colors["gray"],2))

#   Generales
opt_quitar = tk.Button(optframe, text="Quitar Selección", bg=mod.pastel(colors["brown"],1),
                       command=partial(limpiar_st, "clean opt", "hide opt") )
opt_alerta = tk.Label(optframe, fg=colors["red"], bg=optframe["bg"], text="")

#   Widgets for mostrar_nota_bt
opt_lblmat = tk.Label(optframe)
opt_lblnota = tk.Label(optframe)
opt_lblconcep = tk.Label(optframe)
opt_bteditar = tk.Button(optframe, text="Editar")

#   Widgets for editar_nota_materia_bt y agregar_nota_materia_bt
opt_entrylblnota = tk.Label(optframe, text="Nota", bg=optframe["bg"])
entrynota = tk.StringVar(optframe)
opt_entrynota = tk.Entry(optframe, textvariable=entrynota, font=(cts["Constants"]["entryfont"], 10), 
        justify=cts["Constants"]["entryjustify"])

opt_entrylblpctj = tk.Label(optframe, text="Porcentaje", bg=optframe["bg"])
entrypctj = tk.StringVar(optframe)
opt_entrypctj = tk.Entry(optframe, textvariable=entrypctj, font=(cts["Constants"]["entryfont"], 10), 
        justify=cts["Constants"]["entryjustify"])
opt_lbljustpctj = tk.Label(optframe, text="%", bg=optframe["bg"])

opt_entrylblconcep = tk.Label(optframe, text="Concepto", bg=optframe["bg"])
entryconcep = tk.StringVar(optframe)
opt_entryconcep = tk.Entry(optframe, textvariable=entryconcep, font=(cts["Constants"]["entryfont"], 10), 
        justify=cts["Constants"]["entryjustify"])

opt_butfinalizar = tk.Button(optframe, text="Finalizar")

opt_buteliminar = tk.Button(optframe, text="Eliminar nota")

# Widgets for agregar_materia_bt
opt_lblNombreMateria = tk.Label(optframe, text="*Nombre materia", bg=optframe["bg"])
opt_lblCodigo = tk.Label(optframe, text="*Código", bg=optframe["bg"])
opt_lblSeccion = tk.Label(optframe, text="Sección", bg=optframe["bg"])
opt_lblCreditos = tk.Label(optframe, text="*Créditos", bg=optframe["bg"])
opt_lblSemestre = tk.Label(optframe, text="*Semestre", bg=optframe["bg"])
opt_lblProfesores = tk.Label(optframe, text="Profesores", bg=optframe["bg"])
opt_lblSalones = tk.Label(optframe, text="Salones", bg=optframe["bg"])
opt_lblHorario = tk.Label(optframe, text="Horario", bg=optframe["bg"])
opt_lblCalif = tk.Label(optframe, text="*Modo Calificación", bg=optframe["bg"])
opt_lblEstado = tk.Label(optframe, text="Estado", bg=optframe["bg"])

entryNombreMateria = tk.StringVar(optframe)
opt_entryNombreMateria = EntryWithPlaceholder(optframe, placeholder="Introducción a Física", color='grey', width=36,
        textvariable=entryNombreMateria, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entryCodigo = tk.StringVar(optframe)
opt_entryCodigo = EntryWithPlaceholder(optframe, placeholder="FISI 1502", color='grey', width=12, 
        textvariable=entryCodigo, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entryCreditos = tk.StringVar(optframe)
opt_entryCreditos = EntryWithPlaceholder(optframe, placeholder="3", color='grey', width=2, 
        textvariable=entryCreditos, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entrySeccion = tk.StringVar(optframe)
opt_entrySeccion = EntryWithPlaceholder(optframe, placeholder="1", color='grey', width=2, 
        textvariable=entrySeccion, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entryCalif = tk.StringVar(optframe)
opt_entryCalif = EntryWithListbox(optframe,("NUMERICO", "A/R", "NO CALIFICABLE"), textvariable=entryCalif, 
        font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"], width=15)


selectcolor = mod.pastel(colors["red"],2)
unselectcolor = mod.pastel(colors["green"],3)

#Horario
chkLunes = tk.BooleanVar(optframe)
opt_chkLunes = tk.Checkbutton(optframe, text='Lun', variable=chkLunes, onvalue=True, offvalue=False,
            activebackground=mod.pastel(colors["blue"],1), bg=unselectcolor,
            command=lambda: opt_chkLunes.config(bg=selectcolor if chkLunes.get() else unselectcolor))
chkMartes = tk.BooleanVar(optframe)
opt_chkMartes = tk.Checkbutton(optframe, text='Mar', variable=chkMartes, onvalue=True, offvalue=False,
            activebackground=mod.pastel(colors["blue"],1), bg=unselectcolor,
            command=lambda: opt_chkMartes.config(bg=selectcolor if chkMartes.get() else unselectcolor))
chkMiercoles = tk.BooleanVar(optframe)
opt_chkMiercoles = tk.Checkbutton(optframe, text='Mie', variable=chkMiercoles, onvalue=True, offvalue=False,
            activebackground=mod.pastel(colors["blue"],1), bg=unselectcolor,
            command=lambda: opt_chkMiercoles.config(bg=selectcolor if chkMiercoles.get() else unselectcolor))
chkJueves = tk.BooleanVar(optframe)
opt_chkJueves = tk.Checkbutton(optframe, text='Jue', variable=chkJueves, onvalue=True, offvalue=False,
            activebackground=mod.pastel(colors["blue"],1), bg=unselectcolor,
            command=lambda: opt_chkJueves.config(bg=selectcolor if chkJueves.get() else unselectcolor))
chkViernes = tk.BooleanVar(optframe)
opt_chkViernes = tk.Checkbutton(optframe, text='Vie', variable=chkViernes, onvalue=True, offvalue=False,
            activebackground=mod.pastel(colors["blue"],1), bg=unselectcolor,
            command=lambda: opt_chkViernes.config(bg=selectcolor if chkViernes.get() else unselectcolor))
chkSabado = tk.BooleanVar(optframe)
opt_chkSabado = tk.Checkbutton(optframe, text='Sab', variable=chkSabado, onvalue=True, offvalue=False,
            activebackground=mod.pastel(colors["blue"],1), bg=unselectcolor,
            command=lambda: opt_chkSabado.config(bg=selectcolor if chkSabado.get() else unselectcolor))
chkDomingo = tk.BooleanVar(optframe)
opt_chkDomingo = tk.Checkbutton(optframe, text='Dom', variable=chkDomingo, onvalue=True, offvalue=False,
            activebackground=mod.pastel(colors["blue"],1), bg=mod.pastel(colors["green"],3),
            command=lambda: opt_chkDomingo.config(bg=mod.pastel(colors["red"],2) if chkDomingo.get() else mod.pastel(colors["green"],3)))


entrySemestre1 = tk.StringVar(optframe)
opt_entrySemestre1 = EntryWithPlaceholder(optframe, placeholder="1", color='grey', width=2, 
        textvariable=entrySemestre1, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entrySemestre2 = tk.StringVar(optframe)
opt_entrySemestre2 = EntryWithPlaceholder(optframe, placeholder="2020-10A", color='grey', width=9, 
        textvariable=entrySemestre2, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entryProfesor1 = tk.StringVar(optframe)
opt_entryProfesor1 = EntryWithPlaceholder(optframe, placeholder="Camilo Pérez", color='grey', width=34,
        textvariable=entryProfesor1, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entryProfesor2 = tk.StringVar(optframe)
opt_entryProfesor2 = EntryWithPlaceholder(optframe, placeholder="", color='grey', width=34, 
        textvariable=entryProfesor2, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entrySalon1 = tk.StringVar(optframe)
opt_entrySalon1 = EntryWithPlaceholder(optframe, placeholder="ML 109", color='grey', width=9, 
        textvariable=entrySalon1, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entrySalon2 = tk.StringVar(optframe)
opt_entrySalon2 = EntryWithPlaceholder(optframe, placeholder="", color='grey', width=9,
        textvariable=entrySalon2, font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"])

entryEstado = tk.StringVar(optframe)

opt_entryEstado = EntryWithListbox(optframe, ("PENDIENTE", "RETIRADA"), textvariable=entryEstado, 
        font=(cts["Constants"]["entryfont"], 10), justify=cts["Constants"]["entryjustify"],width=10)

opt_buttonAgregar = tk.Button(optframe, text= "Agregar", bg=mod.pastel(colors["pink"],1), 
                              command=command_agregar_materia)


#materias de Subjects Frame Student
materias = []

#bbutton_image = tk.PhotoImage(master=st_subframe1, file=path_back_image)
#st_back_button = tk.Button(st_subframe1, image=bbutton_image, height=50, width=50)

topframe.pack(side="top", fill="x")

subframe.pack(side="top", fill="both", expand=True)
#sbjframe.pack(fill="both", expand=True)

#optframe.pack(side="top", fill="both", expand=True)

""" MAINLOOP """

root.mainloop()


"""
root = tk.Tk()
cts = mod.cargar_constantes(path_configs)

wd1 = Window("grid", root)

wd1.add(tk.Label, "lbl1", text="Label")
wd1.set_put_args("lbl1", "place")
wd1.add(tk.Button, "but1", text="button?")
wd1.set("but1", "grid")
wd1.add(tk.Button, "but2", text="clear")
wd1.set_put_args("but2", "grid")


wd1.but1['command'] = partial(switch_text, wd1.but2, "WTF?", wd1.but2['text'])
wd1.but2['command'] = partial(wd1.forget)
wd1.put(True)

root.mainloop()
"""