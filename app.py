import streamlit as st
import json
import os

# --- Load Data ---
if os.path.exists("verses.json"):
    with open("verses.json", "r") as f:
        data = json.load(f)
else:
    data = {}

if "data" not in st.session_state:
    st.session_state.data = data

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""

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
            with open("verses.json", "w") as f:
                json.dump(st.session_state.data, f, indent=4)
            st.sidebar.success(f"Topic '{new_topic}' added!")

# Topic selection
selected_topic = st.sidebar.selectbox(
    "Select Topic", [""] + list(st.session_state.data.keys())
)
st.session_state.selected_topic = selected_topic

# --- Main App ---
if st.session_state.selected_topic == "":
    st.subheader("Please select a topic from the sidebar")
else:
    topic = st.session_state.selected_topic
    st.header(f"📁 {topic}")

    # Add new verse
    with st.expander("➕ Add New Verse"):
        title = st.text_input("Verse Title / Reference")
        content = st.text_area("Verse Content")
        note = st.text_area("Personal Note")

        if st.button("💾 Save Verse"):
            if title and content:
                st.session_state.data[topic].append({
                    "title": title,
                    "content": content,
                    "note": note
                })
                # Save immediately to JSON
                with open("verses.json", "w") as f:
                    json.dump(st.session_state.data, f, indent=4)
                st.success("Verse added!")

    # Display existing verses
    st.subheader("📄 Verses")
    for i, verse in enumerate(st.session_state.data[topic]):
        st.markdown(f"**{verse['title']}**")
        st.markdown(verse['content'])
        if verse['note']:
            st.markdown(f"_Note: {verse['note']}_")

        # Delete verse
        if st.button(f"🗑 Delete {verse['title']}", key=f"del_{i}"):
            st.session_state.data[topic].pop(i)
            with open("verses.json", "w") as f:
                json.dump(st.session_state.data, f, indent=4)
            st.success(f"Deleted verse: {verse['title']}")
