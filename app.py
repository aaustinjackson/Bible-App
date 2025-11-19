import streamlit as st
import json
import os

# --- Page Setup ---
st.set_page_config(page_title="Bible Notebook", layout="wide")
st.markdown("""
<style>
/* Card styling */
.card {
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
    background-color: #f5f5f5;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.card:hover {
    background-color: #e0f7fa;
}
.title {
    font-size: 18px;
    font-weight: bold;
}
.note {
    font-style: italic;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# --- Load Data ---
if os.path.exists("verses.json"):
    with open("verses.json", "r") as f:
        data = json.load(f)
else:
    data = {}

# --- Sidebar: Topic Management ---
st.sidebar.header("📁 Topics")
new_topic = st.sidebar.text_input("New Topic")
if st.sidebar.button("➕ Add Topic"):
    if new_topic:
        if new_topic in data:
            st.sidebar.warning("Topic exists")
        else:
            data[new_topic] = []
            with open("verses.json", "w") as f:
                json.dump(data, f, indent=4)
            st.sidebar.success(f"Topic '{new_topic}' added!")

st.sidebar.markdown("---")
selected_topic = st.sidebar.selectbox("Select Topic", [""] + list(data.keys()))

# --- Main App ---
st.title("📖 Bible Notebook")

# --- Folder Grid View ---
if not selected_topic:
    st.subheader("Topics")
    cols = st.columns(2)
    colors = ["#FFCDD2","#C8E6C9","#BBDEFB","#FFF9C4","#D1C4E9"]  # color palette
    for i, topic in enumerate(data.keys()):
        col = cols[i % 2]
        color = colors[i % len(colors)]
        with col:
            if st.button(f"📂 {topic}", key=f"topic_{i}"):
                selected_topic = topic
            st.markdown(f"<div style='background-color:{color};border-radius:10px;padding:10px;text-align:center;margin-top:5px'>{topic}</div>", unsafe_allow_html=True)

else:
    st.header(f"📁 {selected_topic}")

    # --- Add Verse Card ---
    with st.expander("➕ Add New Verse", expanded=True):
        title = st.text_input("Verse Title / Reference")
        content = st.text_area("Verse Content")
        note = st.text_area("Personal Note")
        if st.button("💾 Save Verse"):
            if title and content:
                data[selected_topic].append({"title": title, "content": content, "note": note})
                with open("verses.json", "w") as f:
                    json.dump(data, f, indent=4)
                st.success(f"Verse '{title}' added!")

    # --- Display Existing Verses ---
    st.subheader("📄 Verses")
    for i, verse in enumerate(data[selected_topic]):
        with st.container():
            st.markdown(f"<div class='card'><div class='title'>📜 {verse['title']}</div><p>{verse['content']}</p>", unsafe_allow_html=True)
            if verse['note']:
                st.markdown(f"<p class='note'>💡 {verse['note']}</p></div>", unsafe_allow_html=True)
            else:
                st.markdown("</div>", unsafe_allow_html=True)
            # Delete button
            if st.button(f"🗑 Delete {verse['title']}", key=f"del_{i}"):
                data[selected_topic].pop(i)
                with open("verses.json", "w") as f:
                    json.dump(data, f, indent=4)
                st.experimental_rerun()
