import streamlit as st
import base64
import html as html_lib
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from openai import OpenAI 

BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI4Research — EXHYTE Dashboard",
    layout="wide"
)

# ---------------------------------------------------------
# HELPER: GENERATE STRUCTURED SUMMARY HTML
# ---------------------------------------------------------
def generate_summary_html(data):
    """
    Parses JSON with ROBUST handling for lists of dictionaries.
    """
    html_parts = []
    
    # --- HELPER: HEADER ---
    def make_header(emoji, text):
        return f"<div style='margin-top: 18px; margin-bottom: 8px; font-weight: bold; font-size: 1.1em; border-bottom: 1px solid #ddd; padding-bottom: 4px; color: #000; font-family: \"Times New Roman\", serif;'>{emoji} {text}</div>"

    # --- HELPER: EVIDENCE ---
    def render_evidence(data_dict_or_str):
        if isinstance(data_dict_or_str, dict) and "evidence" in data_dict_or_str and data_dict_or_str["evidence"]:
            ev = data_dict_or_str["evidence"]
            if isinstance(ev, list):
                ev_text = "<br>• ".join(ev)
                if len(ev) > 0: ev_text = "• " + ev_text
            else:
                ev_text = str(ev)
            return f"<div style='margin-top: 4px; font-size: 0.9em; color: #555; background-color: #f4f4f4; padding: 6px; border-radius: 4px;'><em>📌 Evidence: {ev_text}</em></div>"
        return ""

    # --- HELPER: RENDER CONTENT ---
    def render_content(content):
        # CASE 1: List of items
        if isinstance(content, list):
            html = "<ul>"
            for item in content:
                html += "<li style='margin-bottom:8px;'>"
                if isinstance(item, dict):
                    label = item.get("label") or item.get("name") or item.get("step") or ""
                    desc = item.get("explanation") or item.get("description") or item.get("answer") or ""
                    
                    text_part = ""
                    if label:
                        text_part += f"<strong>{html_lib.escape(str(label))}</strong>"
                        if desc: text_part += f": {html_lib.escape(str(desc))}"
                    elif desc:
                        text_part += f"{html_lib.escape(str(desc))}"
                    
                    html += f"<div>{text_part}</div>"
                    html += render_evidence(item)
                else:
                    html += f"{html_lib.escape(str(item))}"
                html += "</li>"
            html += "</ul>"
            return html
        # CASE 2: Single String
        elif isinstance(content, str):
            return f"<div>{html_lib.escape(content)}</div>"
        return ""

    # SECTIONS
    if "objective" in data and data["objective"]:
        d = data["objective"]
        html = make_header("🎯", "Objective")
        html += "<div style='margin-left: 10px;'>" + render_content(d.get("answer", "")) + render_evidence(d) + "</div>"
        html_parts.append(html)

    if "knowledge_gap" in data and data["knowledge_gap"]:
        d = data["knowledge_gap"]
        html = make_header("🧩", "Knowledge Gap")
        html += "<div style='margin-left: 10px;'>" + render_content(d.get("answer", "")) + render_evidence(d) + "</div>"
        html_parts.append(html)

    if "novelty" in data and data["novelty"]:
        d = data["novelty"]
        html = make_header("✨", "Novelty")
        html += "<div style='margin-left: 10px;'>" + render_content(d.get("answer", "")) + render_evidence(d) + "</div>"
        html_parts.append(html)

    if "inspirational_papers" in data and data["inspirational_papers"]:
        d = data["inspirational_papers"]
        html = make_header("💡", "Inspirational Papers")
        html += "<div style='margin-left: 10px;'>" + render_content(d.get("answer", "")) + render_evidence(d) + "</div>"
        html_parts.append(html)

    if "method" in data and data["method"]:
        d = data["method"]
        html = make_header("⚙️", "Method")
        html += "<div style='margin-left: 10px;'>"
        if "steps" in d and isinstance(d["steps"], list):
            for step in d["steps"]:
                step_name = step.get("step", "Step")
                html += f"<div style='margin-top: 10px; background-color: #fff; border: 1px solid #e0e0e0; padding: 10px; border-radius: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);'>"
                html += f"<div style='font-weight: bold; color: #333; margin-bottom: 4px;'>{step_name}</div>"
                if "input" in step: html += f"<div style='font-size: 0.95em;'><strong>Input:</strong> {step['input']}</div>"
                if "output" in step: html += f"<div style='font-size: 0.95em;'><strong>Output:</strong> {step['output']}</div>"
                if "tools" in step:
                    tools = step["tools"]
                    if isinstance(tools, list): tools = ", ".join(tools)
                    html += f"<div style='font-size: 0.95em; color: #0056b3;'><strong>Tools:</strong> {tools}</div>"
                html += render_evidence(step)
                html += "</div>"
        if "tools" in d and isinstance(d["tools"], list):
             html += f"<div style='margin-top: 12px;'><strong>Global Tools:</strong> {', '.join(d['tools'])}</div>"
        html += render_evidence(d)
        html += "</div>"
        html_parts.append(html)

    if "performance_summary" in data and data["performance_summary"]:
        d = data["performance_summary"]
        html = make_header("📊", "Performance")
        html += "<div style='margin-left: 10px;'>"
        if "performance_summary" in d: html += render_content(d["performance_summary"])
        if "baselines" in d and d["baselines"]:
             html += "<div style='margin-top: 8px;'><strong>Baselines:</strong></div>" + render_content(d["baselines"])
        if "evaluation_metrics" in d and d["evaluation_metrics"]:
             html += "<div style='margin-top: 8px;'><strong>Metrics:</strong></div>" + render_content(d["evaluation_metrics"])
        html += render_evidence(d)
        html += "</div>"
        html_parts.append(html)

    if "subject_area" in data and data["subject_area"]:
        d = data["subject_area"]
        html = make_header("📚", "Subject Area")
        html += "<div style='margin-left: 10px;'>" + render_content(d.get("areas", [])) + render_evidence(d) + "</div>"
        html_parts.append(html)

    if "limitations" in data and data["limitations"]:
        d = data["limitations"]
        content_list = d.get("limitations", [])
        if content_list:
            html = make_header("⚠️", "Limitations")
            html += "<div style='margin-left: 10px;'>" + render_content(content_list) + render_evidence(d) + "</div>"
            html_parts.append(html)

    if "future_directions" in data and data["future_directions"]:
        d = data["future_directions"]
        content_list = d.get("future_directions", [])
        if content_list:
            html = make_header("🔮", "Future Directions")
            html += "<div style='margin-left: 10px;'>" + render_content(content_list) + render_evidence(d) + "</div>"
            html_parts.append(html)

    if "resource_link" in data and data["resource_link"]:
        d = data["resource_link"]
        url = d.get("answer", "")
        if url and url.startswith("http"):
            html = make_header("🔗", "Resource Link")
            html += f"<div style='margin-left: 10px;'><a href='{url}' target='_blank' style='color:#0000EE; text-decoration:underline;'>{url}</a></div>"
            html_parts.append(html)

    if not html_parts:
        return "<div style='color:#666; font-style:italic;'>No detailed summary data available.</div>"
    
    return "".join(html_parts)


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
def resolve_papers_directory(directory_name="Papers"):
    cwd_directory = Path.cwd() / directory_name
    base_directory = BASE_DIR / directory_name
    for directory in (cwd_directory, base_directory):
        if directory.exists() and directory.is_dir():
            return directory
    return base_directory

def load_papers_from_directory(directory_name="Papers"):
    papers = []
    directory = resolve_papers_directory(directory_name)
    
    if not directory.exists():
        return []

    json_files = sorted(directory.rglob("*.json"))
    
    for file_path in json_files:
        filename = file_path.name
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            
            raw_authors = data.get("authors", [])
            authors_str = ", ".join(raw_authors) if isinstance(raw_authors, list) else str(raw_authors)
            paper_link = data.get("link") or "#"
            paper_link = paper_link if isinstance(paper_link, str) else str(paper_link)
            
            pub_date = str(data.get("published", ""))
            year_match = re.search(r"\b(?:19|20)\d{2}\b", pub_date)
            year_str = year_match.group(0) if year_match else "N/A"
            
            topics = []
            subject_area = data.get("subject_area") or {}
            raw_areas = subject_area.get("areas", []) if isinstance(subject_area, dict) else []
            for area in raw_areas:
                if isinstance(area, dict):
                    topics.append(area.get("name", "Unknown"))
                else:
                    topics.append(str(area))
            
            papers.append({
                "title": data.get("paper_title") or "Untitled Paper",
                "authors": authors_str,
                "year": year_str,
                "venue": "arXiv" if "arxiv" in paper_link.lower() else "Scientific Publication",
                "url": paper_link,
                "topics": topics,
                "filename": filename,
                "full_data": data
            })
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue
            
    return papers

PAPER_DATA = load_papers_from_directory("Papers")

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def read_file(path):
    file_path = BASE_DIR / path
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        st.error(f"Could not find file: {path}")
        return ""

def load_image_as_base64(path):
    file_path = BASE_DIR / path
    try:
        with file_path.open("rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def process_html_content(html_content, image_map):
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all("a", href=True):
        if "wordtohtml.net" in link["href"]:
            removable = link.find_parent("div") or link
            removable.decompose()

    for p in soup.find_all('p'):
        if not p.get_text(strip=True) and p.find('br'):
            p.decompose()

    images = soup.find_all('img')
    for img in images:
        src = img.get('src', '')
        is_data_uri = src.startswith("data:")
        filename = src.split('/')[-1].split("?")[0] if '/' in src else src.split("?")[0]
        if filename in image_map:
            ext = filename.split('.')[-1].lower()
            mime = "jpeg" if ext == "jpg" else ext
            img['src'] = f"data:image/{mime};base64,{image_map[filename]}"
        elif not is_data_uri:
            placeholder = soup.new_tag("div")
            placeholder["style"] = (
                "border: 1px dashed #aaa; background: #f8f8f8; color: #555; "
                "font-family: 'Times New Roman', serif; text-align: center; "
                "padding: 32px 16px; margin: 16px auto; max-width: 640px;"
            )
            placeholder.string = f"Missing image file: {filename or 'unknown image'}"
            img.replace_with(placeholder)
            continue
        existing_style = img.get('style', '')
        img['style'] = "; ".join([
            part for part in [existing_style, 'max-width: 100%; height: auto; display: block; margin: 0 auto;'] if part
        ])
    if soup.body and "exhyte-paper" in soup.body.get("class", []):
        return str(soup)
    style_tag = soup.new_tag("style")
    style_tag.string = """
        html, body {
            background: #ffffff;
            color: #111;
        }
        body, body.pdf-article, body.exhyte-paper {
            box-sizing: border-box;
            margin: 0 auto !important;
            max-width: none !important;
            width: 100% !important;
            padding: 20px 24px 34px !important;
            background: #ffffff;
            color: #111;
            font-family: "Times New Roman", serif;
            font-size: 14pt !important;
            line-height: 1.45 !important;
        }
        p, h1, h2, h3, h4, h5, li, div {
            margin-top: 5px !important; margin-bottom: 5px !important;
            padding-top: 0px !important; padding-bottom: 0px !important;
            line-height: 1.45 !important;
        }
        h1 { font-size: 22pt !important; line-height: 1.22 !important; }
        h2 { font-size: 18pt !important; line-height: 1.25 !important; }
        h3 { font-size: 16pt !important; line-height: 1.28 !important; }
        li { margin-left: 20px !important; }
        figure { margin: 16px 0; }
        img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
        figcaption { font-size: 14pt !important; line-height: 1.35 !important; text-align: justify; }
        a { color: #0b57d0; text-decoration: underline; }
    """
    if soup.head: soup.head.append(style_tag)
    else: soup.append(style_tag)
    return str(soup)

# ---------------------------------------------------------
# Load Files
# ---------------------------------------------------------
FILES = {
    "tab1_html": "EXHYTE_webpage (1).html",
    "tab2_html": "EXHYTE_webpage (1)-1 (1).html",
    "tab3_html": "EXHYTE_webpage (2) (1).html",
}

IMAGE_FILES = [
    "image001.png",
    "image001_t2.jpg",
    "image002.jpg",
    "image003.jpg",
    "figure1.v10.png",
    "figure_2_v4_062126.png",
    "EXHYTE_stages_input_outputs_v4.png",
    "figure4_ai_methods.png",
]
image_map = {}
for img_name in IMAGE_FILES:
    b64_data = load_image_as_base64(img_name)
    if b64_data:
        image_map[img_name] = b64_data
    if b64_data and "image001.png" in img_name:
         image_map["Image_001.png"] = b64_data

html_tab1 = process_html_content(read_file(FILES["tab1_html"]), image_map)
html_tab2 = process_html_content(read_file(FILES["tab2_html"]), image_map)
html_tab3 = process_html_content(read_file(FILES["tab3_html"]), image_map)

# ---------------------------------------------------------
# CSS — Streamlit Tabs & UI Styling (GLOBAL FONTS)
# ---------------------------------------------------------
st.markdown("""
<style>
/* Global Font Setting */
html, body, [class*="css"], .stTextInput input, .stMultiSelect, .stButton button {
    font-family: 'Times New Roman', serif !important;
}

.stApp {
    max-width: none;
    width: 100%;
    margin: 0 auto;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 0.5rem;
    padding-bottom: 2rem;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    max-width: none !important;
    width: 100% !important;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] { gap: 2px; width: 100%; }
.stTabs [data-baseweb="tab"] {
    height: 60px; white-space: pre-wrap; background-color: #f0f2f6;
    border-radius: 4px 4px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px;
    flex-grow: 1; width: 100%;  
}
.stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] div {
    font-family: "Times New Roman", Times, serif !important;
    font-size: 24px !important; font-weight: 600 !important;
}
.stTabs [aria-selected="true"] { background-color: #ffffff !important; border-top: 3px solid #ff4b4b !important; }
.stTabs [data-baseweb="tab-panel"] {
    width: 100% !important;
    max-width: none !important;
    font-size: 14pt !important;
}
.stTabs [data-baseweb="tab-panel"] iframe {
    width: 100% !important;
}
.stTabs [data-baseweb="tab-panel"] p,
.stTabs [data-baseweb="tab-panel"] li,
.stTabs [data-baseweb="tab-panel"] label,
.stTabs [data-baseweb="tab-panel"] span,
.stTabs [data-baseweb="tab-panel"] input,
.stTabs [data-baseweb="tab-panel"] textarea,
.stTabs [data-baseweb="tab-panel"] button {
    font-size: 14pt !important;
    line-height: 1.42 !important;
}
.stTabs [data-baseweb="tab-panel"] h1 { font-size: 22pt !important; }
.stTabs [data-baseweb="tab-panel"] h2 { font-size: 18pt !important; }
.stTabs [data-baseweb="tab-panel"] h3 { font-size: 16pt !important; }
.stTabs [data-baseweb="tab-panel"] h4,
.stTabs [data-baseweb="tab-panel"] h5,
.stTabs [data-baseweb="tab-panel"] h6 {
    font-size: 14pt !important;
}

/* Paper List Numbering */
.paper-number {
    font-size: 14pt; font-weight: bold; color: #555; text-align: right;
    padding-right: 10px; font-family: 'Times New Roman', serif;
    white-space: nowrap !important; width: 100%;
}

/* Custom Font for Dropdown Options */
div[data-baseweb="select"] > div {
    font-family: 'Times New Roman', serif !important;
}
div[data-baseweb="popover"] {
    font-family: 'Times New Roman', serif !important;
    font-size: 14pt !important;
}
div[data-baseweb="popover"] * {
    font-size: 14pt !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<h1 style="text-align:center; font-size:48px; margin-bottom:5px; font-family: 'Times New Roman', serif;">
A Process-Centric Survey of AI for Scientific Discovery Through the EXHYTE Framework
</h1>
<p style="text-align:center; font-size:20px; margin-top:5px; margin-bottom:10px; font-family: 'Times New Roman', serif;">
Md Musaddaqul Hasib<sup>1,2</sup>, Sumin Jo<sup>3</sup>, Harsh Sinha<sup>1,4</sup>,
Jifeng Song<sup>1,3</sup>, Arun Das<sup>1,2</sup>, Zhentao Liu<sup>1</sup>,
Hugh Galloway<sup>1</sup>, Huey Huang<sup>5</sup>, Jianqiu (Michelle) Zhang<sup>10</sup>,
Kexun Zhang<sup>6</sup>, Shou-Jiang Gao<sup>1,7</sup>, Yu-Chiao Chiu<sup>2,8,9</sup>,
Lei Li<sup>6</sup>, Yufei Huang<sup>1,2,3*</sup>
</p>
<p style="text-align:center; font-size:16px; max-width:900px; margin:auto; line-height:1.4; font-family: 'Times New Roman', serif;">
1 Cancer Virology Program, UPMC Hillman Cancer Center, Pittsburgh, PA, USA;
2 Department of Medicine, University of Pittsburgh, Pittsburgh, PA, USA;
3 Department of Electrical and Computer Engineering, Swanson School of Engineering, University of Pittsburgh, Pittsburgh, PA, USA;
4 Intelligent Systems Program, School of Computing and Information, University of Pittsburgh, Pittsburgh, PA, USA;
5 Electrical and Computer Engineering, University of Texas at Austin, Austin, TX, USA;
6 Language Technologies Institute, Carnegie Mellon University, Pittsburgh, PA, USA;
7 Department of Microbiology and Molecular Genetics, University of Pittsburgh School of Medicine, Pittsburgh, PA, USA;
8 Department of Computational and Systems Biology, University of Pittsburgh School of Medicine, Pittsburgh, PA, USA;
9 Cancer Therapeutics Program, UPMC Hillman Cancer Center, Pittsburgh, PA, USA;
10 Klesse College of Engineering and Integrated Design, University of Texas at San Antonio, San Antonio, TX, USA.
</p>
<p style="text-align:center; font-size:15px; max-width:900px; margin:10px auto 0; line-height:1.35; font-family: 'Times New Roman', serif;">
*Corresponding author(s). E-mail(s): yuh119@pitt.edu;<br>
Contributing authors: mdh121@pitt.edu; sumin.jo@pitt.edu; has197@pitt.edu;
jis219@pitt.edu; ard212@pitt.edu; zhl169@pitt.edu; hug18@pitt.edu;
hueyhuang@utexas.edu; michelle.zhang@utsa.edu; kexunz@andrew.cmu.edu;
gaos8@upmc.edu; yuc250@pitt.edu; leili@andrew.cmu.edu;
</p>

<div style="max-width:900px; margin:auto; margin-top:25px; margin-bottom:20px; font-family: 'Times New Roman', serif;">
    <h3 style="text-align:center; font-size:24px; font-weight:bold; margin-bottom:10px; font-family: 'Times New Roman', serif;">Abstract</h3>
    <p style="font-size:18px; line-height:1.5; text-align:justify; margin-bottom:15px;">
    Large language models (LLMs) and agent systems increasingly support scientific discovery across domains.
    Yet the literature remains fragmented around isolated tasks, with limited attention to how components
    form integrated workflows. Here, we introduce <strong>EX</strong>ploration, <strong>HY</strong>pothesis generation, and <strong>TE</strong>sting (EXHYTE)
    as an empirical workflow abstraction for reviewing AI-assisted scientific discovery. We mapped a corpus
    of recent studies to EXHYTE stages and substages to identify recurring strategies, workflow connections,
    and capability gaps. The analysis shows strong progress in exploration, especially retrieval, knowledge
    assembly, and representation learning, and growing capacity for hypothesis and idea generation. The central
    bottleneck remains the transition from hypothesis or idea generation to executable experimental or
    computational testing, followed by feedback that can refine subsequent workflow steps. Because EXHYTE
    organizes systems by workflow function rather than agent architecture, it applies to both multi-agent
    scaffolds and emerging generalist tool-using agents. It also shows that integrated workflows do not imply
    full automation: current systems still depend on human judgment for problem formulation, contextualization,
    interpretation, risk assessment, and oversight. We discuss evaluation, reproducibility, hypothesis-space
    narrowing, external validation, and governance considerations. An accompanying website at
    https://webapps.crc.pitt.edu/exhyte/ provides paper summaries and an EXHYTE-based interactive survey.
    </p>
    <p style="font-size:18px; text-align:justify;">
    <strong>Keywords:</strong> AI for Scientific discovery, the EXHYTE framework, Large language models, Hypothesis generation, Idea generation
    </p>
</div>

<hr style="margin-top:20px; margin-bottom:20px;">
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TABS & CONTENT
# ---------------------------------------------------------
tab_sec2, tab_sec34, tab_sec5, tab_papers, tab_survey = st.tabs([
    "The EXHYTE Framework",
    "AI Methods for EXHYTE",
    "Tools & Datasets",
    "Paper List",
    "Survey Generator"
])

with tab_sec2: st.iframe(html_tab1, height=1350)
with tab_sec34: st.iframe(html_tab2, height=1350)
with tab_sec5: st.iframe(html_tab3, height=1350)

# --- TAB 4: PAPER LIST ---
with tab_papers:
    col_filter, col_list = st.columns([1, 4])

    with col_filter:
        st.markdown("### Filters")
        all_topics = set()
        for p in PAPER_DATA:
            if "topics" in p: all_topics.update(p["topics"])
        
        selected_topics = st.multiselect("Search by Topic", options=sorted(list(all_topics)))
        search_keyword = st.text_input("Search by Keyword", placeholder="e.g. Creativity...")

    # Filter Logic
    filtered_papers = []
    clean_keyword = search_keyword.strip().lower() if search_keyword else ""
    
    if not selected_topics and not clean_keyword:
        filtered_papers = PAPER_DATA 
    else:
        for p in PAPER_DATA:
            topic_match = not selected_topics or any(t in p.get("topics", []) for t in selected_topics)
            keyword_match = True
            if clean_keyword:
                full_text_search = str(p['full_data']).lower()
                if clean_keyword not in full_text_search:
                    keyword_match = False
            if topic_match and keyword_match:
                filtered_papers.append(p)

    with col_list:
        st.markdown(f"### References & Papers ({len(filtered_papers)})")
        st.markdown("---")
        
        if not filtered_papers:
            if not PAPER_DATA: st.warning("No JSON files found in 'Papers' folder.")
            else: st.info("No papers found matching criteria.")

        with st.container(height=1000, border=False):
            for idx, paper in enumerate(filtered_papers):
                with st.container():
                    paper_id = re.sub(r"[^A-Za-z0-9_-]+", "_", paper.get("filename", str(idx)))
                    summary_key = f"show_summary_{paper_id}"
                    c_num, c_content, c_btns = st.columns([1, 14, 3])
                    
                    with c_num:
                        st.markdown(f"<div class='paper-number'>{idx + 1}</div>", unsafe_allow_html=True)
                    
                    with c_content:
                        title_html = html_lib.escape(paper['title'], quote=True)
                        authors_html = html_lib.escape(paper['authors'], quote=True)
                        venue_html = html_lib.escape(paper['venue'], quote=True)
                        year_html = html_lib.escape(str(paper['year']), quote=True)
                        content_html = f"""
                        <div style="font-family: 'Times New Roman', serif;">
                            <div style="font-size: 14pt; font-weight: bold; color: #000;">{title_html}</div>
                            <div style="font-size: 14pt; color: #333; font-style: italic;">{authors_html} ({year_html})</div>
                            <div style="font-size: 14pt; color: #666;">{venue_html}</div>
                        </div>
                        """
                        st.markdown(content_html, unsafe_allow_html=True)

                    with c_btns:
                        b1, b2 = st.columns([1, 1])
                        with b1:
                            if st.button("📄", key=f"sum_btn_{paper_id}", help="View Summary"):
                                st.session_state[summary_key] = not st.session_state.get(summary_key, False)
                        with b2:
                            url = paper.get("url", "")
                            if isinstance(url, str) and url.startswith(("http://", "https://")):
                                st.link_button("🔗", url, help="Go to Source")
                            else:
                                st.button("🔗", key=f"link_btn_{paper_id}", help="No source link available", disabled=True)

                    if st.session_state.get(summary_key, False):
                        rich_summary_html = generate_summary_html(paper['full_data'])
                        
                        st.markdown(f"""
                        <div style="
                            background-color: #fcfcfc; 
                            border: 1px solid #ddd;
                            border-left: 5px solid #888; 
                            padding: 15px; 
                            margin-top: 10px; 
                            margin-bottom: 15px; 
                            font-family: 'Times New Roman', serif; 
                            color: #000;
                            line-height: 1.5;">
                            {rich_summary_html}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<hr style='margin-top: 5px; margin-bottom: 5px; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

# --- TAB 5: SURVEY GENERATOR ---
with tab_survey:
    # SURVEY PROMPT TEMPLATE
    survey_prompt_template = """
    I want you to write a scientific survey that summarizes the provided JSON papers.
    
    The survey should have the following sections:
    1. **Introduction**: Overview of the research themes.
    2. **Methodological Approaches**: Synthesize the methods (e.g. tools, frameworks).
    3. **Key Innovations**: Highlight novelty across papers.
    4. **Limitations & Gaps**: Discuss common limitations or knowledge gaps.
    5. **Future Directions**: Suggest future research paths based on the papers.
    
    Output the survey in well-formatted Markdown.
    Use academic tone.
    """

    st.markdown("### Scientific Survey Generator")
    st.markdown("Generate a structured, scientific-style survey from selected papers.")
    st.markdown("---")

    if "survey_selected_titles" not in st.session_state:
        st.session_state.survey_selected_titles = []
    if "survey_output" not in st.session_state:
        st.session_state.survey_output = ""

    col_left, col_right = st.columns([1, 2])

    with col_left:
        # 1. API KEY INPUT
        st.markdown("**1. API Key**")
        openai_api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            placeholder="sk-..."
        )

        # 2. FILTER BY YEAR
        st.markdown("**2. Filter Papers by Year**")
        # Extract all unique years
        all_years = sorted(
            {p['year'] for p in PAPER_DATA if re.fullmatch(r"(?:19|20)\d{2}", str(p['year']))},
            key=int,
            reverse=True
        )
        selected_years = st.multiselect(
            "Select Publication Years:",
            options=all_years,
            help="Filter the list of papers below by their publication year."
        )

        # 3. PAPER SELECTION (Filtered by year)
        st.markdown("**3. Select Papers**")

        # Filter titles based on selected years
        if selected_years:
            filtered_paper_data = [p for p in PAPER_DATA if p['year'] in selected_years]
        else:
            filtered_paper_data = PAPER_DATA

        # Map Title -> Full Data
        paper_map = {p['title']: p['full_data'] for p in filtered_paper_data}
        all_titles = sorted(list(paper_map.keys()))

        valid_selected_titles = [title for title in st.session_state.survey_selected_titles if title in paper_map]
        if valid_selected_titles != st.session_state.survey_selected_titles:
            st.session_state.survey_selected_titles = valid_selected_titles

        selected_titles = st.multiselect(
            "Choose papers to include in the survey:",
            options=all_titles,
            default=st.session_state.survey_selected_titles,
            help="Select multiple papers to synthesize into a survey."
        )
        st.session_state.survey_selected_titles = selected_titles

        if not all_titles:
            st.info("No papers are available for the currently selected years.")
        else:
            st.caption(f"{len(all_titles)} papers available for the current filter.")

        # 4. GENERATE BUTTON
        st.markdown("<br>", unsafe_allow_html=True)
        generate_clicked = st.button("🚀 Generate Survey Summary")

    with col_right:
        st.markdown("**Survey Output**")

        if generate_clicked:
            if not openai_api_key:
                st.error("Please enter your OpenAI API key first.")
            elif not selected_titles:
                st.warning("Please select at least one paper.")
            else:
                try:
                    client = OpenAI(api_key=openai_api_key)
                    json_objects = [paper_map[title] for title in selected_titles]
                    user_content = f"Here are {len(json_objects)} JSON files representing selected papers:\n" + "\n\n".join(
                        json.dumps(obj, indent=2) for obj in json_objects
                    )

                    messages = [
                        {"role": "system", "content": "You are a helpful assistant for writing scientific surveys."},
                        {"role": "user", "content": survey_prompt_template + "\n\n" + user_content},
                    ]

                    with st.spinner("Generating survey summary... this may take a minute ⏳"):
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=messages,
                            temperature=0.1,
                            max_tokens=4000,
                        )

                    survey_text = response.choices[0].message.content.strip()
                    st.session_state.survey_output = survey_text

                    st.success("Survey Generated Successfully!")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        if st.session_state.survey_output:
            st.markdown(st.session_state.survey_output)
        elif not generate_clicked:
            st.info("Choose papers and click generate to create a survey.")
