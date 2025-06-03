import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas



#---------------------------------------------- clases
class Usuario:
    def __init__(self,nombre = "Primer nombre",apellido = "Primer apellido",cedula = "cedula",ref = "referencia"):
        self.setNombre(nombre)
        self.setApellido(apellido)
        self.setCedula(cedula)
        self.setReferencia(ref)
        self.__verificado = "No"
        self.__fecha = "0/0/0"
        self.__monto = "--"
    def setMonto(self,monto):
        self.__monto = monto
    def setNombre(self,nombre):
        self.__nombre = nombre
    def setApellido(self,apellido):
        self.__apellido = apellido
    def setCedula(self,cedula):
        self.__cedula = cedula
    def setReferencia(self,ref):
        self.__Referencia = ref
    def setVerificado(self,status):
        self.__verificado = status
    def setFecha(self,fecha):
        self.__fecha = fecha
    def getNombre(self):
        return self.__nombre
    def getApellido(self):
        return self.__apellido
    def getCedula(self):
        return self.__cedula
    def getReferencia(self):
        return self.__Referencia
    def getVerificado(self):
        return self.__verificado
    def getFecha(self):
        return self.__fecha
    def getMonto(self):
        return self.__monto

#-------------------------------------------------------------------- funciones

def instanciaClaseUsuario(index_banco,index_usuario,df_banco,df_potrero,v = 1):
    nombre = df_potrero["Nombre"][index_usuario]
    apellido = df_potrero["Apellido"][index_usuario]
    cedula = df_potrero["Cedula"][index_usuario]
    if v == 1:
        referencia = df_banco["Referencia"][index_banco]
    else:
        referencia = df_potrero["Referencias"][index_usuario]
    return Usuario(nombre,apellido,cedula,referencia)

def verficacionMonto(index_banco,df_banco,precio):
    if df_banco["Credito"][index_banco] == precio:
        monto = "Correcto"
    elif df_banco["Credito"][index_banco] > precio:
        monto = "Sobran: {}".format(df_banco["Credito"][index_banco] - precio)
    else:
        monto = "Faltan: {}".format(precio - df_banco["Credito"][index_banco])
    return monto

def usuariosConReferenciasRepetidas(df_potrero,df_banco):
    ref_p = {}
    lista = []
    global df_usuarios
    for i in range(len(df_potrero["Referencias"])):
        if str(df_potrero["Referencias"][i]) in ref_p:
            ref_p[str(df_potrero["Referencias"][i])] += 1
        else:
            ref_p[str(df_potrero["Referencias"][i])] = 1
    for h in ref_p:
        print(ref_p)
        count = 0   #i - count --> de esa forma la lista no se sale de rango
        for i in range(len(df_potrero["Referencias"])):
            if str(df_potrero["Referencias"][i-count]) == h and ref_p[h] >= 2:
                indice = 0
                # me traigo el indice de la referencia del otro archivo
                for j in range(len(df_banco["Referencia"])):
                    if h == str(df_banco["Referencia"][j])[-4:]:
                        indice = j
                user = instanciaClaseUsuario(indice,i-count,df_banco,df_potrero)
                user.setVerificado("Repetido")
                lista.append(user)
                #Elimino las filas de mi dataFrame que contienen las refrencias repetidas
                df_potrero = df_potrero.drop([i-count],axis = 0).reset_index(drop =True)
                count += 1
    # variable global para poder modificarla dentro de la funcion
    df_usuarios = df_potrero
    return lista
def comprobacionDePago(indice_potrero,df_banco,df_potrero):
    global precio
    for j in range(len(df_banco)):
        if int(str(df_banco["Referencia"][j])[-4:]) == df_potrero["Referencias"][indice_potrero]:
            user = instanciaClaseUsuario(j,indice_potrero,df_banco,df_usuarios)
            user.setVerificado("Si")
            user.setMonto(verficacionMonto(j,df_banco,precio))
            user.setFecha(df_banco["Fechas"][j])
            return user
    return instanciaClaseUsuario(True,indice_potrero,df_banco,df_usuarios,0)
#---------------------funciones para exportar pdf
def exportar_para_pdf(lista_de_usuarios_con_referencias_repetidas, lista_de_usuarios_confirmados, lista_de_usuarios_no_confirmados, nome_arquivo="resumo_pagamentos.pdf"):
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    width, height = A4
    margem = 50
    linha_atual = height - 40
    espacamento = 15

    def escrever_titulo(titulo):
        nonlocal linha_atual
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margem, linha_atual, titulo)
        linha_atual -= espacamento

    def escrever_usuario(usuario):
        nonlocal linha_atual
        if linha_atual < 60:
            c.showPage()
            linha_atual = height - 40
        texto = f"{usuario.getNombre()} {usuario.getApellido()} - C.I: {usuario.getCedula()} | Ref: {usuario.getReferencia()} | Verificado: {usuario.getVerificado()} | Data: {usuario.getFecha()} | Valor: {usuario.getMonto()}"
        c.setFont("Helvetica", 10)
        c.drawString(margem, linha_atual, texto)
        linha_atual -= espacamento
    escrever_titulo("Usuários com Referência Repetida:")
    for u in lista_de_usuarios_con_referencias_repetidas:
        escrever_usuario(u)

    linha_atual -= espacamento
    escrever_titulo("Usuários Confirmados:")
    for u in lista_de_usuarios_confirmados:
        escrever_usuario(u)

    linha_atual -= espacamento
    escrever_titulo("Usuários Não Confirmados:")
    for u in lista_de_usuarios_no_confirmados:
        escrever_usuario(u)
    c.save()
    print(f"PDF gerado com sucesso: {nome_arquivo}")



# -----------------------------------------------------------------------variables generales
precio = int(input("Ingrese el precio del producto: "))
archivo_del_banco = input("Ingrese el nombre del archivo del banco: ")
archivo_de_usuarios = input("Ingrese el nombre del archivo del banco: ")

#---------------------------------------------------------------------------- codigo del programa

# lectura de los documentos y creacion de los Dataframe
doc_mercantil = pd.read_excel(archivo_del_banco + "Agosto2020.xlsx",header=None,names = ["Fechas","Descripcion","Referencia","Debito","Credito"])
doc_usuarios = pd.read_excel(archivo_de_usuarios + "Potrero.xlsx",names= ["Fecha","Nombre","Apellido","Cedula","Referencias"])
df_usuarios = pd.DataFrame(doc_usuarios)
df_mercantil = pd.DataFrame(doc_mercantil)

lista_de_usuarios_con_referencias_repetidas = usuariosConReferenciasRepetidas(df_usuarios,df_mercantil)
lista_de_usuarios_confirmados = []
lista_de_usuarios_no_confirmados = []
print(df_mercantil)
for i in range(len(df_usuarios)):
    objeto_usuario = comprobacionDePago(i,df_mercantil,df_usuarios)
    if (objeto_usuario.getVerificado() == "Si"):
        lista_de_usuarios_confirmados.append(objeto_usuario)
    else:
        lista_de_usuarios_no_confirmados.append(objeto_usuario)


exportar_para_pdf(lista_de_usuarios_con_referencias_repetidas,lista_de_usuarios_confirmados,lista_de_usuarios_no_confirmados)

