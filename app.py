# app.py
import streamlit as st
from backend.query_data import query_vibe_console
import os

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Album Vibe Search",
    page_icon="🎧",
    layout="centered"
)

# ========== CUSTOM CSS ==========
SCANDINAVIAN_CSS = """
<style>
:root{
  --bg: #fffcf0;
  --navy: #040a29;
  --chip-border: #e6e1d8;
  --card-bg: #ffffff;
}

body, .stApp {
  background-color: var(--bg) !important;
  color: var(--navy) !important;
  font-family: 'Inter', sans-serif;
}

h1, h2, h3, label, p, div {
  color: var(--navy) !important;
}

.result-card {
  padding: 0.9rem;
  border-radius: 10px;
  background: var(--card-bg);
  border: 1px solid #dedacf;
  margin-bottom: 0.9rem;
}

.result-title { font-size:1rem; font-weight:600; color:var(--navy); }
.result-meta { font-size:0.85rem; color:#556; }
.result-review { margin-top:0.35rem; font-size:0.85rem; color:var(--navy); }

/* input styling */
.stTextInput>div>div>input {
  background-color: white !important;
  border-radius: 8px !important;
  border: 1px solid #ccc !important;
  padding: 0.6rem !important;
  color: var(--navy) !important;
}

/* primary search button */
.primary-search-button button {
  background-color: var(--navy) !important;
  color: var(--bg) !important;
  border-radius: 8px !important;
  padding: 0.5rem 0.9rem !important;
  border: none !important;
  font-weight: 600;
}

/* minor responsive tweak */
@media (max-width:640px) {
  .result-title { font-size:0.98rem; }
  .result-meta, .result-review { font-size:0.82rem; }
}
</style>
"""
st.markdown(SCANDINAVIAN_CSS, unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown("<h1 style='text-align:center; margin-top:18px;'>🎧 Album Vibe Search</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; margin-bottom:6px;'>Type a vibe (mood, genre, adjectives) and press Search.</p>", unsafe_allow_html=True)

# ========== INPUT ==========
query = st.text_input("Enter vibe text:", placeholder="e.g., dreamy nostalgic indie folk")

top_k = st.slider("Results to return", 5, 20, 5)

search_col1, search_col2 = st.columns([3, 1])
with search_col2:
    st.markdown('<div class="primary-search-button">', unsafe_allow_html=True)
    search_btn = st.button("Search")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== SEARCH LOGIC ==========
if search_btn:
    q_text = (query or "").strip()
    if not q_text:
        st.warning("Please enter a query (describe the vibe you want).")
    else:
        with st.spinner("Searching for matching albums..."):
            try:
                results = query_vibe_console(q_text, top_k=top_k)
            except Exception as e:
                st.error(f"Error running search: {e}")
                results = []

        st.markdown("---")
        st.subheader(f"Top {len(results)} Results for: «{q_text}»")
        if not results:
            st.info("No results found.")
        for r in results:
            artist = r.get("artist", "") or ""
            title = r.get("title", "") or ""
            genre = r.get("genre", "") or ""
            year = r.get("year_released", "") or ""
            score = r.get("score", 0.0)
            review = r.get("review", "") or ""
            st.markdown(
                f"""
                <div class='result-card'>
                    <div class='result-title'>{r.get("rank","")}. {artist} — {title}</div>
                    <div class='result-meta'>{genre} • {year} • score={score:.4f}</div>
                    <div class='result-review'>{review}...</div>
                </div>
                """,
                unsafe_allow_html=True
            )
