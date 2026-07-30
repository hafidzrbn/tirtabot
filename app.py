import os
import json
import pandas as pd
import numpy as np
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TirtaBot - Asisten AI Sentimen & Opini dr. Tirta",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Chat Interface
st.markdown("""
<style>
    .bot-header {
        text-align: center;
        padding-bottom: 1rem;
    }
    .bot-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.1rem;
    }
    .bot-subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .sentiment-badge-pos {
        background-color: #d1fae5;
        color: #065f46;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .sentiment-badge-neu {
        background-color: #e0f2fe;
        color: #075985;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .sentiment-badge-neg {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .citation-box {
        background-color: #f8fafc;
        border-left: 3px solid #3b82f6;
        padding: 0.8rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Cache RAG Engine
@st.cache_resource
def load_rag_engine():
    try:
        from rag_system import DoctorTirtaRAG
        return DoctorTirtaRAG()
    except Exception as e:
        st.error(f"Gagal memuat sistem RAG: {e}")
        return None

rag_engine = load_rag_engine()

# Sidebar: TirtaBot Info & Presets
st.sidebar.image("https://img.icons8.com/color/96/medical-doctor.png", width=75)
st.sidebar.title("TirtaBot 🩺")
st.sidebar.markdown("**Asisten AI Sentimen & Opini Publik**")
st.sidebar.markdown("Menjawab pertanyaan Anda berdasarkan analisis **24.325 komentar masyarakat** dari 10 video YouTube populer tentang dr. Tirta Mandira Hudhi.")

st.sidebar.divider()
st.sidebar.subheader("💡 Rekomendasi Topik Pertanyaan")

preset_queries = [
    "🩺 Himbauan kesehatan & gaya hidup sehat dr Tirta",
    "👟 Kualitas & opini sepatu lari brand lokal Indonesia",
    "👨‍⚕️ Tanggapan isu gaji dokter & realitas medis",
    "🗣️ Perdebatan gaya bicara tegas di podcast Deddy Corbuzier",
    "❤️ Respon perubahan sikap dr Tirta demi anaknya di PWK"
]

selected_preset = None
for q in preset_queries:
    if st.sidebar.button(q, use_container_width=True):
        selected_preset = q.split(" ", 1)[1] # Strip emoji prefix

st.sidebar.divider()
if st.sidebar.button("🗑️ Bersihkan Riwayat Chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.sidebar.caption("UAS Trending Topics on Statistics © 2026")

# Header Section
st.markdown("""
<div class="bot-header">
    <div class="bot-title">🩺 TirtaBot</div>
    <div class="bot-subtitle">Asisten AI Intelijen Sentimen & Opini Masyarakat terhadap <b>dr. Tirta Mandira Hudhi</b></div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State Messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! Saya **TirtaBot** 🩺. Saya adalah Asisten AI yang siap membantumu mengetahui bagaimana **kecenderungan respon, opini, serta sentimen masyarakat** terhadap dr. Tirta Mandira Hudhi dalam berbagai isu (kesehatan, bisnis sepatu lokal, kebijakan, profesi dokter, maupun personal).\n\nAda topik atau isu apa yang ingin kamu tanyakan?",
            "citations": []
        }
    ]

# Display Existing Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👨‍⚕️" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander("📚 Lihat Rujukan Dokumen & Sitasi Komentar (5 Referensi)"):
                for idx, src in enumerate(msg["citations"], 1):
                    sent = src.get('sentiment', 'Netral')
                    badge_class = "sentiment-badge-pos" if sent == "Positif" else ("sentiment-badge-neg" if sent == "Negatif" else "sentiment-badge-neu")
                    
                    st.markdown(f"""
                    <div class="citation-box">
                        <b>[{idx}] {src['author']}</b> <span class="{badge_class}">{sent}</span> (👍 {src['votes']} likes)<br>
                        <i>"{src['text']}"</i><br>
                        <small>🔗 Sumber Video: <a href="{src['video_url']}" target="_blank">{src['video_url']}</a> (ID: {src['video_id']}) | Skor Relevansi: {src['score']:.4f}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Handle Input Query (from User Typing or Sidebar Preset Button)
prompt_input = st.chat_input("Tanyakan isu/topik tentang dr. Tirta di sini...")
prompt = selected_preset if selected_preset else prompt_input

if prompt:
    # 1. Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt, "citations": []})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # 2. Generate Assistant Response via RAG
    with st.chat_message("assistant", avatar="👨‍⚕️"):
        with st.spinner("TirtaBot sedang menganalisis sentimen & mencari rujukan dokumen..."):
            if rag_engine is not None:
                answer_summary, sources, sent_counts = rag_engine.generate_rag_response(prompt)
                
                total_s = len(sources) if len(sources) > 0 else 1
                pos_pct = int((sent_counts.get("Positif", 0) / total_s) * 100)
                neu_pct = int((sent_counts.get("Netral", 0) / total_s) * 100)
                neg_pct = int((sent_counts.get("Negatif", 0) / total_s) * 100)
                
                # Format Response Content
                response_text = f"### 📊 Kecenderungan Sentimen & Opini Publik\n"
                response_text += f"* **Positif**: {pos_pct}% | **Netral**: {neu_pct}% | **Negatif**: {neg_pct}%\n\n"
                response_text += f"---\n\n"
                response_text += answer_summary
                
                st.markdown(response_text)
                
                if sources:
                    with st.expander("📚 Lihat Rujukan Dokumen & Sitasi Komentar (5 Referensi)"):
                        for idx, src in enumerate(sources, 1):
                            sent = src.get('sentiment', 'Netral')
                            badge_class = "sentiment-badge-pos" if sent == "Positif" else ("sentiment-badge-neg" if sent == "Negatif" else "sentiment-badge-neu")
                            
                            st.markdown(f"""
                            <div class="citation-box">
                                <b>[{idx}] {src['author']}</b> <span class="{badge_class}">{sent}</span> (👍 {src['votes']} likes)<br>
                                <i>"{src['text']}"</i><br>
                                <small>🔗 Sumber Video: <a href="{src['video_url']}" target="_blank">{src['video_url']}</a> (ID: {src['video_id']}) | Skor Relevansi: {src['score']:.4f}</small>
                            </div>
                            """, unsafe_allow_html=True)
                            
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text,
                    "citations": sources
                })
            else:
                st.error("Maaf, sistem TirtaBot RAG mengalami masalah teknis saat memuat data.")
