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
    color: black; /* Ensure text is black */
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
body, .stText, .stTextArea, .stTextInput {
    color: black !important; /* Ensure text is visible in dark mode */
}
</style>
""", unsafe_allow_html=True)

# --- Load or Initialize Data ---
if os.path.exists("verses.json"):
    with open("verses.json", "r") as f:
        data = json.load(f)
else:
    data = {}

# --- Session State Initialization ---
if "data" not in st.session_state:
    st.session_state.data = data

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

if "title_input" not in st.session_state:
    st.session_state.title_input = ""
if "content_input" not in st.session_state:
    st.session_state.content_input = ""
if "note_input" not in st.session_state:
    st.session_state.note_input = ""

# --- Sidebar: Topic Management ---
st.sidebar.header("📁 Topics")

# Add new topic
new_topic = st.sidebar.text_input("New Topic")
if st.sidebar.button("➕ Add Topic"):
    if new_topic:
        if new_topic in st.session_state.data:
            st.sidebar.warning("Topic exists")
        else:
            st.session_state.data[new_topic] = []
            with open("verses.json", "w") as f:
                json.dump(st.session_state.data, f, indent=4)
            st.sidebar.success(f"Topic '{new_topic}' added!")

st.sidebar.markdown("---")

# Sidebar selectbox for topic
selected = st.sidebar.selectbox(
    "Select Topic", [""] + list(st.session_state.data.keys()), index=0
)
st.session_state.selected_topic = selected  # update session_state on change

# --- Main App ---
st.title("📖 Bible Notebook")

# --- Folder Grid View ---
if st.session_state.selected_topic == "":
    st.subheader("Topics")
    cols = st.columns(2)
    colors = ["#FFCDD2","#C8E6C9","#BBDEFB","#FFF9C4","#D1C4E9"]  # color palette

    for i, topic in enumerate(st.session_state.data.keys()):
        col = cols[i % 2]
        color = colors[i % len(colors)]
        with col:
            if st.button(f"📂 {topic}", key=f"topic_{i}"):
                st.session_state.selected_topic = topic  # simply set session state
            st.markdown(
                f"<div style='background-color:{color};border-radius:10px;padding:10px;text-align:center;margin-top:5px;color:black'>{topic}</div>",
                unsafe_allow_html=True
            )

# --- Display Selected Topic ---
else:
    topic = st.session_state.selected_topic
    st.header(f"📁 {topic}")

    # --- Add Verse Card ---
    with st.expander("➕ Add New Verse", expanded=True):
        st.session_state.title_input = st.text_input("Verse Title / Reference", st.session_state.title_input)
        st.session_state.content_input = st.text_area("Verse Content", st.session_state.content_input)
        st.session_state.note_input = st.text_area("Personal Note", st.session_state.note_input)

        if st.button("💾 Save Verse"):
            if st.session_state.title_input and st.session_state.content_input:
                st.session_state.data[topic].append({
                    "title": st.session_state.title_input,
                    "content": st.session_state.content_input,
                    "note": st.session_state.note_input
                })
                with open("verses.json", "w") as f:
                    json.dump(st.session_state.data, f, indent=4)
                # Clear inputs
                st.session_state.title_input = ""
                st.session_state.content_input = ""
                st.session_state.note_input = ""
                st.success("Verse added!")

    # --- Display Existing Verses ---
    st.subheader("📄 Verses")
    for i, verse in enumerate(st.session_state.data[topic]):
        with st.container():
            st.markdown(
                f"<div class='card'><div class='title'>📜 {verse['title']}</div><p>{verse['content']}</p>",
                unsafe_allow_html=True
            )
            if verse['note']:
                st.markdown(f"<p class='note'>💡 {verse['note']}</p></div>", unsafe_allow_html=True)
            else:
                st.markdown("</div>", unsafe_allow_html=True)

            if st.button(f"🗑 Delete {verse['title']}", key=f"del_{i}"):
                st.session_state.data[topic].pop(i)
                with open("verses.json", "w") as f:
                    json.dump(st.session_state.data, f, indent=4)

    # --- Back Button ---
    if st.button("⬅ Back to Topics"):
        st.session_state.selected_topic = ""
