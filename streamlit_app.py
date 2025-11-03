import streamlit as st
import json
from pathlib import Path
from html import escape
from collections import defaultdict
import re

# ===============================
# 0) Figure discovery (ramenPics)
# ===============================
IMG_DIR = Path("ramenPics")

def _natural_key(p: Path):
    # Natural sort: ramenStep2 < ramenStep10
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.stem)]

def _build_caption(p: Path) -> str:
    # "ramenStep4" -> "Ramen Step 4"
    name = re.sub(r"[_\-]+", " ", p.stem).strip()
    return name.title()

def discover_figures(dirpath: Path):
    exts = ("*.png", "*.jpg", "*.jpeg", "*.svg", "*.webp")
    files = []
    for pat in exts:
        files.extend(dirpath.glob(pat))
    files = sorted(files, key=_natural_key)
    return [{"src": str(p), "caption": _build_caption(p)} for p in files]

FIGURES = discover_figures(IMG_DIR)

# ==========================================
# 1) Page Configuration & Academic Styling
# ==========================================
st.set_page_config(page_title="Scientific Hypothesis Viewer", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Source+Serif+Pro:wght@400;600;700&display=swap');

    body { font-family: 'Lato', sans-serif; color: #212529; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Source Serif Pro', serif; font-weight: 700; }
    .block-container { padding-top: 2rem; }
    hr { border-top: 1px solid #DEE2E6; }

    .main-header h1 { font-size: 2.5rem; color: #343A40; }
    .main-header p { font-size: 1.1rem; color: #6C757D; margin-top: -10px; }

    .paper-list-text { font-family: 'Source Serif Pro', serif; font-size: 1.1rem; }

    /* Dialog tweaks */
    div[data-testid="stDialog"] > div { max-width: 900px; }
    .summary-scroll { max-height: 75vh; overflow-y: auto; padding-right: 8px; }

    .summary-box { font-family: 'Lato', sans-serif; line-height: 1.6; }
    .summary-box h3 {
        font-family: 'Source Serif Pro', serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #000;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 0.5rem;
    }
    .summary-box h3:first-child { margin-top: 0; }
    .summary-box h4 { font-family: 'Lato', sans-serif; font-size: 1.1rem; font-weight: 700; color: #495057; margin-top: 1rem; }
    .summary-box p { margin-bottom: 0.5rem; }
    .summary-box ul { margin-bottom: 0.75rem; list-style-type: none; padding-left: 0; }
    .summary-box li { margin-bottom: 0.25rem; }
    .evidence-quote { background-color: #F8F9FA; border-left: 4px solid #CED4DA; padding: 10px 15px; margin: 10px 0 15px 0; font-style: italic; color: #495057; }
</style>
""", unsafe_allow_html=True)

# ==================================
# 2) Data Loading & Helper Functions
# ==================================
def extract_topics(data):
    subject_area = data.get("subject_area", {})
    if isinstance(subject_area, dict):
        areas = subject_area.get("areas", [])
        if areas and isinstance(areas, list):
            return [area.get("name", "Unknown Topic") for area in areas if isinstance(area, dict)]
    return ["Uncategorized"]

def get_sortable_date(data):
    """
    Returns YYYY.MM.DD or YYYY.MM or YYYY (as string) for descending sort.
    Falls back to year parsed from filename; '0000' if unknown.
    """
    date_str = data.get("published_at") or data.get("date") or data.get("pub_date")
    if isinstance(date_str, str):
        m = re.search(r'(\d{4})[-_/\.](\d{2})[-_/\.](\d{2})', date_str)
        if m:
            return f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
        m = re.search(r'(\d{4})[-_/\.](\d{2})', date_str)
        if m:
            return f"{m.group(1)}.{m.group(2)}"
        m = re.search(r'(\d{4})', date_str)
        if m:
            return m.group(1)
    year = data.get("year")
    if year:
        return str(year)
    filename = data.get("filename", "")
    m = re.search(r'(\d{4})', filename)
    if m:
        return m.group(1)
    return "0000"

@st.cache_data
def load_papers(json_dir: Path):
    papers = []
    if not json_dir.exists():
        st.error(f"Directory not found: {json_dir}")
        return []
    for file_path in sorted(json_dir.glob("*.json")):
        try:
            with file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                data['filename'] = file_path.name
                title = file_path.stem
                topics = extract_topics(data)
                sort_date = get_sortable_date(data)
                papers.append({"id": file_path.stem, "title": title, "topics": topics, "data": data, "sort_date": sort_date})
        except (json.JSONDecodeError, IOError) as e:
            st.warning(f"Could not read or parse {file_path.name}: {e}")
    return papers

# ================================
# 3) Summary Generation Functions
# ================================
def format_evidence(evidence):
    if not evidence: return ""
    html = '<div class="evidence-quote"><strong>Evidence:</strong> '
    if isinstance(evidence, list):
        html += "".join(f"<p style='margin:0;'>{escape(str(e))}</p>" for e in evidence)
    else:
        html += f"<p style='margin:0;'>{escape(str(evidence))}</p>"
    html += "</div>"
    return html

def render_answer_evidence(content):
    html = ""
    if isinstance(content, dict) and 'answer' in content:
        answer = content.get('answer')
        if isinstance(answer, list):
            html += "".join(f"<p>{escape(str(item))}</p>" for item in answer)
        else:
            html += f"<p>{escape(str(answer))}</p>"
        html += format_evidence(content.get("evidence"))
    return html

def render_list_section(items, title_key, desc_key):
    html = ""
    for item in items:
        if isinstance(item, dict):
            title = item.get(title_key, "N/A")
            desc = item.get(desc_key, "")
            html += f"<p><strong>{escape(str(title))}:</strong> {escape(str(desc))}</p>"
            html += format_evidence(item.get("evidence"))
        else:
            html += f"<p>{escape(str(item))}</p>"
    return html

def render_method(content):
    html = ""
    if content.get("steps"):
        html += "<h4>Steps</h4>"
        for step in content.get("steps", []):
            html += f"<p><strong>{escape(step.get('step', 'N/A'))}</strong></p>"
            html += f"<p style='padding-left: 15px;'><em>Input:</em> {escape(step.get('input', 'N/A'))}</p>"
            html += f"<p style='padding-left: 15px;'><em>Output:</em> {escape(step.get('output', 'N/A'))}</p>"
            html += format_evidence(step.get('evidence'))
    if content.get("tools"):
        html += "<h4>Tools</h4>" + render_list_section(content["tools"], "name", "description")
    if content.get("benchmark_datasets"):
        html += "<h4>Benchmark Datasets</h4>" + render_list_section(content["benchmark_datasets"], "name", "data_description")
    if content.get("evaluation_metrics"):
        html += "<h4>Evaluation Metrics</h4>" + render_list_section(content["evaluation_metrics"], "name", "purpose")
    return html

def render_performance_summary(content):
    html = ""
    if content.get("performance_summary"):
        html += "<h4>Performance</h4>" + render_list_section(content["performance_summary"], "summary", "")
    if content.get("baselines"):
        html += "<h4>Baselines</h4>" + render_list_section(content["baselines"], "name", "description")
    return html

def create_summary_text(paper_data):
    summary_html = ""
    section_order = [
        "objective", "knowledge_gap", "novelty", "inspirational_papers", "method", 
        "method_type", "subject_area", "performance_summary", "benchmark_dataset", 
        "limitations", "future_directions"
    ]
    render_map = {
        "objective": render_answer_evidence, "knowledge_gap": render_answer_evidence,
        "novelty": render_answer_evidence, "inspirational_papers": render_answer_evidence,
        "method": render_method,
        "method_type": lambda c: render_list_section(c.get("methods", []), "name", "description"),
        "subject_area": lambda c: render_list_section(c.get("areas", []), "name", "description"),
        "performance_summary": render_performance_summary,
        "benchmark_dataset": lambda c: f"<p>{escape(str(c))}</p>" if c else "<p>No benchmark dataset was used.</p>",
        "limitations": lambda c: render_list_section(c.get("limitations", []), "name", "description"),
        "future_directions": lambda c: render_list_section(c.get("future_directions", []), "name", "description"),
    }
    for key in section_order:
        content = paper_data.get(key)
        if key in render_map and content:
            title = key.replace('_', ' ').title()
            summary_html += f"<h3>{escape(title)}</h3>"
            summary_html += render_map[key](content)
    return summary_html if summary_html else "<p>No summary information could be generated.</p>"

# ============================
# 3b) Dialog helper
# ============================
def open_summary_dialog(title: str, html: str):
    @st.dialog(title, width="large")
    def _dlg():
        st.markdown(f'<div class="summary-box summary-scroll">{html}</div>', unsafe_allow_html=True)
    _dlg()

# ===========================================
# 3c) Streamlit-native Figure "Carousel"
# ===========================================
def render_figure_carousel(figures):
    if not figures:
        st.info("No figures found in 'ramenPics/'. Add images to that folder and reload.")
        return

    if "fig_idx" not in st.session_state:
        st.session_state.fig_idx = 0

    total = len(figures)
    with st.container():
        c1, c2, c3 = st.columns([0.12, 0.76, 0.12])
        with c1:
            if st.button("‹", key="fig_prev", use_container_width=True):
                st.session_state.fig_idx = (st.session_state.fig_idx - 1) % total
        with c2:
            slider_val = st.slider(
                "Figure",
                min_value=1,
                max_value=total,
                value=st.session_state.fig_idx + 1,
                label_visibility="collapsed",
            )
            st.session_state.fig_idx = slider_val - 1
        with c3:
            if st.button("›", key="fig_next", use_container_width=True):
                st.session_state.fig_idx = (st.session_state.fig_idx + 1) % total

        current = figures[st.session_state.fig_idx]
        st.image(current["src"], use_container_width=True, caption=current.get("caption", ""))

# =======================
# 4) Main Application
# =======================
json_dir = Path("Papers")
papers = load_papers(json_dir)

# Header
st.markdown(
    '<div class="main-header"><h1>Scientific Hypothesis Viewer</h1>'
    '<p>An interactive supplement to our journal submission, providing a structured view of the analyzed papers.</p></div>',
    unsafe_allow_html=True
)

# Figure carousel directly under header
render_figure_carousel(FIGURES)
st.markdown("<hr>", unsafe_allow_html=True)

# Search
search_query = st.text_input("Search papers by title (filename)", placeholder="Filter papers...")
filtered_papers = [p for p in papers if search_query.lower() in p['title'].lower()] if search_query else papers

# Dialog state
if "dlg_open" not in st.session_state:
    st.session_state.dlg_open = False
if "dlg_title" not in st.session_state:
    st.session_state.dlg_title = ""
if "dlg_html" not in st.session_state:
    st.session_state.dlg_html = ""

# Tabs
tab_topic, tab_all = st.tabs(["By Topic", "All by Date"])

with tab_topic:
    papers_by_topic = defaultdict(list)
    for paper in filtered_papers:
        for topic in paper.get('topics', ['Uncategorized']):
            papers_by_topic[topic].append(paper)

    if not papers_by_topic:
        st.info("No papers match your search query.")
    else:
        for topic in sorted(papers_by_topic.keys()):
            with st.expander(topic):
                papers_in_topic = papers_by_topic[topic]
                sorted_papers = sorted(papers_in_topic, key=lambda p: p.get('sort_date', '0'), reverse=True)

                for i, paper in enumerate(sorted_papers, start=1):
                    col1, col2 = st.columns([0.8, 0.2])
                    with col1:
                        st.markdown(
                            f'<div class="paper-list-text" style="padding: 8px 0;">{i}. {escape(paper["title"])}</div>',
                            unsafe_allow_html=True
                        )
                    with col2:
                        icon_col1, icon_col2 = st.columns(2)
                        with icon_col1:
                            resource_info = paper["data"].get("resource_link", {})
                            if isinstance(resource_info, dict):
                                resource_url = resource_info.get("answer")
                                if resource_url and isinstance(resource_url, str) and resource_url.strip().startswith("http"):
                                    st.link_button("Source", resource_url)
                                else:
                                    raw_answer = str(resource_info.get('answer', 'N/A')).strip()
                                    raw_evidence = str(resource_info.get('evidence', 'N/A')).strip()
                                    download_text = f"Answer: {raw_answer}\nEvidence: {raw_evidence}"
                                    st.download_button("Source", data=download_text, file_name=f"{paper['id']}_resource.txt", key=f"src_dl_topic_{topic}_{paper['id']}")
                            else:
                                download_text = f"Resource Info: {str(resource_info)}"
                                st.download_button("Source", data=download_text, file_name=f"{paper['id']}_resource.txt", key=f"src2_dl_topic_{topic}_{paper['id']}")
                        with icon_col2:
                            if st.button("Summary", key=f"btn_summary_topic_{topic}_{paper['id']}"):
                                summary_content = create_summary_text(paper['data'])
                                st.session_state.dlg_open = True
                                st.session_state.dlg_title = paper['title']
                                st.session_state.dlg_html = summary_content

with tab_all:
    if not filtered_papers:
        st.info("No papers match your search query.")
    else:
        sorted_all = sorted(filtered_papers, key=lambda p: p.get('sort_date', '0'), reverse=True)
        for i, paper in enumerate(sorted_all, start=1):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown(
                    f'<div class="paper-list-text" style="padding: 8px 0;">{i}. {escape(paper["title"])}</div>',
                    unsafe_allow_html=True
                )
            with col2:
                icon_col1, icon_col2 = st.columns(2)
                with icon_col1:
                    resource_info = paper["data"].get("resource_link", {})
                    if isinstance(resource_info, dict):
                        resource_url = resource_info.get("answer")
                        if resource_url and isinstance(resource_url, str) and resource_url.strip().startswith("http"):
                            st.link_button("Source", resource_url)
                        else:
                            raw_answer = str(resource_info.get('answer', 'N/A')).strip()
                            raw_evidence = str(resource_info.get('evidence', 'N/A')).strip()
                            download_text = f"Answer: {raw_answer}\nEvidence: {raw_evidence}"
                            st.download_button("Source", data=download_text, file_name=f"{paper['id']}_resource.txt", key=f"src_dl_all_{paper['id']}")
                    else:
                        download_text = f"Resource Info: {str(resource_info)}"
                        st.download_button("Source", data=download_text, file_name=f"{paper['id']}_resource.txt", key=f"src2_dl_all_{paper['id']}")
                with icon_col2:
                    if st.button("Summary", key=f"btn_summary_all_{paper['id']}"):
                        summary_content = create_summary_text(paper['data'])
                        st.session_state.dlg_open = True
                        st.session_state.dlg_title = paper['title']
                        st.session_state.dlg_html = summary_content

# Open dialog if requested
if st.session_state.dlg_open:
    open_summary_dialog(st.session_state.dlg_title, st.session_state.dlg_html)
