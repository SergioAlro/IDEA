import streamlit as st
import requests

API_URL = "http://localhost:8000"


def set_page(page: str):
    st.session_state.page = page


def main_menu():
    st.title("IDEA")
    st.header("Menú principal")
    st.write("Seleccione una opción")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Administrar preguntas", key="admin_btn", help="Ir a crud"):
            set_page("admin")
            st.experimental_rerun()
    with col2:
        if st.button("Generar examen", key="test_btn", help="Generar test"):
            set_page("test")
            st.experimental_rerun()


def admin_page():
    st.title("Administrar preguntas")
    if st.button("Volver", key="back_admin"):
        set_page("menu")
        st.experimental_rerun()

    # Listar preguntas
    st.subheader("Preguntas registradas")
    resp = requests.get(f"{API_URL}/preguntas/")
    if resp.ok:
        preguntas = resp.json()
        for p in preguntas:
            st.write(f"{p['id']}. {p['pregunta']}")
    else:
        st.error("Error obteniendo preguntas")

    st.markdown("---")
    st.subheader("Crear nueva pregunta")
    with st.form("create_form"):
        pregunta = st.text_input("Pregunta")
        opcion_a = st.text_input("Opción A")
        opcion_b = st.text_input("Opción B")
        opcion_c = st.text_input("Opción C")
        opcion_d = st.text_input("Opción D")
        resultado = st.selectbox("Respuesta correcta", ["A", "B", "C", "D"])
        submitted = st.form_submit_button("Crear")
        if submitted:
            data = {
                "pregunta": pregunta,
                "opcion_a": opcion_a,
                "opcion_b": opcion_b,
                "opcion_c": opcion_c,
                "opcion_d": opcion_d,
                "resultado": resultado,
            }
            r = requests.post(f"{API_URL}/preguntas/", json=data)
            if r.ok:
                st.success("Pregunta creada")
                st.experimental_rerun()
            else:
                st.error("Error al crear pregunta")

    st.markdown("---")
    st.subheader("Actualizar o eliminar pregunta")
    resp = requests.get(f"{API_URL}/preguntas/")
    if resp.ok:
        preguntas = resp.json()
        ids = [str(p['id']) for p in preguntas]
        select_id = st.selectbox("Seleccione ID", ids)
        if select_id:
            p = next((x for x in preguntas if str(x['id']) == select_id), None)
            if p:
                with st.form("update_form"):
                    pregunta = st.text_input("Pregunta", value=p['pregunta'])
                    opcion_a = st.text_input("Opción A", value=p['opcion_a'])
                    opcion_b = st.text_input("Opción B", value=p['opcion_b'])
                    opcion_c = st.text_input("Opción C", value=p['opcion_c'])
                    opcion_d = st.text_input("Opción D", value=p['opcion_d'])
                    resultado = st.selectbox(
                        "Respuesta correcta",
                        ["A", "B", "C", "D"],
                        index=["A", "B", "C", "D"].index(p['resultado'])
                    )
                    if st.form_submit_button("Actualizar"):
                        data = {
                            "pregunta": pregunta,
                            "opcion_a": opcion_a,
                            "opcion_b": opcion_b,
                            "opcion_c": opcion_c,
                            "opcion_d": opcion_d,
                            "resultado": resultado,
                        }
                        r = requests.put(f"{API_URL}/preguntas/{select_id}", json=data)
                        if r.ok:
                            st.success("Pregunta actualizada")
                            st.experimental_rerun()
                        else:
                            st.error("Error actualizando pregunta")
                if st.button("Eliminar", key="delete_btn"):
                    r = requests.delete(f"{API_URL}/preguntas/{select_id}")
                    if r.ok:
                        st.success("Pregunta eliminada")
                        st.experimental_rerun()
                    else:
                        st.error("Error eliminando pregunta")
    else:
        st.error("No se pudieron cargar preguntas")


def test_page():
    st.title("Generar examen")
    if st.button("Volver", key="back_test"):
        set_page("menu")
        st.experimental_rerun()

    if "generated_test" not in st.session_state:
        st.session_state.generated_test = []

    n = st.number_input("Número de preguntas", min_value=1, step=1, key="num_questions")
    if st.button("Generar", key="generate_btn"):
        r = requests.get(f"{API_URL}/generar_test/", params={"preguntas": int(n)})
        if r.ok:
            st.session_state.generated_test = r.json()
        else:
            st.error("Error al generar examen")

    for idx, p in enumerate(st.session_state.generated_test):
        st.subheader(f"{idx + 1}. {p['pregunta']}")
        opciones = {
            "A": p['opcion_a'],
            "B": p['opcion_b'],
            "C": p['opcion_c'],
            "D": p['opcion_d'],
        }
        st.radio(
            "Seleccione la respuesta correcta",
            list(opciones.keys()),
            format_func=lambda x: f"{x}. {opciones[x]}",
            key=f"respuesta_{idx}",
            index=None,
        )

    if st.session_state.generated_test:
        if st.button("Corregir", key="grade_btn"):
            total = len(st.session_state.generated_test)
            correctas = 0

            for idx, p in enumerate(st.session_state.generated_test):
                seleccion = st.session_state.get(f"respuesta_{idx}")
                if seleccion is None:
                    st.error("Seleccione todas las respuestas antes de corregir")
                    return

            for idx, p in enumerate(st.session_state.generated_test):
                seleccion = st.session_state.get(f"respuesta_{idx}")
                correcta = p['resultado']
                st.write(f"{idx + 1}. {p['pregunta']}")
                st.write(f"Tu respuesta: {seleccion}")
                st.write(f"Respuesta correcta: {correcta}")
                if seleccion == correcta:
                    correctas += 1

            st.success(f"Has acertado {correctas} de {total} preguntas")


def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'menu'

    if st.session_state.page == 'menu':
        main_menu()
    elif st.session_state.page == 'admin':
        admin_page()
    elif st.session_state.page == 'test':
        test_page()


if __name__ == "__main__":
    main()
