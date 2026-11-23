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
    .stApp {
        background-color: #070b14;
        color: #f1f5f9;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1150px;
    }
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
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin: 0;
    }
    .product-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 18px;
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
        box-sizing: border-box;
    }
    .wa-btn:hover {
        background-color: #20bd5a;
    }
</style>
""", unsafe_allow_html=True)

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
    texto_busqueda = st.text_input("Buscar producto", placeholder="Ej: Wall Panel, madera, exterior...")
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

st.write(f"Mostrando **{len(filtrados)}** producto(s)")

if not filtrados:
    st.info("No hay productos cargados o ninguno coincide con el filtro.")
else:
    cols = st.columns(3)
    for idx, prod in enumerate(filtrados):
        with cols[idx % 3]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)

            if prod["imagenes"]:
                foto_sel = st.selectbox(
                    "Foto del producto",
                    prod["imagenes"],
                    format_func=lambda x: os.path.basename(x),
                    key=f"foto_{idx}_{prod['id']}"
                )
                st.image(foto_sel, use_container_width=True)
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
            </div>
            """, unsafe_allow_html=True)

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
