import xlrd
import xlwt
class User:
    def __init__(self,nombre = "Primer nombre",apellido = "Primer apellido",cedula = "cedula",ref = "referencia"):
        self.setNombre(nombre)
        self.setApellido(apellido)
        self.setCedula(cedula)
        self.setReferencia(ref)
        self.__verificado = "No"
        self.__fecha = "0/0/0"
        self.__monto = "Cero"
    def setMonto(self,monto):
        self.__monto = monto
    def setNombre(self,nombre):
        self.__nombre = str(nombre)
    def setApellido(self,apellido):
        self.__apellido = str(apellido)
    def setCedula(self,cedula):
        self.__cedula = str(int(cedula))
    def setReferencia(self,ref):
        self.__Referencia = str(int(ref))
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

class DatosTransferencia:
    def __init__(self,fecha = "00/00/00",referencia = "123456",monto = "150000"):
        self.setFecha(fecha)
        self.setReferencia(referencia)
        self.setMonto(monto)
    def setFecha(self,fecha):
        self.__fecha = str(int(fecha))
    def setReferencia(self,referencia):
        self.__referencia = referencia[len(referencia)-4::]
    def setMonto(self,monto):
        self.__monto = monto
    def getFecha(self):
        return self.__fecha
    def getReferencia(self):
        return self.__referencia
    def getMonto(self):
        return self.__monto

def datos_bancarios(folder):
    transferencias = []
    for i in range(folder.nrows):
        fecha = folder.cell_value(i,0)
        referencia = str(int(folder.cell_value(i,2)))
        monto = folder.cell_value(i,4).split(".")[0]
        transferencias.append(DatosTransferencia(fecha,referencia,monto))
    return transferencias

def datos_users(datos):
    vecinos = []
    for i in range(1,datos.nrows):
        nombre = datos.cell_value(i,1)
        apellido = datos.cell_value(i,2)
        cedula = datos.cell_value(i,3)
        referencia = datos.cell_value(i,4)
        vecinos.append(User(nombre,apellido,cedula,referencia))
    return vecinos


opend_document = xlrd.open_workbook("Agosto2020.xlsx")
folder = opend_document.sheet_by_name("Agosto2020")

opend_data = xlrd.open_workbook('Potrero.xlsx')
datos_a_verificar = opend_data.sheet_by_name("Respuestas de formulario 1")

lista_de_transferencias = datos_bancarios(folder)
lista_de_vecinos = datos_users(datos_a_verificar)

precio_bolsa = 150000
for i in lista_de_vecinos:
    for j in lista_de_transferencias:
        if i.getReferencia() == j.getReferencia():
            i.setVerificado("Si")
            i.setFecha(j.getFecha())
            if int(j.getMonto()) == precio_bolsa:
                i.setMonto("Exacto")
            elif int(j.getMonto()) > precio_bolsa:
                i.setMonto("Sobran {} ".format(int(j.getMonto())-precio_bolsa))
            else:
                i.setMonto("Faltan {}".format(precio_bolsa - int(j.getMonto())))
            lista_de_transferencias.pop(lista_de_transferencias.index(j))
referencias_repetidas = {}
for i in lista_de_vecinos:
    if i.getReferencia() not in referencias_repetidas:
        referencias_repetidas[i.getReferencia()] = 1
    else:
        referencias_repetidas[i.getReferencia()] += 1
referencias_en_conflicto = []
for i in referencias_repetidas:
    for j in lista_de_vecinos:
        if referencias_repetidas[i] >= 2 and i == j.getReferencia():
            j.setVerificado("Conflicto")
            referencias_en_conflicto.append(j)
print()
print("Referencias en conflicto")
print()
for i in referencias_en_conflicto:
    print(i.getNombre() + " " + i.getApellido() + " " + i.getCedula() + " " + i.getReferencia() + " " + str(i.getVerificado()))


print()
print("Referencias confirmadas")
print()
for i in lista_de_vecinos:
    if i.getVerificado() == "Si":
        print(i.getNombre() + " " + i.getApellido() + " " + i.getCedula() + " " + i.getReferencia() + " " + str(i.getVerificado()) + " " + i.getMonto() )
print()
print("Referencias no confirmados")
print()
for i in lista_de_vecinos:
    if i.getVerificado() == "No":
        print(i.getNombre() + " " + i.getApellido() + " " + i.getCedula() + " " + i.getReferencia() + " " + str(i.getVerificado()))


print()
print("Referencias por Confirmar")
print()
for i in lista_de_transferencias:
    print(i.getReferencia())


archivo_excel = xlwt.Workbook()
hoja_excel = archivo_excel.add_sheet("Potrero del medio")


hoja_excel.write(0,1,"Referencias en conflictos")
hoja_excel.write(1,0,"Nombre")
hoja_excel.write(1,1,"Apellido")
hoja_excel.write(1,2,"Cedula")
hoja_excel.write(1,3,"Referencia")
hoja_excel.write(1,4,"Verificacion")
numero_linea = 2
for i in referencias_en_conflicto:
    hoja_excel.write(numero_linea,0,i.getNombre())
    hoja_excel.write(numero_linea,1,i.getApellido())
    hoja_excel.write(numero_linea,2,i.getCedula())
    hoja_excel.write(numero_linea,3,i.getReferencia())
    hoja_excel.write(numero_linea,4,i.getVerificado())
    numero_linea += 1


numero_linea += 5
hoja_excel.write(numero_linea-3,1,"Referencias confirmadas")
hoja_excel.write(numero_linea-1,0,"Nombre")
hoja_excel.write(numero_linea-1,1,"Apellido")
hoja_excel.write(numero_linea-1,2,"Cedula")
hoja_excel.write(numero_linea-1,3,"Referencia")
hoja_excel.write(numero_linea-1,4,"Verificacion")
hoja_excel.write(numero_linea-1,5,"Monto")
for i in lista_de_vecinos:
    if i.getVerificado() == "Si":
        hoja_excel.write(numero_linea,0,i.getNombre())
        hoja_excel.write(numero_linea,1,i.getApellido())
        hoja_excel.write(numero_linea,2,i.getCedula())
        hoja_excel.write(numero_linea,3,i.getReferencia())
        hoja_excel.write(numero_linea,4,i.getVerificado())
        hoja_excel.write(numero_linea,5,i.getMonto())
        numero_linea += 1

numero_linea += 5
hoja_excel.write(numero_linea-3,1,"Referencias no confirmadas")
hoja_excel.write(numero_linea-1,0,"Nombre")
hoja_excel.write(numero_linea-1,1,"Apellido")
hoja_excel.write(numero_linea-1,2,"Cedula")
hoja_excel.write(numero_linea-1,3,"Referencia")
hoja_excel.write(numero_linea-1,4,"Verificacion")

for i in lista_de_vecinos:
    if i.getVerificado() == "No":
        hoja_excel.write(numero_linea,0,i.getNombre())
        hoja_excel.write(numero_linea,1,i.getApellido())
        hoja_excel.write(numero_linea,2,i.getCedula())
        hoja_excel.write(numero_linea,3,i.getReferencia())
        hoja_excel.write(numero_linea,4,i.getVerificado())
        numero_linea += 1
archivo_excel.save("Resumen_potrero_del_medio.xls")
