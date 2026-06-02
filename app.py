import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="Encuesta OCAI",
    layout="wide"
)

# ==========================================
# CONTROL DE ENVÍO
# ==========================================

if "encuesta_enviada" not in st.session_state:
    st.session_state.encuesta_enviada = False

# Si ya fue enviada, mostrar solo agradecimiento

if st.session_state.encuesta_enviada:

    st.success(
        "Gracias por participar de la encuesta."
    )
    st.markdown(
            """
            Puede cerrar esta ventana.
           """
    )

    st.stop()


st.title("Encuesta OCAI - Cultura Organizacional Actual")

# ==========================================
# DATOS PARTICIPANTE
# ==========================================

st.header("Datos del participante")

col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre Completo (opcional)")
    cargo = st.text_input("Cargo")

with col2:
    gerencia = st.text_input("Gerencia")
    area = st.text_input("Área")


st.markdown("---")

st.markdown("""
### Instrucciones

Distribuya exactamente 100 puntos entre las cuatro alternativas de cada dimensión.

Mientras más representativa sea una alternativa de la cultura actual de la organización, más puntos debe asignarle.

La suma de las cuatro alternativas debe ser igual a 100.
""")


# ==========================================
# PREGUNTAS OCAI
# ==========================================

preguntas = {

    "1. Características dominantes": {

        "Clan":
        "La organización es un lugar muy personal. Es como una familia extendida. Las personas parecen compartir mucho de sí mismas.",

        "Adhocracia":
        "La organización es muy dinámica y emprendedora. Las personas están dispuestas a arriesgarse y asumir riesgos.",

        "Mercado":
        "La organización está muy orientada a resultados. Una preocupación principal es cumplir con el trabajo/resultado. Las personas son muy competitivas y orientadas al logro.",

        "Jerarquía":
        "La organización es un lugar muy controlado y estructurado. Los procedimientos formales generalmente gobiernan lo que hacen las personas."
    },

    "2. Liderazgo organizacional": {

        "Clan":
        "El liderazgo en la organización generalmente se considera como ejemplar en mentoría, facilitación o apoyo al desarrollo de personas.",

        "Adhocracia":
        "El liderazgo en la organización generalmente se considera como ejemplar en emprendimiento, innovación o toma de riesgos.",

        "Mercado":
        "El liderazgo en la organización generalmente se considera como ejemplar en un enfoque directo/práctico, agresivo con las metas y orientado a resultados.",

        "Jerarquía":
        "El liderazgo en la organización generalmente se considera como ejemplar en coordinación, organización o buen funcionamiento de operaciones fluidas."
    },

    "3. Gestión de empleados": {

        "Clan":
        "El estilo de gestión en la organización se caracteriza por trabajo en equipo, consenso y participación.",

        "Adhocracia":
        "El estilo de gestión en la organización se caracteriza por la toma de riesgos individual, innovación, libertad y singularidad.",

        "Mercado":
        "El estilo de gestión en la organización se caracteriza por competitividad intensa, altas exigencias y logro.",

        "Jerarquía":
        "El estilo de gestión en la organización se caracteriza por seguridad laboral, conformidad, previsibilidad y estabilidad en las relaciones."
    },

    "4. Cohesión organizacional": {

        "Clan":
        "Lo que mantiene unida a la organización es la lealtad y la confianza mutua. El compromiso con esta organización es alto.",

        "Adhocracia":
        "Lo que mantiene unida a la organización es el compromiso con la innovación y el desarrollo. Hay énfasis en estar a la vanguardia.",

        "Mercado":
        "Lo que mantiene unida a la organización es el énfasis en el logro de resultados y el cumplimiento de objetivos.",

        "Jerarquía":
        "Lo que mantiene unida a la organización son las reglas y políticas formales. Mantener un funcionamiento bien coordinado es importante."
    },

    "5. Énfasis estratégicos": {

        "Clan":
        "La organización enfatiza el desarrollo humano. Predominan la alta confianza, la apertura y la participación constante.",

        "Adhocracia":
        "La organización enfatiza adquirir nuevos recursos y crear nuevos desafíos. Se valoran probar cosas nuevas y buscar oportunidades.",

        "Mercado":
        "La organización enfatiza acciones competitivas y logro. Alcanzar metas ambiciosas y ganar en el mercado es muy importante.",

        "Jerarquía":
        "La organización enfatiza la permanencia y la estabilidad. La eficiencia, el control y el buen funcionamiento de las operaciones son importantes."
    },

    "6. Criterios de éxito": {

        "Clan":
        "La organización define el éxito en función del desarrollo de recursos humanos, trabajo en equipo, compromiso de los empleados y preocupación por las personas.",

        "Adhocracia":
        "La organización define el éxito en función de tener los productos más únicos o nuevos. Es líder en productos e innovación.",

        "Mercado":
        "La organización define el éxito en función de ganar en el mercado y superar a la competencia. El liderazgo competitivo es fundamental.",

        "Jerarquía":
        "La organización define el éxito en función de la eficiencia, la entrega confiable, el buen cumplimiento de la programación y la producción de bajo costo."
    }

}

# ==========================================
# CAPTURA RESPUESTAS
# ==========================================

resultados = {}

for dimension, opciones in preguntas.items():

    st.subheader(dimension)

    respuestas = {}

    for cultura, texto in opciones.items():

        col_texto, col_valor = st.columns([10,1]) 
        
        with col_texto: 
            st.write(texto)

        with col_valor:
            respuestas[cultura] = st.number_input(
                label="",
                min_value=0,
                max_value=100,
                value=0,
                step=1,
                key=f"{dimension}_{cultura}"
            )

    total = sum(respuestas.values()) 
        
    if total > 0:

        if total != 100:
            st.warning(
                f"Puntos asignados: {total}/100"
            )
        else:
            st.success(
                "Total correcto: 100 puntos"
            )
            
    resultados[dimension] = respuestas 
        
    st.markdown("---")


# ==========================================
# BOTÓN FINALIZAR Y VALIDACIONES    
# ==========================================

if st.button("Finalizar Encuesta"):

    errores = []

    # Validar que todas las dimensiones sumen 100

    for dimension, respuestas in resultados.items():

        if sum(respuestas.values()) != 100:
            errores.append(dimension)

    # Validar datos obligatorios

    campos_faltantes = []

    if not gerencia:
        campos_faltantes.append("Gerencia")

    if not area:
        campos_faltantes.append("Área")

    if not cargo:
        campos_faltantes.append("Cargo")

    # Mostrar errores

    if len(campos_faltantes) > 0:

        st.error(
            "Complete los siguientes campos: "
            + ", ".join(campos_faltantes)
        )

    elif len(errores) > 0:

        st.error(
            "Debe completar correctamente las 6 preguntas. "
            "La suma de cada dimensión debe ser igual a 100."
        )

    else:

        # Evitar doble envío
        if st.session_state.encuesta_enviada:

            st.warning(
                "Esta encuesta ya fue enviada."
            )

            st.stop()

        try:

            registro = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre": nombre,
                "cargo": cargo,
                "gerencia": gerencia,
                "area": area
            }

            # Guardar respuestas

            for dimension, respuestas in resultados.items():

                for cultura, valor in respuestas.items():

                    registro[
                        f"{dimension}_{cultura}"
                    ] = valor

            archivo = "resultados_ocai.csv"

            df_nuevo = pd.DataFrame([registro])

            if os.path.exists(archivo):

                df_nuevo.to_csv(
                    archivo,
                    mode="a",
                    header=False,
                    index=False,
                    encoding="utf-8-sig"
                )

            else:

                df_nuevo.to_csv(
                    archivo,
                    index=False,
                    encoding="utf-8-sig"
    
                )

            # Marcar encuesta como enviada
            st.session_state.encuesta_enviada = True

            st.rerun()

            st.success(
                "¡Gracias por participar de la encuesta!"
            )    
            
            st.markdown(
            """
            Puede cerrar esta ventana.
            """
            )

            st.balloons()

        except Exception as e:

            st.error(
                f"Error al guardar la encuesta: {e}"
            )