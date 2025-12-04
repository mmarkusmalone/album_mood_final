from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

# Import your existing query function. Assumes query_data.py is in the same folder
# and exposes `query_vibe_console` as in your pasted file.
from backend.query_data import query_vibe_console

app = Flask(__name__)
CORS(app)

# Path to the uploaded descriptors CSV (you mentioned it's available at /mnt/data/music_descriptors_3000.csv)
DESCRIPTORS_CSV = os.environ.get("DESCRIPTORS_CSV", "/data_cleaning_data/music_descriptors_3000.csv")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "building_embedding_data")

# Load descriptors once at startup
try:
    df_desc = pd.read_csv(DESCRIPTORS_CSV)
    # Expect a single column containing descriptor text — try to pick the first text column
    first_text_col = None
    for c in df_desc.columns:
        if df_desc[c].dtype == object:
            first_text_col = c
            break
    descriptors = (df_desc[first_text_col].dropna().astype(str).tolist()[:3000]) if first_text_col else []
except Exception as e:
    print("Failed to load descriptors csv:", e)
descriptors = []

@app.route('/api/descriptors')
def get_descriptors():
# Return a short curated list for the UI (first 120)
    return jsonify(descriptors[:120])

@app.route('/api/query', methods=['POST'])
def query():
    payload = request.get_json() or {}
    vibe = payload.get('vibe', '')
    extras = payload.get('extras', []) or []
    # Build final query string: user's text + joined extras
    extras_text = ' '.join(extras)
    final_query = (vibe + ' ' + extras_text).strip()

    # fall back
    if not final_query:
        return jsonify({ 'results': [], 'error': 'empty query' }), 400

# call your function. it returns a list of dicts.
    try:
        topk = query_vibe_console(final_query, top_k=12)
    except Exception as e:
        return jsonify({ 'results': [], 'error': str(e) }), 500

    return jsonify({ 'results': topk })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)