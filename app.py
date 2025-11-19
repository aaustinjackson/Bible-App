import streamlit as st
import json
import os

# --- File path ---
JSON_FILE = "verses.json"

# --- Load data ---
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

# --- Session state ---
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

# --- Page Setup ---
st.set_page_config(page_title="Bible Notebook", layout="wide")
st.title("📖 Bible Notebook")

# --- Sidebar: Topic Management ---
st.sidebar.header("📁 Topics")

# Add new topic
new_topic = st.sidebar.text_input("New Topic")
if st.sidebar.button("➕ Add Topic"):
    if new_topic:
        if new_topic not in st.session_state.data:
            st.session_state.data[new_topic] = []
            # Save immediately to JSON
            with open(JSON_FILE, "w") as f:
                json.dump(st.session_state.data, f, indent=4)
            st.sidebar.success(f"Topic '{new_topic}' added!")

# Sidebar topic selectbox
selected_topic = st.sidebar.selectbox(
    "Select Topic", [""] + list(st.session_state.data.keys())
)
st.session_state.selected_topic = selected_topic

# --- Main Page: Topics as Expanders ---
st.subheader("Topics")
for topic_name in st.session_state.data.keys():
    with st.expander(topic_name, expanded=(topic_name == st.session_state.selected_topic)):
        # Show existing verses
        for i, verse in enumerate(st.session_state.data[topic_name]):
            st.markdown(f"**{verse['title']}**")
            st.markdown(verse['content'])
            if verse['note']:
                st.markdown(f"_Note: {verse['note']}_")

        # Add new verse under this topic
        with st.form(f"add_verse_form_{topic_name}"):
            title = st.text_input("Verse Title / Reference", key=f"title_{topic_name}")
            content = st.text_area("Verse Content", key=f"content_{topic_name}")
            note = st.text_area("Personal Note", key=f"note_{topic_name}")
            submitted = st.form_submit_button("💾 Save Verse")
            if submitted and title and content:
                st.session_state.data[topic_name].append({
                    "title": title,
                    "content": content,
                    "note": note
                })
                # Save immediately to JSON
                with open(JSON_FILE, "w") as f:
                    json.dump(st.session_state.data, f, indent=4)
                st.success(f"Verse '{title}' added!")
                # Clear form inputs
                st.session_state[f"title_{topic_name}"] = ""
                st.session_state[f"content_{topic_name}"] = ""
                st.session_state[f"note_{topic_name}"] = ""
