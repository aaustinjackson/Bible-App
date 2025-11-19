import streamlit as st
import json
import os

JSON_FILE = "verses.json"

# --- Load data ---
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

if "data" not in st.session_state:
    st.session_state.data = data

st.set_page_config(page_title="Bible Notebook", layout="wide")
st.title("📖 Bible Notebook")

# --- Sidebar ---
st.sidebar.header("📁 Topics")
new_topic = st.sidebar.text_input("New Topic")
if st.sidebar.button("➕ Add Topic"):
    if new_topic and new_topic not in st.session_state.data:
        st.session_state.data[new_topic] = []
        with open(JSON_FILE, "w") as f:
            json.dump(st.session_state.data, f, indent=4)
        st.sidebar.success(f"Topic '{new_topic}' added!")

selected_topic = st.sidebar.selectbox(
    "Select Topic", [""] + list(st.session_state.data.keys())
)

# --- Main page ---
st.subheader("Topics")

for topic_name in st.session_state.data.keys():
    with st.expander(topic_name, expanded=(topic_name == selected_topic)):
        # Display existing verses
        verses = st.session_state.data[topic_name]
        for i, verse in enumerate(verses):
            st.markdown(f"**{verse['title']}**")
            st.markdown(verse['content'])
            if verse['note']:
                st.markdown(f"_Note: {verse['note']}_")
            
            # Delete button
            if st.button(f"🗑 Delete {verse['title']}", key=f"del_{topic_name}_{i}"):
                st.session_state.data[topic_name].pop(i)
                with open(JSON_FILE, "w") as f:
                    json.dump(st.session_state.data, f, indent=4)
                st.success(f"Deleted verse: {verse['title']}")

        # Add new verse form (use local variables, not session_state)
        with st.form(f"add_verse_form_{topic_name}"):
            title = st.text_input("Verse Title / Reference")
            content = st.text_area("Verse Content")
            note = st.text_area("Personal Note")
            submitted = st.form_submit_button("💾 Save Verse")
            if submitted and title and content:
                st.session_state.data[topic_name].append({
                    "title": title,
                    "content": content,
                    "note": note
                })
                with open(JSON_FILE, "w") as f:
                    json.dump(st.session_state.data, f, indent=4)
                st.success(f"Verse '{title}' added!")
