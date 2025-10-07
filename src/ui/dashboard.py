import json
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Edge CCTV Dashboard", layout="wide")
st.title("Edge CCTV Analytics")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Recent Events")
    path = Path("artifacts/normalized/events.log")
    if path.exists():
        events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
        for event in events[-20:]:
            st.json(event)
    else:
        st.info("No events yet")

with col2:
    st.subheader("Placeholders")
    placeholders = Path("docs/placeholders.md").read_text(encoding="utf-8")
    st.markdown(placeholders)
