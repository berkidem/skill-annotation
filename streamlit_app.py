"""Quick test of streamlit-annotation-tools"""

import streamlit as st
!pip install streamlit_annotation_tools
from streamlit_annotation_tools import text_highlighter
import json

st.title("Testing streamlit-annotation-tools - TEXT HIGHLIGHTER")

# Test with multiple examples
examples = [
    {
        "id": "posting_1",
        "text": "We are looking for a Senior Software Engineer with 5+ years of experience in Python and Java. Must have strong problem-solving skills and experience with AWS."
    },
    {
        "id": "posting_2", 
        "text": "Data Scientist needed. Required: machine learning, TensorFlow, PyTorch, SQL, and R. Excellent communication skills required."
    }
]

# Select example
example_idx = st.selectbox("Select Example", range(len(examples)), format_func=lambda i: f"Example {i+1}: {examples[i]['text'][:50]}...")
current_example = examples[example_idx]

st.markdown("### Text Highlighter")
st.caption("Click words to highlight them as skills. Click X to remove. Click + to highlight more.")

# Use text_highlighter
annotations = text_highlighter(current_example['text'])

st.divider()

st.markdown("### 📊 Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Raw Return Value:**")
    st.write("Type:", str(type(annotations)))
    st.write("Value:")
    try:
        if annotations:
            st.json(annotations)
        else:
            st.info("No annotations yet")
    except Exception as e:
        st.error(f"Error displaying: {e}")
        st.code(repr(annotations))

with col2:
    st.markdown("**Parsed Skills:**")
    try:
        if annotations and isinstance(annotations, list) and len(annotations) > 0:
            # Handle nested list structure [[{...}, {...}]]
            actual_annotations = annotations[0] if isinstance(annotations[0], list) else annotations
            
            st.write(f"Total skills: {len(actual_annotations)}")
            
            for i, ann in enumerate(actual_annotations):
                if isinstance(ann, dict):
                    # text_highlighter returns 'label' field with the text
                    text = ann.get('label', ann.get('text', 'N/A'))
                    start = ann.get('start', '?')
                    end = ann.get('end', '?')
                    
                    st.write(f"{i+1}. **{text}**")
                    st.caption(f"   Position: {start}-{end}")
                    
                    # Verify the text matches
                    if isinstance(start, int) and isinstance(end, int):
                        extracted = current_example['text'][start:end]
                        matches = extracted == text
                        st.caption(f"   Extracted: '{extracted}' {'✓' if matches else '✗ MISMATCH'}")
                else:
                    st.write(f"{i+1}. {repr(ann)} (unexpected format)")
        else:
            st.info("Click words above to highlight them")
    except Exception as e:
        st.error(f"Error parsing: {e}")
        st.code(repr(annotations))

st.divider()

# Show how we'd save this
st.markdown("### 💾 How We'd Save This")

if st.button("Show Save Format"):
    if annotations and isinstance(annotations, list) and len(annotations) > 0:
        # Handle nested list structure
        actual_annotations = annotations[0] if isinstance(annotations[0], list) else annotations
        
        save_format = {
            "job_id": current_example['id'],
            "description": current_example['text'],
            "extracted_skills": [
                {
                    "text": ann.get('label', ann.get('text', '')),
                    "start": ann.get('start', 0),
                    "end": ann.get('end', 0),
                    "note": ""
                }
                for ann in actual_annotations if isinstance(ann, dict)
            ]
        }
        st.json(save_format)
        st.success(f"✅ This format matches our requirements perfectly! {len(save_format['extracted_skills'])} skills captured.")
    else:
        st.warning("Highlight some skills first")

st.divider()


