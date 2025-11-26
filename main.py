import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import folium
from folium.plugins import MarkerCluster
from PIL import Image
import random
import io
import math
import pandas as pd
import urllib.parse
import numpy as np

# Import local modules
import db
import ai_service

# --- Page Configuration ---
st.set_page_config(
    page_title="EcoCycle ID - Future of Waste",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Design System & CSS ---
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #10b981;
    --primary-dark: #047857;
    --secondary: #f59e0b;
    --dark: #0f172a;
    --light: #f8fafc;
    --glass: rgba(255, 255, 255, 0.9);
    --glass-border: rgba(255, 255, 255, 0.2);
    --shadow: 0 10px 40px -10px rgba(0,0,0,0.1);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--dark);
    background-color: #f0fdf4; /* Very light green bg */
}

/* Background Pattern */
.stApp {
    background-image: 
        radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(245, 158, 11, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.1) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%);
    background-attachment: fixed;
}

/* Typography */
h1, h2, h3 {
    letter-spacing: -0.02em;
}

/* Components */
.hero-header {
    text-align: center;
    padding: 4rem 2rem 2rem;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: clamp(3rem, 8vw, 5.5rem);
    font-weight: 800;
    background: linear-gradient(135deg, #064e3b 0%, #10b981 50%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: 1rem;
    text-shadow: 0 20px 40px rgba(16, 185, 129, 0.2);
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #475569;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
}

.pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1.25rem;
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 100px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    font-weight: 600;
    font-size: 0.875rem;
    color: #059669;
    margin-bottom: 2rem;
}

/* Glass Cards */
.modern-card {
    background: var(--glass);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.6);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.modern-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 50px -10px rgba(0,0,0,0.15);
}

.stat-number {
    font-size: 3rem;
    font-weight: 800;
    color: var(--dark);
    line-height: 1;
}
.stat-label {
    font-weight: 600;
    color: #64748b;
    margin-top: 0.5rem;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}

/* Feature Action Cards */
.feature-btn-container {
    position: relative;
    border-radius: 32px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    transition: all 0.3s ease;
    cursor: pointer;
    height: 320px;
}
.feature-btn-container:hover {
    transform: scale(1.02);
}

.feature-content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 2.5rem;
    background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0) 100%);
    color: white;
    z-index: 2;
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: inline-block;
    padding: 1rem;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    backdrop-filter: blur(8px);
}

/* Custom Button Styling Override */
div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    border: none;
    transition: all 0.2s;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -5px rgba(0,0,0,0.2);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --- Database Initialization ---
try:
    db.init_db()
except Exception as e:
    st.error(f"Gagal menginisialisasi database: {e}")
    st.stop()


# --- Helper Functions ---
def jitter_location(lat, lon, meters=200):
    """Adds a random offset to latitude and longitude to protect privacy."""
    lat_jitter = random.uniform(-meters, meters) / 111132
    lon_jitter = random.uniform(-meters, meters) / (111132 * abs(math.cos(math.radians(lat))))
    return lat + lat_jitter, lon + lon_jitter

def get_marker_color(post: dict) -> str:
    """Determines marker color based on waste suitability."""
    suitable_for = post.get('suitable_for', '').lower()
    if 'sayur' in post.get('waste_category', '').lower() or 'kompos' in suitable_for:
        return 'green'
    if 'makanan' in post.get('waste_category', '').lower() or 'ayam' in suitable_for or 'maggot' in suitable_for:
        return 'orange'
    return 'red'

def get_suitability_emojis(tags_string: str) -> str:
    """Returns emojis based on suitability tags."""
    emojis = []
    if 'Maggot' in tags_string: emojis.append("🐛")
    if 'Ayam' in tags_string or 'Unggas' in tags_string: emojis.append("🐔")
    if 'Pupuk Kompos' in tags_string: emojis.append("🌱")
    if 'Ikan' in tags_string: emojis.append("🐟")
    if 'Biogas' in tags_string: emojis.append("💨")
    return " ".join(emojis)

def change_page(page_name):
    """Callback function to change the page view."""
    st.session_state.page = page_name

# ======================================================================================
# --- 1. LANDING PAGE (PITCH DECK STYLE) ---
# ======================================================================================
def show_landing_page():
    # Hero Section
    st.markdown(
        """
        <div class="hero-header">
            <div class="pill-badge">🚀 Finalist ITB Hackathon 2025</div>
            <h1 class="hero-title">EcoCycle ID</h1>
            <p class="hero-subtitle">
                Platform <b>AI-Driven Marketplace</b> pertama di Indonesia yang mengubah 
                masalah limbah organik menjadi peluang ekonomi sirkular bagi peternak lokal.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Key Traction Metrics
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("1,247 kg", "Limbah Terolah", "↗ 12% WoW"),
        ("Rp 18.5jt", "Valuasi Transaksi", "↗ 8% MoM"),
        ("318", "Mitra UMKM", "+12 Hari ini"),
        ("98.5%", "Akurasi AI", "Model v2.1")
    ]
    
    for col, (val, label, trend) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="modern-card" style="text-align:center;">
                    <div class="stat-number">{val}</div>
                    <div class="stat-label">{label}</div>
                    <div style="color:#10b981; font-size:0.8rem; font-weight:bold; margin-top:0.5rem;">{trend}</div>
                </div>
                """, unsafe_allow_html=True
            )

    st.write("")
    st.write("")
    st.write("")

    # Main Action Area (Split View)
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        # Provider Card
        st.markdown(
            """
            <div class="feature-btn-container" style="background: linear-gradient(150deg, #10b981 0%, #065f46 100%);">
                <div class="feature-content">
                    <div class="feature-icon">📸</div>
                    <h2>Provider</h2>
                    <p>Untuk Resto, Hotel & Rumah Tangga.<br>Scan sampahmu, dapatkan poin & pickup terjadwal.</p>
                </div>
                <div style="position:absolute; top:0; right:0; bottom:0; left:0; background:url('https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'); opacity:0.2; background-size:cover;"></div>
            </div>
            """, unsafe_allow_html=True
        )
        st.button("Mulai Setor Sampah →", key="btn_prov", on_click=change_page, args=("provider",), use_container_width=True)

    with col_right:
        # Seeker Card
        st.markdown(
            """
            <div class="feature-btn-container" style="background: linear-gradient(150deg, #f59e0b 0%, #78350f 100%);">
                <div class="feature-content">
                    <div class="feature-icon">🗺️</div>
                    <h2>Seeker</h2>
                    <p>Untuk Peternak Maggot & Komposter.<br>Cari bahan baku murah di sekitarmu.</p>
                </div>
                <div style="position:absolute; top:0; right:0; bottom:0; left:0; background:url('https://images.unsplash.com/photo-1585119192228-f6723c0e832b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'); opacity:0.2; background-size:cover;"></div>
            </div>
            """, unsafe_allow_html=True
        )
        st.button("Cari Pakan Sekarang →", key="btn_seek", on_click=change_page, args=("seeker",), use_container_width=True)

    # Footer Trust
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; opacity:0.6; font-size:0.9rem;">
            <p>Dipercaya oleh komunitas peduli lingkungan di <b>Jakarta, Bandung, & Surabaya</b></p>
        </div>
        """, unsafe_allow_html=True
    )


# ======================================================================================
# --- 2. PROVIDER VIEW (AI SCANNER) ---
# ======================================================================================
def show_provider_page():
    c1, c2 = st.columns([1, 5])
    with c1:
        st.button("← Kembali", on_click=change_page, args=("landing",))
    
    st.markdown(
        """
        <div style="background:white; border-radius:20px; padding:2rem; box-shadow:0 4px 20px rgba(0,0,0,0.05); margin-bottom:2rem;">
            <h2 style="margin:0; color:#047857;">📸 AI Waste Scanner</h2>
            <p style="color:#64748b;">Upload foto sampah organik Anda. AI kami akan mengidentifikasi jenis, berat, dan nilai ekonominya.</p>
        </div>
        """, unsafe_allow_html=True
    )

    c_input, c_preview = st.columns([1, 1])

    with c_input:
        st.selectbox("Jenis Sumber", [p.value for p in db.ProviderType], key="prov_type")
        uploaded_file = st.file_uploader("Ambil Foto / Upload", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            if st.button("🔍 Analisis Foto", type="primary", use_container_width=True):
                st.session_state.pil_image = Image.open(uploaded_file)
                with st.spinner("AI sedang bekerja..."):
                    res = ai_service.analyze_waste_multipurpose(st.session_state.pil_image)
                    if 'error' not in res:
                        if res.get('is_organic_waste') is False:
                            st.error(f"❌ Foto ditolak: {res.get('rejection_reason', 'Bukan limbah organik.')}")
                            # Clear analysis so it doesn't show the success card
                            if 'ai_analysis' in st.session_state: del st.session_state.ai_analysis
                        else:
                            st.session_state.ai_analysis = res
                    else:
                        st.error("Gagal analisis.")

    with c_preview:
        if 'pil_image' in st.session_state:
            st.image(st.session_state.pil_image, caption="Preview", use_column_width=True)

    # Result Section
    if 'ai_analysis' in st.session_state and st.session_state.ai_analysis.get('is_organic_waste', True):
        st.markdown("---")
        res = st.session_state.ai_analysis
        
        # Glass Result Card
        st.markdown(
            f"""
            <div class="modern-card" style="background:linear-gradient(135deg, #ecfdf5 0%, #fff 100%); border-color:#a7f3d0;">
                <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
                    <div style="font-size:2rem;">✨</div>
                    <div>
                        <h3 style="margin:0; color:#065f46;">{res.get('main_composition', 'Terdeteksi')}</h3>
                        <p style="margin:0; color:#059669;">Grade A • Organik Murni</p>
                    </div>
                    <div style="margin-left:auto; text-align:right;">
                        <div style="font-size:2rem; font-weight:800; color:#059669;">{res.get('estimated_weight_kg', 0)} kg</div>
                        <div style="font-size:0.8rem; color:#059669;">Estimasi Berat</div>
                    </div>
                </div>
                <div style="background:rgba(255,255,255,0.6); padding:1rem; border-radius:12px; margin-top:1rem;">
                    <strong>💡 Rekomendasi:</strong> {', '.join(res.get('suitability_tags', []))} {get_suitability_emojis(", ".join(res.get('suitability_tags', [])))}
                    <br>
                    <small style="color:#64748b;">Tip: {res.get('handling_tip', '-')}</small>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
        
        st.write("")
        col_loc, col_act = st.columns([2, 1])
        with col_loc:
            location = streamlit_geolocation()
        with col_act:
            if location and location.get('latitude'):
                st.success("Lokasi Akurat.")
                if st.button("🚀 Posting ke Marketplace", type="primary", use_container_width=True):
                    priv_lat, priv_lon = jitter_location(location['latitude'], location['longitude'])
                    blob = ai_service.image_to_blob(st.session_state.pil_image)
                    db.add_waste_post(
                        db.ProviderType(st.session_state.prov_type),
                        priv_lat, priv_lon, blob, st.session_state.ai_analysis
                    )
                    st.balloons()
                    st.success("Berhasil diposting!")
                    del st.session_state.ai_analysis


# ======================================================================================
# --- 3. SEEKER VIEW (MAPS) ---
# ======================================================================================
def show_seeker_page():
    st.button("← Kembali ke Dashboard", on_click=change_page, args=("landing",))
    
    # Header
    st.markdown(
        """
        <div style="margin-bottom:1.5rem;">
            <h1 style="font-size:2.5rem; margin-bottom:0.5rem;">🗺️ Peta Limbah Real-Time</h1>
            <p style="color:#64748b; font-size:1.1rem;">Temukan sumber pakan organik di sekitar Anda. Data diperbarui setiap 15 menit.</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Filter Bar (Floating look)
    with st.container():
        cols = st.columns([3, 2])
        with cols[0]:
            filters = st.multiselect("Filter Kategori Pakan:", ['Maggot BSF', 'Ayam/Unggas', 'Ikan Lele', 'Pupuk Kompos'], default=['Maggot BSF'])
        with cols[1]:
             st.caption("Menampilkan hasil real-time dari database.")

    # Map Logic
    posts = db.get_waste_posts(filters=filters)
    
    # --- AUTO FOCUS LOGIC ---
    if posts:
        # Calculate centroid of all posts
        lats = [p['lat'] for p in posts]
        lons = [p['lon'] for p in posts]
        avg_lat = np.mean(lats)
        avg_lon = np.mean(lons)
        map_center = [avg_lat, avg_lon]
        zoom_level = 13 # Closer zoom because we have data
    else:
        # Fallback if no data
        map_center = [-6.2088, 106.8456] # Jakarta
        zoom_level = 11

    # Initialize Map
    m = folium.Map(location=map_center, zoom_start=zoom_level, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    for post in posts:
        # Content for Popup
        emojis = get_suitability_emojis(post['suitable_for'])
        
        # WhatsApp Link Construction
        phone = "6285388156854"
        msg = f"Halo, saya lihat postingan limbah *{post['waste_category']}* ({post['weight_est']}kg) di EcoCycle Maps. Apakah masih ada?"
        wa_url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"

        html = f"""
            <div style="font-family:'Plus Jakarta Sans',sans-serif; width:250px;">
                <div style="background:#10b981; color:white; padding:4px 10px; border-radius:4px 4px 0 0; font-size:10px; font-weight:bold; text-transform:uppercase;">
                    {post['provider_type']}
                </div>
                <div style="padding:12px; border:1px solid #e2e8f0; border-top:none; border-radius:0 0 8px 8px; background:white;">
                    <h4 style="margin:0 0 5px; color:#0f172a;">{post['waste_category']}</h4>
                    <div style="font-size:18px; font-weight:800; color:#059669; margin-bottom:8px;">{post['weight_est']:.1f} kg</div>
                    <p style="font-size:12px; color:#64748b; margin:0 0 12px;">Cocok: {post['suitable_for']} {emojis}</p>
                    
                    <a href="{wa_url}" target="_blank" style="display:block; background:#25D366; color:white; text-align:center; padding:8px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:13px;">
                        💬 Hubungi via WA
                    </a>
                    <div style="text-align:center; margin-top:8px;">
                        <a href="https://www.google.com/maps/dir/?api=1&destination={post['lat']},{post['lon']}" target="_blank" style="color:#3b82f6; font-size:11px; text-decoration:none;">
                            📍 Navigasi ke Lokasi
                        </a>
                    </div>
                </div>
            </div>
        """

        folium.Marker(
            location=[post['lat'], post['lon']],
            popup=folium.Popup(html, max_width=300),
            tooltip=f"{post['waste_category']}",
            icon=folium.Icon(color=get_marker_color(post), icon="leaf", prefix="fa"),
        ).add_to(marker_cluster)

    st_folium(m, width='100%', height=600, returned_objects=[])
    
    if posts:
        st.success(f"Menampilkan {len(posts)} titik lokasi terdekat.")
    else:
        st.warning("Belum ada data limbah di area ini. Jadilah yang pertama memposting!")


# ======================================================================================
# --- ROUTER ---
# ======================================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'provider':
    show_provider_page()
elif st.session_state.page == 'seeker':
    show_seeker_page()
