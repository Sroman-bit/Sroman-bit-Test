import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("Encuesta de Actualizacion de Datos ANEIAP Uninorte")
st.markdown("Llena los espacios con tu información personal")

conn = st.experimental_connection("gsheets", type = GSheetsConnection)
existing_data = conn.read(worksheet = "Hoja", usecols = list(range(16)), ttl=5)
existing_data = existing_data.dropna(how = "all")
Direccion = ["ACADÉMICO","COMUNICACIONES","DESARROLLO","FINANZAS","MERCADEO"]
Carne = ["SI","NO",]
Carrera = ["ING. INDUSTRIAL","ING. ADMINISTRATIVA","ING. PRODUCCIÓN"]
RH = ["O-","O+","A−","A+","B−","B+","AB−","AB+"]
Semestre = ["I","II","III","IV","V","VI","VII","VIII","IX","X"]
Tipo_Documento = [ "C.C","T.I"]

with st.form(key = "data_base"):
    numero_dentificacion = st.text_input(label = "IDENTIFICACIÓN")
    documento = st.multiselect("TIPO DE DOCUMENTO", options = Tipo_Documento)
    nombres = st.text_input(label = "NOMBRES")
    apellidos = st.text_input(label = "APELLIDOS")
    nacimiento = st.sidebar.date_input(label = "FECHA DE NACIMIENTO")
    semestre_academico = st.multiselect("SEMESTRE", options = Semestre)
    direccion_perteneciente = st.multiselect("DIRECCIÓN A LA QUE PERTENECE", options = Direccion)
    telefono = st.text_input(label = "CELULAR")
    correo = st.text_input(label = "CORREO CORPORATIVO")
    semestre_ingreso = st.text_input(label = "SEMESTRE DE INGRESO A ANEIAP (20XX-X)")
    carne_o_no = st.multiselect("¿TIENE CARNÉ? ", options = Carne)
    carrera_iap = st.multiselect("CARRERA IAP", options = Carrera)
    tipo_sangre = st.multiselect("TIPO DE SANGRE ", options = RH)
    
    st.markdown("*Cada campo de esta encuesta es obligatorio de llenar, se agradece asociad@ por su colaboración.*")
    
    submit_botton = st.form_submit_button(label = "Subir información")
    if submit_botton:
        if not numero_dentificacion or not documento or not nombres or not apellidos or not nacimiento or not semestre_academico or not direccion_perteneciente or not telefono or not correo or not semestre_ingreso or not carne_o_no or not carrera_iap or not carrera_iap or not tipo_sangre:
          st.warning("Todos los campos de esta encuesta deben ser llenados, revise por favor que asi sea el caso.")
          st.stop
        
        else:
          data_base = pd.DataFrame (
              {
                  "IDENTIFICACIÓN" : numero_dentificacion,
                  "TIPO DE DOCUMENTO": documento,
                  "NOMBRES": nombres,
                  "APELLIDOS" : apellidos,
                  "FECHA DE NACIMIENTO": nacimiento.strtime("%Y-%m-%d"),
                  "SEMESTRE": semestre,
                  "DIRECCIÓN A LA QUE PERTENECE": direccion_perteneciente,
                  "CELULAR": telefono,
                  "CORREO COPORATIVO": correo,
                  "SEMESTRE DE INGRESO A ANEIAP (20XX-X)": semestre_ingreso,
                  "TIENE CARNÉ": carne_o_no,
                  "CARRERA": carrera_iap,
                  "RH": tipo_sangre,
              }
          )
          data_frame_actualizado = pd.concat([existing_data,data_base], ignore_index = True)
          conn.update(worksheet = "Hoja", data = data_frame_actualizado)
          st.sucess("Se ha subido exitosamente su información a la base de datos capitular")
