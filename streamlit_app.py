import json
import urllib.parse
import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración general de la página (debe ir siempre primero)
st.set_page_config(
    page_title="Catálogo Digital",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilos CSS personalizados (modo oscuro, tarjetas limpias y diseño adaptable a celular)
st.markdown("""
<style>
    /* Fondo general y tipografía */
    .stApp {
        background-color: #070b14;
        color: #f1f5f9;
    }

    /* Ocultar elementos innecesarios de Streamlit para que parezca una web comercial */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Contenedor principal más aprovechado en celular */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1150px;
    }

    /* Encabezado / Hero */
    .hero-box {
        background: linear-gradient(135deg, #0d172a 0%, #112240 100%);
        border: 1px solid #1e3a5f;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 22px;
        text-align: center;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 6px 0;
        letter-spacing: 0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin: 0;
    }

    /* Tarjeta de producto */
    .product-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 18px;
        transition: transform 0.2s ease, border-color 0.2s ease;
        display: flex;
        flex-direction: column;
    }
    .product-card:hover {
        border-color: #39ff14;
        transform: translateY(-3px);
    }
    .product-img {
        width: 100%;
        height: 210px;
        object-fit: cover;
        border-bottom: 1px solid #1e293b;
    }
    .product-body {
        padding: 16px;
    }
    .product-badge {
        display: inline-block;
        background-color: rgba(0, 212, 255, 0.12);
        color: #00d4ff;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 999px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    .product-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0 0 6px 0;
    }
    .product-desc {
        font-size: 0.9rem;
        color: #cbd5e1;
        margin: 0 0 12px 0;
        line-height: 1.4;
    }
    .product-price {
        font-size: 1.25rem;
        font-weight: 800;
        color: #39ff14;
        margin-bottom: 14px;
    }
    .wa-btn {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #25d366;
        color: #051b0e !important;
        font-weight: 800;
        text-decoration: none;
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 0.95rem;
    }
    .wa-btn:hover {
        background-color: #20bd5a;
    }
</style>
""", unsafe_allow_html=True)

# 3. Cargar productos desde el archivo JSON
@st.cache_data
def cargar_productos():
    with open("productos.json", "r", encoding="utf-8") as f:
        return json.load(f)

productos = cargar_productos()

# Número de WhatsApp en formato internacional sin '+' ni espacios (Uruguay: 598...)
TELEFONO_WHATSAPP = "59899417716"

# 4. Encabezado visual
st.markdown("""
<div class="hero-box">
    <div class="hero-title">CATÁLOGO DE PRODUCTOS</div>
    <div class="hero-subtitle">Explorá las opciones disponibles y consultá directo por WhatsApp</div>
</div>
""", unsafe_allow_html=True)

# 5. Barra de búsqueda y filtro por categoría
col_busqueda, col_categoria = st.columns([2, 1])

with col_busqueda:
    texto_busqueda = st.text_input("Buscar producto", placeholder="Ej: nombre, código o característica...")

with col_categoria:
    categorias = ["Todas"] + sorted(list(set(p["categoria"] for p in productos)))
    categoria_elegida = st.selectbox("Categoría", categorias)

# Filtrar productos
filtrados = []
for p in productos:
    coincide_cat = (categoria_elegida == "Todas") or (p["categoria"] == categoria_elegida)
    coincide_txt = (
        texto_busqueda.strip() == ""
        or texto_busqueda.lower() in p["nombre"].lower()
        or texto_busqueda.lower() in p["descripcion"].lower()
        or texto_busqueda.lower() in p["id"].lower()
    )
    if coincide_cat and coincide_txt:
        filtrados.append(p)

st.write(f"Mostrando **{len(filtrados)}** producto(s)")

# 6. Grilla de tarjetas (3 columnas en PC, se apilan solas en celular)
if not filtrados:
    st.info("No se encontraron productos con ese filtro.")
else:
    cols = st.columns(3)
    for idx, prod in enumerate(filtrados):
        mensaje = f"Hola, me interesa el producto: {prod['nombre']} (Ref: {prod['id']}) que vi en el catálogo."
        url_wa = f"https://wa.me/{TELEFONO_WHATSAPP}?text={urllib.parse.quote(mensaje)}"

        tarjeta_html = f"""
        <div class="product-card">
            <img src="{prod['imagen']}" class="product-img" alt="{prod['nombre']}">
            <div class="product-body">
                <span class="product-badge">{prod['categoria']} · {prod['id']}</span>
                <div class="product-title">{prod['nombre']}</div>
                <div class="product-desc">{prod['descripcion']}</div>
                <div class="product-price">{prod['precio']}</div>
                <a href="{url_wa}" target="_blank" class="wa-btn">Consultar por WhatsApp</a>
            </div>
        </div>
        """
        with cols[idx % 3]:
            st.markdown(tarjeta_html, unsafe_allow_html=True)

# 7. Pequeño bloque JS opcional (ejemplo: botón para copiar enlace del catálogo)
components.html("""
<div style="text-align:center; margin-top:10px; font-family:sans-serif;">
    <button onclick="copiarLink()" style="background:#1e293b; color:#e2e8f0; border:1px solid #334155; padding:8px 16px; border-radius:8px; cursor:pointer; font-size:13px;">
        Copiar enlace del catálogo
    </button>
    <span id="msg" style="color:#39ff14; font-size:13px; margin-left:8px;"></span>
</div>
<script>
function copiarLink() {
    navigator.clipboard.writeText(window.parent.location.href);
    document.getElementById('msg').innerText = '¡Enlace copiado!';
    setTimeout(() => { document.getElementById('msg').innerText = ''; }, 2500);
}
</script>
""", height=55)
