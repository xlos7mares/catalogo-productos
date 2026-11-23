import os
import urllib.parse
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Catálogo Digital",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Fondo claro y textos oscuros legibles */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1150px;
    }

    /* Encabezado luminoso en tonos celestes */
    .hero-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border: 1px solid #7dd3fc;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 22px;
        text-align: center;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0c4a6e;
        margin: 0 0 6px 0;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #0369a1;
        margin: 0;
    }

    /* Etiquetas de campos y selectores */
    label, .stTextInput label, .stSelectbox label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Contador de imagen */
    .foto-contador {
        text-align: center;
        font-size: 0.88rem;
        color: #0369a1;
        font-weight: 600;
        margin: 6px 0 10px 0;
    }

    /* Botones celestes bien visibles en reposo y al pasar el cursor */
    .stButton > button {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border: 1px solid #0369a1 !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        padding: 0.45rem 0.75rem !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {
        color: #ffffff !important;
    }
    .stButton > button:hover {
        background-color: #0369a1 !important;
        border-color: #0c4a6e !important;
        color: #ffffff !important;
    }
    .stButton > button:focus,
    .stButton > button:active {
        background-color: #0ea5e9 !important;
        border-color: #0284c7 !important;
        color: #ffffff !important;
    }

    /* Etiqueta de categoría, título, descripción y precio */
    .product-badge {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        border: 1px solid #bae6fd;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 999px;
        margin-top: 10px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .product-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 6px 0;
    }
    .product-desc {
        font-size: 0.9rem;
        color: #334155;
        margin: 0 0 12px 0;
        line-height: 1.45;
    }
    .product-price {
        font-size: 1.25rem;
        font-weight: 800;
        color: #0284c7;
        margin-bottom: 14px;
    }

    /* Botón alegre de consulta por WhatsApp */
    .wa-btn {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #16a34a;
        color: #ffffff !important;
        font-weight: 800;
        text-decoration: none;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.95rem;
        box-sizing: border-box;
        transition: background-color 0.15s ease;
    }
    .wa-btn:hover {
        background-color: #15803d;
    }
</style>
""", unsafe_allow_html=True)

# Evitar sugerencias guardadas del navegador en el campo de búsqueda
components.html("""
<script>
(function() {
    const doc = window.parent.document;
    function desactivarAutocomplete() {
        const inputs = doc.querySelectorAll('input[type="text"]');
        inputs.forEach(inp => {
            inp.setAttribute('autocomplete', 'off');
            inp.setAttribute('autocorrect', 'off');
            inp.setAttribute('autocapitalize', 'off');
            inp.setAttribute('spellcheck', 'false');
        });
    }
    desactivarAutocomplete();
    const obs = new MutationObserver(desactivarAutocomplete);
    obs.observe(doc.body, { childList: true, subtree: true });
})();
</script>
""", height=0)

TELEFONO_WHATSAPP = "59899417716"
CARPETA_BASE = "imagenes"
EXTENSIONES_IMG = (".jpg", ".jpeg", ".png", ".webp")

def parsear_datos_txt(ruta_txt, nombre_carpeta):
    datos = {
        "nombre": nombre_carpeta,
        "categoria": "General",
        "precio": "Consultar",
        "descripcion": ""
    }
    if os.path.isfile(ruta_txt):
        with open(ruta_txt, "r", encoding="utf-8") as f:
            for linea in f:
                if ":" in linea:
                    clave, valor = linea.split(":", 1)
                    clave = clave.strip().lower()
                    valor = valor.strip()
                    if clave in datos and valor:
                        datos[clave] = valor
    return datos

@st.cache_data
def cargar_catalogo_desde_carpetas():
    productos = []
    if not os.path.isdir(CARPETA_BASE):
        return productos

    for item in sorted(os.listdir(CARPETA_BASE)):
        ruta_prod = os.path.join(CARPETA_BASE, item)
        if os.path.isdir(ruta_prod):
            ruta_txt = os.path.join(ruta_prod, "datos.txt")
            info = parsear_datos_txt(ruta_txt, item)
            fotos = [
                os.path.join(ruta_prod, archivo)
                for archivo in sorted(os.listdir(ruta_prod))
                if archivo.lower().endswith(EXTENSIONES_IMG)
            ]
            productos.append({
                "id": item,
                "nombre": info["nombre"],
                "categoria": info["categoria"],
                "precio": info["precio"],
                "descripcion": info["descripcion"],
                "imagenes": fotos
            })
    return productos

productos = cargar_catalogo_desde_carpetas()

st.markdown("""
<div class="hero-box">
    <div class="hero-title">CATÁLOGO DE PRODUCTOS</div>
    <div class="hero-subtitle">Explorá las opciones disponibles y consultá directo por WhatsApp</div>
</div>
""", unsafe_allow_html=True)

col_busqueda, col_categoria = st.columns([2, 1])
with col_busqueda:
    texto_busqueda = st.text_input(
        "Buscar producto",
        placeholder="Ej: Wall Panel, madera, exterior...",
        autocomplete="off"
    )
with col_categoria:
    categorias = ["Todas"] + sorted(list(set(p["categoria"] for p in productos)))
    categoria_elegida = st.selectbox("Categoría", categorias)

filtrados = [
    p for p in productos
    if (categoria_elegida == "Todas" or p["categoria"] == categoria_elegida)
    and (
        texto_busqueda.strip() == ""
        or texto_busqueda.lower() in p["nombre"].lower()
        or texto_busqueda.lower() in p["descripcion"].lower()
        or texto_busqueda.lower() in p["categoria"].lower()
    )
]

if len(filtrados) == 1:
    st.markdown(f"**{filtrados[0]['nombre']}**")
elif len(filtrados) > 1:
    nombres = ", ".join(p["nombre"] for p in filtrados)
    st.markdown(f"**{nombres}**")
else:
    st.markdown("**Sin productos para mostrar**")

if not filtrados:
    st.info("No hay productos cargados o ninguno coincide con el filtro.")
else:
    cols = st.columns(3)
    for idx, prod in enumerate(filtrados):
        with cols[idx % 3]:
            with st.container(border=True):
                fotos = prod["imagenes"]
                if fotos:
                    state_key = f"img_idx_{prod['id']}"
                    if state_key not in st.session_state:
                        st.session_state[state_key] = 0
                    if st.session_state[state_key] >= len(fotos):
                        st.session_state[state_key] = 0

                    pos_actual = st.session_state[state_key]
                    st.image(fotos[pos_actual], use_container_width=True)
                    st.markdown(
                        f'<div class="foto-contador">Imagen {pos_actual + 1} de {len(fotos)}</div>',
                        unsafe_allow_html=True
                    )

                    if len(fotos) > 1:
                        b_prev, b_next = st.columns(2)
                        with b_prev:
                            if st.button("◀ Anterior", key=f"prev_{idx}_{prod['id']}", use_container_width=True):
                                st.session_state[state_key] = (pos_actual - 1) % len(fotos)
                                st.rerun()
                        with b_next:
                            if st.button("Siguiente ▶", key=f"next_{idx}_{prod['id']}", use_container_width=True):
                                st.session_state[state_key] = (pos_actual + 1) % len(fotos)
                                st.rerun()
                else:
                    st.warning("Sin imágenes en esta carpeta")

                mensaje = f"Hola, me interesa el producto: {prod['nombre']} (Precio: {prod['precio']}) que vi en el catálogo."
                url_wa = f"https://wa.me/{TELEFONO_WHATSAPP}?text={urllib.parse.quote(mensaje)}"

                st.markdown(f"""
                    <span class="product-badge">{prod['categoria']}</span>
                    <div class="product-title">{prod['nombre']}</div>
                    <div class="product-desc">{prod['descripcion']}</div>
                    <div class="product-price">{prod['precio']}</div>
                    <a href="{url_wa}" target="_blank" class="wa-btn">Consultar por WhatsApp</a>
                """, unsafe_allow_html=True)

components.html("""
<div style="text-align:center; margin-top:12px; font-family:sans-serif;">
    <button onclick="copiarLink()" style="background:#0284c7; color:#ffffff; border:1px solid #0369a1; padding:8px 16px; border-radius:9px; cursor:pointer; font-size:13px; font-weight:700;">
        Copiar enlace del catálogo
    </button>
    <span id="msg" style="color:#0284c7; font-size:13px; margin-left:8px; font-weight:700;"></span>
</div>
<script>
function copiarLink() {
    navigator.clipboard.writeText(window.parent.location.href);
    document.getElementById('msg').innerText = '¡Enlace copiado!';
    setTimeout(() => { document.getElementById('msg').innerText = ''; }, 2500);
}
</script>
""", height=55)
