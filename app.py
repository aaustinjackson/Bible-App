import streamlit as st
import json
import os

JSON_FILE = "verses.json"

# --- Load Data ---
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

if "data" not in st.session_state:
    st.session_state.data = data

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

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
st.session_state.selected_topic = selected_topic

# --- Main page ---
st.subheader("Topics")

for topic_name in st.session_state.data.keys():
    with st.expander(topic_name, expanded=(topic_name == st.session_state.selected_topic)):
        # Display existing verses
        for i, verse in enumerate(st.session_state.data[topic_name]):
            st.markdown(f"**{verse['title']}**")
            st.markdown(verse['content'])
            if verse['note']:
                st.markdown(f"_Note: {verse['note']}_")

            # Delete button
            if st.button(f"🗑 Delete {verse['title']}", key=f"del_{topic_name}_{i}"):
                st.session_state.data[topic_name].pop(i)
                with open(JSON_FILE, "w") as f:
                    json.dump(st.session_state.data, f, indent=4)
                st.experimental_rerun()  # rerun to refresh after deletion

        # Add new verse (outside delete buttons)
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
                # Save immediately to local JSON
                with open(JSON_FILE, "w") as f:
                    json.dump(st.session_state.data, f, indent=4)
                st.success(f"Verse '{title}' added!")
                # Clear inputs
                st.session_state[f"title_{topic_name}"] = ""
                st.session_state[f"content_{topic_name}"] = ""
                st.session_state[f"note_{topic_name}"] = ""
                st.experimental_rerun()
