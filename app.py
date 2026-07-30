import os
import json
import base64
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="TirtaBot - Asisten AI Sentimen & Opini dr. Tirta",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_logo_base64():
    logo_path = os.path.join("static", "logo-tirta.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
        except: pass
    return "https://img.icons8.com/color/96/medical-doctor.png"

logo_b64 = get_logo_base64()

# Modern Custom CSS Styling System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp { background: linear-gradient(180deg, #F4F9FC 0%, #EAF3FB 100%); }
    
    .chat-header-container {
        display: flex; align-items: center; gap: 12px;
        background-color: #ffffff; padding: 1rem 1.5rem;
        border: 1px solid #e2e8f0; border-radius: 16px; margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .chat-header-avatar { width: 46px; height: 46px; border-radius: 50%; object-fit: cover; border: 2px solid #0EA5B7; }
    .chat-header-title { font-size: 1.3rem; font-weight: 800; color: #0EA5B7 !important; margin: 0; }
    .chat-header-subtitle { font-size: 0.825rem; color: #475569 !important; margin: 0; }
    
    .sidebar-brand-container { display: flex; align-items: center; gap: 12px; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 1rem; }
    .sidebar-brand-logo { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; border: 2px solid #0EA5B7; }
    .sidebar-brand-title { font-size: 1.4rem; font-weight: 800; color: #0EA5B7 !important; margin: 0; }
    
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important; border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important; color: #0f172a !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important; padding: 1rem !important; margin-bottom: 0.75rem !important;
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] li { color: #0f172a !important; }
    
    .promo-card { background: linear-gradient(135deg, #0EA5B7 0%, #2E9BE6 100%); color: white; padding: 1.1rem; border-radius: 18px; margin-top: 1rem; }
    .promo-card-title { font-size: 1rem; font-weight: 800; margin-bottom: 4px; }
    .promo-card-text { font-size: 0.75rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 8px; }
    .promo-card-badge { background-color: white; color: #0EA5B7; font-size: 0.7rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-block; }
    
    .badge-pos { background-color: #d1fae5; color: #065f46; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700; }
    .badge-neu { background-color: #e0f2fe; color: #075985; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700; }
    .badge-neg { background-color: #fee2e2; color: #991b1b; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: 700; }
    
    .citation-card { background-color: #ffffff; border-left: 4px solid #0EA5B7; padding: 0.85rem; border-radius: 0 10px 10px 0; margin-top: 0.6rem; font-size: 0.85rem; }
    .sentiment-summary-box { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 1rem; margin-bottom: 1rem; }
    
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"], .stChatInputContainer, footer { background-color: transparent !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# Cache RAG Engine Instance
@st.cache_resource
def load_rag_engine():
    try:
        from rag_system import DoctorTirtaRAG
        return DoctorTirtaRAG()
    except Exception as e:
        st.error(f"Gagal memuat RAG engine: {e}")
        return None

rag_engine = load_rag_engine()

# Sidebar Navigation
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand-container">
        <img src="{logo_b64}" class="sidebar-brand-logo">
        <div class="sidebar-brand-title">TirtaBot</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ Chat Baru", use_container_width=True, type="primary"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Halo! Saya **TirtaBot** 🩺. Saya adalah Asisten AI yang siap membantumu mengetahui bagaimana **kecenderungan respon, opini, serta sentimen masyarakat** terhadap dr. Tirta Mandira Hudhi dalam berbagai isu (kesehatan, bisnis sepatu lokal, kebijakan, profesi dokter, maupun personal).\n\nAda topik atau isu apa yang ingin kamu tanyakan?",
            "citations": []
        }]
        st.rerun()
        
    st.markdown("### 📋 Template Pertanyaan")
    selected_preset = None
    preset_options = [
        ("🩺 Gaya Hidup Sehat & Medis", "Saran dan himbauan utama dokter Tirta tentang gaya hidup sehat diabetes dan olahraga"),
        ("👟 Review Sepatu Lari Lokal", "Pendapat netizen tentang kualitas sepatu lari brand lokal Indonesia seperti Ortuseight dan 910"),
        ("👨‍⚕️ Realitas Profesi Dokter", "Tanggapan netizen mengenai isu gaji dokter umum dan perjuangan tenaga medis di daerah"),
        ("🗣️ Opini Podcast & Kebijakan", "Perdebatan pro dan kontra netizen terkait ketegasan gaya bicara dokter Tirta di podcast Deddy Corbuzier"),
        ("❤️ Perubahan Sikap Demi Anak", "Respon penonton podcast PWK mengenai perubahan sikap emosi dokter Tirta yang lebih tenang demi anak")
    ]
    for label, query in preset_options:
        if st.button(label, use_container_width=True):
            selected_preset = query
            
    st.markdown("---")
    st.markdown("""
    <div class="promo-card">
        <div class="promo-card-title">TirtaBot</div>
        <div class="promo-card-text">Asisten AI cerdas untuk mengetahui kecenderungan respon & sentimen masyarakat terhadap dr. Tirta Mandira Hudhi.</div>
        <div class="promo-card-badge">24.325 Komentar Analisis</div>
    </div>
    """, unsafe_allow_html=True)

# Main Chat Interface
st.markdown(f"""
<div class="chat-header-container">
    <img src="{logo_b64}" class="chat-header-avatar">
    <div>
        <div class="chat-header-title">Halo! Saya TirtaBot 👋</div>
        <div class="chat-header-subtitle">Asisten AI Sentimen & Opini Publik dr. Tirta</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Halo! Saya **TirtaBot** 🩺. Saya adalah Asisten AI yang siap membantumu mengetahui bagaimana **kecenderungan respon, opini, serta sentimen masyarakat** terhadap dr. Tirta Mandira Hudhi dalam berbagai isu (kesehatan, bisnis sepatu lokal, kebijakan, profesi dokter, maupun personal).\n\nAda topik atau isu apa yang ingin kamu tanyakan?",
        "citations": []
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨‍⚕️" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander(f"📚 Lihat Rujukan Dokumen & Sitasi Komentar ({len(msg['citations'])} Referensi)"):
                for idx, src in enumerate(msg["citations"], 1):
                    sent = src.get('sentiment', 'Netral')
                    badge_cls = "badge-pos" if sent == "Positif" else ("badge-neg" if sent == "Negatif" else "badge-neu")
                    st.markdown(f"""
                    <div class="citation-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <b>[{idx}] {src.get('author', 'Anonim')}</b>
                            <span class="{badge_cls}">{sent}</span>
                        </div>
                        <p style="margin: 4px 0; color: #334155; font-style: italic;">"{src.get('text', '')}"</p>
                        <div style="font-size: 0.75rem; color: #94a3b8; display:flex; justify-content:space-between; margin-top: 4px;">
                            <span>👍 {src.get('votes', 0)} likes | Skor Relevansi: {src.get('score', 0):.4f}</span>
                            <a href="{src.get('video_url', '#')}" target="_blank" style="color: #0EA5B7; font-weight: 600; text-decoration: none;">🔗 Lihat Video</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Quick Action Pills
st.markdown('<div style="font-size: 0.95rem; font-weight: 800; color: #0f172a; margin-bottom: 8px;">💡 Rekomendasi Topik Cepat:</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)
pill_selected = None
if col1.button("🩺 Gaya Hidup Sehat", use_container_width=True): pill_selected = "Himbauan kesehatan & gaya hidup sehat diabetes dr Tirta"
if col2.button("👟 Sepatu Lari Lokal", use_container_width=True): pill_selected = "Kualitas & opini sepatu lari brand lokal Indonesia"
if col3.button("👨‍⚕️ Gaji & Medis", use_container_width=True): pill_selected = "Tanggapan isu gaji dokter umum & realitas tenaga medis"
if col4.button("🗣️ Opini Podcast", use_container_width=True): pill_selected = "Perdebatan gaya bicara tegas dokter Tirta di podcast Deddy Corbuzier"
if col5.button("❤️ Sikap Demi Anak", use_container_width=True): pill_selected = "Respon penonton podcast PWK perubahan sikap dr Tirta demi anak"

user_input = st.chat_input("Tanyakan isu/topik tentang dr. Tirta di sini...")
prompt = selected_preset or pill_selected or user_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt, "citations": []})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    with st.chat_message("assistant", avatar="👨‍⚕️"):
        with st.spinner("TirtaBot sedang menganalisis sentimen & mencari rujukan dokumen..."):
            if rag_engine is not None:
                answer_summary, sources, sent_counts = rag_engine.generate_rag_response(prompt)
                
                total_s = len(sources) if len(sources) > 0 else 1
                pos_pct = round((sent_counts.get("Positif", 0) / total_s) * 100)
                neu_pct = round((sent_counts.get("Netral", 0) / total_s) * 100)
                neg_pct = max(0, 100 - pos_pct - neu_pct)
                
                st.markdown(f"""
                <div class="sentiment-summary-box">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                        Distribusi Sentimen Rujukan ({len(sources)} Komentar Relevan)
                    </div>
                    <div style="display: flex; gap: 8px; margin-bottom: 8px;">
                        <span class="badge-pos">Positif: {pos_pct}%</span>
                        <span class="badge-neu">Netral: {neu_pct}%</span>
                        <span class="badge-neg">Negatif: {neg_pct}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(answer_summary)
                
                if sources:
                    with st.expander(f"📚 Lihat Rujukan Dokumen & Sitasi Komentar ({len(sources)} Referensi)"):
                        for idx, src in enumerate(sources, 1):
                            sent = src.get('sentiment', 'Netral')
                            badge_cls = "badge-pos" if sent == "Positif" else ("badge-neg" if sent == "Negatif" else "badge-neu")
                            st.markdown(f"""
                            <div class="citation-card">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <b>[{idx}] {src.get('author', 'Anonim')}</b>
                                    <span class="{badge_cls}">{sent}</span>
                                </div>
                                <p style="margin: 4px 0; color: #334155; font-style: italic;">"{src.get('text', '')}"</p>
                                <div style="font-size: 0.75rem; color: #94a3b8; display:flex; justify-content:space-between; margin-top: 4px;">
                                    <span>👍 {src.get('votes', 0)} likes | Skor Relevansi: {src.get('score', 0):.4f}</span>
                                    <a href="{src.get('video_url', '#')}" target="_blank" style="color: #0EA5B7; font-weight: 600; text-decoration: none;">🔗 Lihat Video</a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                st.session_state.messages.append({"role": "assistant", "content": answer_summary, "citations": sources})
            else:
                st.error("Sistem TirtaBot RAG mengalami masalah teknis.")
