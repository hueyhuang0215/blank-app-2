import os
import json
import re
import streamlit as st
from openai import OpenAI
from dateutil import parser
from typing import Dict, Any, List

# --------------------------
# Page Configuration
# --------------------------
st.set_page_config(
    page_title="AI Scientific Discovery Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Add an HTML anchor for the "Back to Top" link ---
st.markdown("<a id='top'></a>", unsafe_allow_html=True)

st.title("AI Methods for Scientific Discovery: A Comprehensive Survey")
st.caption("Based on 'AI Methods for Scientific Discovery: A Comprehensive Survey Organized by the EXHYTE Framework'")

# --------------------------
# Define Tabs
# --------------------------
tab_sec2, tab_sec3_4, tab_sec5, tab_paper_list, tab_survey_gen = st.tabs([
    "Section 2: EXHYTE Cycle", 
    "Sections 3 & 4: AI Methods & Closed-Loop", 
    "Section 5: Tools & Datasets", 
    "Paper List Explorer", 
    "Survey Generator"
])


# ----------------------------------------------------------------------
# TAB 1: Section 2: The EXHYTE Cycle
# (This tab is unchanged)
# ----------------------------------------------------------------------
with tab_sec2:
    st.header("Section 2: The EXHYTE Cycle: A workflow for data-intensive scientific discovery")
    with st.container(height=700):
        st.markdown(r"""
        *Content extracted word-for-word from Article\_Title\_\_1\_.pdf*
        
        We derived the EXHYTE cycle from two complementary sources: recent advances in the philosophy of scientific discovery [9-11], which emphasizes iterative and exploratory models of inquiry, and a systematic review of workflows used in state-of-the-art Al-driven research systems. Across these works, we observed a shared structure in which exploration of large knowledge bases leads naturally to hypothesis generation and targeted testing, forming a self-sustaining loop that integrates human reasoning with computational and experimental processes. EXHYTE formalizes this pattern as an explicit, generalizable framework for data-intensive discovery.

        Research typically enters the EXHYTE cycle through a trigger (Fig. 1), for example, an open question, an unexpected observation, an anomaly in data, or the introduction of a new measurement technology. Such triggers define a broad area of inquiry but rarely yield immediately testable predictions. The first stage, EXPLORE, therefore seeks to organize what is known and expose what remains uncertain.
        
        **(Fig. 1 The EXHYTE Cycle and substages)**

        EXPLORE aims to assemble and structure knowledge so that knowledge gaps become explicit and actionable. This stage consists of three substages:
        * • E1: Query structuring translates research questions into machine-actionable forms (e.g., keyphrases, controlled vocabularies, domain schemas) to guide retrieval.
        * • E2: Data retrieval collects literature, code, and structured datasets from scientific repositories and APIs according to the structured query plan in E1.
        * • E3: Knowledge assembly normalizes and integrates retrieved data into representations such as embeddings, graphs, or feature tables and summarizes evidence to surface explicit knowledge gaps.

        The output of EXPLORE is a structured knowledge base and a set of defined knowledge gaps that motivate the next stage.

        HYPOTHESIZE transforms knowledge gaps into ideas or specific, testable claims through two substages:
        * • H1: Hypothesis/idea generation formulates candidate mechanisms or interventions using approaches such as literature-grounded reasoning or data-driven strategies.
        * • H2: Hypothesis/idea prioritization evaluates these candidates for novelty, plausibility, feasibility and expected impact using quantitative metrics or expert and LLM-based assessments.
        
        The outcome of this stage is a prioritized list of hypotheses with clear rationales and success criteria, ready for empirical validation.

        TEST translates hypotheses into executable experiments and closes the feedback loop.
        * • T1: Experimental design specifies objectives, protocols, datasets/materials, and measurable outcomes, yielding executable experimental or computational plans.
        * • T2: Testing and refinement performs in silico, in vitro or in vivo experiments and analyzes the results to confirm, refine, or reject hypotheses.

        Results from TEST feed back into the cycle through one of the three paths. When the findings generally support the hypothesis but leave important uncertainties, the process proceeds through refinement by adjusting parameters, recording additional variables, or refining the experimental design while maintaining the same mechanistic focus. When evidence contradicts the hypothesis, the cycle pivots, preserving the original knowledge gap but exploring alternative explanations or mechanisms in the next iteration. In contrast, when success criteria are fully met and the research question is resolved, the inquiry sunsets, concluding the current line of investigation rather than looping back to further exploration. Together, these outcomes ensure that EXHYTE functions as a self-correcting, evidence-driven process, capable of continuous adaptation while allowing closure when discovery goals are achieved.
        """)


# ----------------------------------------------------------------------
# TAB 2: Sections 3 & 4: AI Methods & Closed-Loop
# (This tab is unchanged)
# ----------------------------------------------------------------------
with tab_sec3_4:
    st.header("Sections 3 & 4: AI Methods and Closed-Loop Discovery")
    with st.container(height=700):
        # --- Section 3 ---
        st.subheader("Section 3: AI Methods for the EXHYTE Cycle")
        st.markdown(r"""
        *Content extracted word-for-word from Article\_Title\_\_1\_.pdf*

        To construct the survey corpus, we focused on the literature published between 2018 and July 2025 to capture recent advances in LLMs and agent systems for scientific discovery...

        #### 3.1 Trigger: User Input
        
        In automated scientific discovery systems, user input ranges from natural language queries about research topics to domain-specific research papers or datasets, playing a central role in aligning system behavior with specific goals. High-level research directions, such as workshop themes, set the scope for the automated scientific workflow. For example, the ICLR 2025 workshop "I Can't Believe It's Not Better" (ICBINB) focused on real-world pitfalls, challenges, and negative or inconclusive results in deep learning, a perspective incorporated in AI-Scientist-v2 [12]. Similarly, focused problem statements, such as "How can we improve the energy efficiency of AI models?" (e.g., SCI-IDEA [13]), guide idea and hypothesis generation. Extending this idea, IRIS [14] formalizes user input as research goals that explicitly decompose into a problem and its motivation/context...

        #### 3.2 The Explore Stage

        **3.2.1 E1: Query Structuring**
        
        User query structuring is the first step in the Explore Stage, where it transforms raw, unstructured research inputs into actionable representations. This process employs complementary strategies including decomposition, vector representation, and information extraction from datasets to enable targeted exploration across literature and data.
        
        * **E1-S1: Decomposition.** Decomposition transforms complex research queries into tractable sub-queries/questions or tasks that enable focused literature/dataset retrieval, reasoning, and solution design using LLM. Different systems operationalize decomposition at various levels. Chain of Ideas [24] decomposes initial research topic into multiple sub-queries that capture diverse perspectives on the same problem., SCI-IDEA [13] extracts keyphrases...
        * **E1-S2: Vector Representations.** Vector representations transform unstructured text queries, documents, or data entities into high-dimensional embeddings...
        * **E1-S3: Information Extraction from Datasets.** Extracting key features and annotations from structured datasets enables automated systems to generate empirical inputs for downstream tasks such as model training, hypothesis formulation, and idea generation. AstroAgents [36], for instance, employs a Data Analyst Agent to identify polycyclic aromatic hydrocarbon (PAH) patterns...

        **3.2.2 E2: Data Retrieval**

        The data retrieval substage leverages structured queries from E1 to gather relevant information from diverse sources, including literature, databases, and code repositories.
        
        * **E2-S1: Literature Retrieval.** Literature retrieval methods gather scientific papers... AI-Scientist-v2 [12], retrieve literature via the Semantic Scholar API...
        * **E2-S2: Related-Work Based Retrieval.** Citation networks and semantic similarity are widely used to link related works and surface new directions. ResearchAgent [18], SCIMON [35], HypER [20], and Chain of Ideas [24] expand from an anchor paper by retrieving both citing and cited works...
        * **E2-S3: Dataset Retrieval from Scientific Repositories.** Datasets provide the empirical foundation for analysis, model training, and validation. In drug discovery, DrugMCTS [21] queries databases to retrieve molecules structurally similar to a query compound...

        **3.2.3 E3: Knowledge Assembly**
        
        The knowledge-assembly stage transforms unstructured scientific text into structured, queryable representations that enable efficient reasoning during discovery. The existing literature typically employs three strategies: structured extraction and summarization from literature, knowledge-graph construction, and database construction...
        
        * **E3-S1: Structured extraction and summarization from literature.** To make literature readily usable for idea and hypothesis generation, systems extract and summarize standardized sections (e.g., titles, abstracts, methods, results). SciPIP [34], Chain of Ideas [24], SCI-IDEA [13], and Al-Researcher [28] use LLMs to generate summaries...
        * **E3-S2: Knowledge Graph Construction.** Knowledge graphs (KGs) are frequently used to consolidate extracted entities and relationships into a structured, queryable format...
        * **E3-S3: Database construction.** Some systems construct specialized databases to support large-scale retrieval and synthesis...

        #### 3.3 The Hypothesize Stage

        **3.3.1 H1: Hypothesis/Idea Generation**

        This substage bridges structured knowledge from EXPLORE to new, testable claims, employing literature-based, data-driven, or multi-agent strategies.
        
        * **H1-S1: Literature-based Generation.** This strategy synthesizes information from existing literature to identify gaps, contradictions, or novel connections...
        * **H1-S2: Data-driven Generation.** Data-driven methods identify patterns, correlations, or anomalies in empirical data to generate hypotheses...
        * **H1-S3: Multi-agent Generation.** Multi-agent systems orchestrate specialized agents to manage complex, multi-step hypothesis-generation...

        **3.3.2 H2: Hypothesis/Idea Prioritization**

        This substage evaluates generated hypotheses to identify the most promising candidates for testing, often balancing novelty, plausibility, and feasibility.
        
        * **H2-S1: Literature-based Assessment.** This strategy assesses novelty and plausibility by cross-referencing hypotheses against the existing literature...
        * **H2-S2: Quantitative Assessment Using Domain Metrics.** In domains with established benchmarks, quantitative metrics are used to rank hypotheses...
        * **H2-S3: Human Evaluation.** Expert-feedback remains a crucial component for validating the real-world relevance and feasibility of generated hypotheses...

        #### 3.4 The Test Stage

        **3.4.1 T1: Experimental Design Generation**

        This substage translates prioritized hypotheses into concrete, executable experimental plans, specifying protocols, materials, and measurement criteria.
        
        * **T1-S1: Literature-informed Experimental Design.** AI systems can retrieve and adapt established protocols from the literature...
        * **T1-S2: LLM-based Experiment Design Generation.** LLMs are increasingly used to generate full experimental plans from scratch...

        **3.4.2 T2: Testing and Refinement**

        This substage involves executing the designed experiments, analyzing results, and refining hypotheses.
        
        * **T2-S1: Data-driven Testing.** This strategy relies on computational analysis or simulation to validate hypotheses...
        * **T2-S2: LLM-based Evaluation.** LLMs are used to interpret experimental outputs, assess outcomes against success criteria, and propose refinements...
        * **T2-S3: Human Feedback and Guided Refinement.** Human-in-the-loop refinement is essential for navigating ambiguous results...
        * **T2-S4: Researcher-Guided Refinement.** In this mode, researchers actively steer the discovery process...
        * **T2-S5: Agent Feedback Refinement.** Multi-agent systems use internal feedback loops...
        """)

        # --- Section 4 ---
        st.subheader("Section 4: Closed-Loop Scientific Discovery")
        st.markdown(r"""
        *Content extracted from Article\_Title\_\_1\_.pdf*

        While the EXHYTE cycle provides a modular framework for understanding AI contributions, the ultimate goal is to integrate these stages into "closed-loop" systems capable of autonomous discovery. Closed-loop systems connect exploration, hypothesis, and testing in a continuous feedback cycle, allowing the system to iteratively refine its understanding and actions based on new evidence.

        #### 4.1 System-driven Closed-loop Discovery
        In a system-driven loop, the AI orchestrates the entire process, often with a human "on-the-loop" for oversight.
        * **T2 -> E1 (Refinement Loop):** This is the most common loop, where experimental results (T2) trigger a new round of exploration (E1).
        * **T2 -> H1 (Pivot Loop):** When experiments (T2) invalidate a hypothesis, the system pivots.
        
        #### 4.2 Human-in-the-loop Closed-loop Discovery
        Human-in-the-loop systems rely on researchers to bridge stages, particularly for complex reasoning or validation.
        * **T2 -> Human -> E1 (Human-guided Exploration):** Researchers analyze test results (T2) and manually define the next exploration query (E1).
        * **T2 -> Human -> H1 (Human-guided Hypothesis):** Test results (T2) are interpreted by researchers who then formulate the next hypothesis (H1).

        #### 4.3 Human-out-of-the-loop Closed-loop Discovery
        In this emerging paradigm, the AI system operates with full autonomy, executing the entire EXHYTE cycle without human intervention. ... These systems, such as AI-Scientist-v2 [12], demonstrate the potential for AI to independently navigate the scientific process, from identifying knowledge gaps in the literature (E1-E3) to generating novel hypotheses (H1), prioritizing them (H2), designing experiments (T1), and interpreting code execution results (T2) to confirm or reject its own ideas, thus concluding the discovery loop.
        """)


# ----------------------------------------------------------------------
# TAB 3: Section 5: Tools and Datasets
# (This tab is unchanged)
# ----------------------------------------------------------------------
with tab_sec5:
    st.header("Section 5: Tools and Datasets for Building EXHYTE Workflows")
    with st.container(height=700):
        st.markdown(r"""
        *Content extracted word-for-word from Article\_Title\_\_1\_.pdf*
        
        The preceding sections surveyed strategies for each EXHYTE stage. Here we complement that view with the practical tools, APIs, and datasets that enable those strategies to operate. We group resources by their role in the cycle and note where they most naturally plug into EXHYTE.

        #### 5.1 Core tools and APIs
        * **Literature & data access (E2).** OpenAlex and PubChem provide open, programmatic access to scholarly works and chemical records for large-scale querying, linking, and metadata integration [76, 77].
        * **Text parsing & normalization (E3).** Scientific NLP pipelines commonly rely on scispaCy for sentence segmentation, lemmatization, and entity recognition [78].
        * **Vector representations & retrieval (E2/E3).** Embedding stores and ANN indexes such as FAISS [79] and ChromaDB enable efficient similarity search over large document or embedding collections.
        * **Molecular & crystal processing (E3/T1).** RDKit is standard for cheminformatics, offering tools for molecular representation, substructure analysis, and feature calculation [80]. Pymatgen is the materials science equivalent, used for structure analysis and database generation [81].
        * **Workflow & agent orchestration (Full cycle).** LangChain, LlamaIndex, and AutoGen provide frameworks for building and coordinating multi-step workflows and agentic systems [82-84].

        #### 5.2 Benchmark Datasets
        Datasets are essential for training models (H1) and validating outcomes (T2).
        
        **Biology & medicine.**
        * **MoleculeNet (H1/T2):** A collection of datasets for molecular property prediction [56].
        * **Therapeutics Data Commons (TDC) (H1/T2):** A broader collection of datasets and tasks spanning drug discovery and development [85].
        * **Protein Data Bank (PDB) (E2/H1):** The primary repository for 3D protein structures.
        * **PubChem & ChEMBL (E2/H1):** Large-scale databases of chemical compounds, bioactivities, and genomic data.
        * **ClinTox (T2):** A dataset for predicting clinical trial toxicity for drugs [56].
        * **MIMIC-IV & UK Biobank (E2/T2):** Large-scale clinical and genomic databases used for data-driven hypothesis generation and testing.
        
        **Materials science & chemistry.**
        * **Materials Project (E2/H1):** A core database of computed material properties [81].
        * **Open Catalyst 2020 (OC20) (H1/T2):** A large-scale dataset for catalyst modeling [87].
        * **JARVIS-DFT & Matbench (E2/H1/T2):** Collections of computed properties and benchmarks for materials-property prediction [86, 88].
        
        **Computer science.**
        * **S2ORC (E2/E3):** A large corpus of scientific papers for literature analysis [90].
        * **SciDocs (E3):** A multi-domain benchmark for scientific document processing [89].
        * **SciFact (T2):** A dataset for verifying scientific claims.
        """)


# ----------------------------------------------------------------------
# TAB 4: Paper List Explorer (NEW 2-ROW LAYOUT + CORRECTED)
# ----------------------------------------------------------------------
with tab_paper_list:

    # --- Initialize Session State to hold the selected paper ---
    if 'paper_to_view' not in st.session_state:
        st.session_state.paper_to_view = None # This will store the data of the paper to show

    # --- Main App Logic ---
    
    # Automatically find the path
    script_dir = os.path.dirname(__file__)
    papers_folder = "Papers"
    json_dir_papers = os.path.join(script_dir, papers_folder)

    # Check if this automatic path exists
    if not os.path.isdir(json_dir_papers):
        st.error(f"Error: The folder '{papers_folder}' was not found.")
        st.warning(f"Please create a folder named '{papers_folder}' in your project's main directory and upload your paper JSON files to it.")
    else:
        # If the path exists, run the rest of the app
        try:
            # --- 1. Load all paper data ---
            @st.cache_data
            def load_all_papers(directory):
                all_papers_data = []
                all_subjects = set()
                
                json_files = sorted([f for f in os.listdir(directory) if f.endswith(".json")])
                if not json_files:
                    return [], []

                for filename in json_files:
                    file_path = os.path.join(directory, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Extract title (handles both 'paper_title' and 'title')
                        title = data.get("paper_title") or data.get("title", filename)
                        
                        # Extract subject areas
                        subjects = []
                        subject_data = data.get("subject_area", {}).get("areas", ["Unknown"])
                        if not subject_data:
                            subjects = ["Unknown"]
                        else:
                            for area in subject_data:
                                subject = str(area.get("name") if isinstance(area, dict) else area)
                                subjects.append(subject)
                                all_subjects.add(subject)

                        # Create a searchable string
                        search_text = json.dumps(data).lower()
                        
                        all_papers_data.append({
                            "filename": filename,
                            "title": title,
                            "data": data,
                            "subjects": subjects,
                            "search_text": search_text
                        })
                    except Exception as e:
                        st.error(f"Error loading {filename}: {e}")
                
                return all_papers_data, sorted(list(all_subjects))

            all_papers, unique_subjects = load_all_papers(json_dir_papers)

            if not all_papers:
                st.warning(f"No JSON files found or loaded from '{json_dir_papers}'.")
            else:
                # --- TOP ROW: Filters and Paper List ---
                col1, col2 = st.columns([3, 7]) 

                # ------------- Column 1: Search & Filter (Unchanged) -------------
                with col1:
                    st.header("Search & Filter")
                    
                    # Feature 1: Search by Keyword
                    st.markdown("#### Search by Keyword")
                    search_query = st.text_input("Enter keywords to search all papers:", key="keyword_search")
                    
                    st.markdown("---")

                    # Feature 2: Search by Topic
                    st.header("Browse by Topic")
                    # Feature 3: "All Papers" is the default
                    topic_list = ["All Papers"] + unique_subjects
                    
                    selected_topic = st.radio(
                        "Filter by topic:", 
                        topic_list, 
                        key="topic_filter"
                    )

                # ------------- Column 2: Paper List (NEW LOGIC) -------------
                with col2:
                    st.header("Paper List")
                    
                    # 1. Filter by Topic
                    if selected_topic == "All Papers":
                        papers_to_show = all_papers
                    else:
                        papers_to_show = [
                            p for p in all_papers if selected_topic in p["subjects"]
                        ]
                    
                    # 2. Filter by Keyword Search
                    if search_query:
                        query = search_query.lower()
                        papers_to_show = [
                            p for p in papers_to_show if query in p["search_text"]
                        ]
                    
                    papers_to_show.sort(key=lambda p: p["title"])
                    
                    st.markdown(f"**Showing {len(papers_to_show)} paper(s)**")
                    st.info("Click a paper's [View Summary] button, then scroll down to see the summary.")
                    st.markdown("---") # Add a separator

                    if not papers_to_show:
                        st.info("No papers match your filters.")
                    else:
                        # Loop to create list with buttons
                        for paper in papers_to_show:
                            
                            # Layout: [Title] [Source] [Summary Button]
                            col_title, col_source, col_summary = st.columns([6, 3, 3])

                            with col_title:
                                st.markdown(f"**{paper['title']}**")

                            with col_source:
                                with st.expander("View Source"):
                                    paper_data = paper['data']
                                    link = paper_data.get('link')
                                    published = paper_data.get('published', 'No publication info available.')
                                    authors = paper_data.get('authors', 'No authors listed.')

                                    st.markdown(f"**Authors:** {authors}")
                                    st.markdown(f"**Publication:** {published}")
                                    if link:
                                        st.markdown(f"**Link:** [{link}]({link})")
                                    else:
                                        st.markdown("**Link:** No link available.")
                            
                            with col_summary:
                                # This button sets the session state, which updates the viewer below
                                if st.button("View Summary", key=f"sum_{paper['filename']}", use_container_width=True):
                                    st.session_state.paper_to_view = paper['data']
                            
                            st.markdown("---") # Add a small separator between papers

                # --- BOTTOM ROW: Summary Viewer ---
                st.markdown("---")
                
                # We use st.empty() to create a container we can "center"
                viewer_container = st.empty()
                
                with viewer_container.container():
                    st.header("📑 Summary Viewer")

                    # Check if a paper has been selected
                    if st.session_state.paper_to_view:
                        paper_data = st.session_state.paper_to_view
                        
                        st.subheader(f"Displaying: {paper_data.get('paper_title') or paper_data.get('title', 'N/A')}")
                        
                        # --- <<< FIX: This logic loops through ALL keys >>> ---
                        
                        # --- Basic Info First ---
                        authors = paper_data.get("authors", "")
                        if authors:
                            st.markdown(f"**Authors:** {authors}")
                        
                        published = paper_data.get("published", "")
                        if published:
                            st.markdown(f"**Published:** {published}")

                        link = paper_data.get("link", "")
                        if link:
                            st.markdown(f"🔗 [Paper Link]({link})")
                            
                        st.markdown("---")

                        # --- Loop through all other keys ---
                        for section, content in paper_data.items():
            
                            # --- Skip keys we already handled or don't want to show ---
                            if section in ["paper_title", "title", "authors", "published", "link", "subject_area"]:
                                continue
                            
                            if not content:
                                continue # Skip empty fields

                            # --- Format section title ---
                            section_title = section.replace("_", " ").title()
                            st.subheader(f"📌 {section_title}")

                            # --- Handle different content types ---
                            
                            # Handle dictionary content (like 'summary' or 'resource_link')
                            if isinstance(content, dict):
                                if "answer" in content:
                                    st.markdown(content.get("answer", "*No answer provided.*"))
                                    evidence = content.get("evidence")
                                    if evidence:
                                        st.markdown(f"**Evidence:** {evidence}")
                                else:
                                    # Generic dictionary print
                                    for key, value in content.items():
                                        if value:
                                            st.markdown(f"- **{key.replace('_', ' ').title()}**: {value}")

                            # Handle list content (like 'method' or 'limitations')
                            elif isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict):
                                        # Nice print for lists of objects (e.g., methods)
                                        name = item.get("name", "")
                                        desc = item.get("description", "") or item.get("step", "")
                                        if name or desc:
                                            st.markdown(f"- **{name}**: {desc}")
                                        else:
                                            st.json(item) # fallback for unknown dicts
                                    else:
                                        st.markdown(f"- {item}")
                            
                            # Handle simple string content
                            elif isinstance(content, str):
                                st.markdown(content)
                            
                            # Fallback for other data types
                            else:
                                st.json(content)

                        st.markdown("---")
                        
                        # --- "Done" button to clear selection and "Back to Top" link ---
                        col_done, col_top = st.columns([2, 10])
                        with col_done:
                            # <<<--- FIX: Removed st.experimental_rerun() ---
                            if st.button("Done (Clear Summary)"):
                                st.session_state.paper_to_view = None
                                # The app will rerun automatically when the state is cleared
                                # To force a visual clear, we re-draw the "empty" state
                                viewer_container.info("Click a 'View Summary' button from the list above to load a paper here.")
                        
                        with col_top:
                            # This link scrolls the user back to the anchor at the top
                            st.markdown("<a href='#top'>⬆️ Back to Top</a>", unsafe_allow_html=True)

                    else:
                        st.info("Click a 'View Summary' button from the list above to load a paper here.")


        except Exception as e:
            st.error(f"An error occurred: {e}")


# ----------------------------------------------------------------------
# TAB 5: Survey Generator
# (This tab is unchanged)
# ----------------------------------------------------------------------
with tab_survey_gen:
    st.header("🤖 Scientific Survey Generator")
    st.write("Generate a structured, scientific-style survey from selected JSON paper files.")

    # --- Configuration Inputs ---
    
    # Automatically find the path
    script_dir = os.path.dirname(__file__)
    survey_folder = "exhyte_data"
    json_dir_survey = os.path.join(script_dir, survey_folder)

    st.subheader("🔑 OpenAI API Key")
    openai_api_key = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        placeholder="sk-...",
        key="survey_gen_api_key"
    )

    if not os.path.isdir(json_dir_survey):
        st.error(f"Error: The folder '{survey_folder}' was not found.")
        st.warning(f"Please create a folder named '{survey_folder}' in your project's main directory and upload your survey JSON files to it.")
    elif not openai_api_key:
        st.warning("Please enter your OpenAI API key to generate surveys.")
    else:
        # If paths are valid, run the rest of the app
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=openai_api_key)

            # --- Load JSON files and extract titles + year ---
            @st.cache_data
            def load_survey_files(directory):
                available_files = [f for f in os.listdir(directory) if f.endswith(".json")]
                if not available_files:
                    return None, None

                paper_titles_map = {}  # title -> filename
                paper_years_map = {}   # title -> year

                for file_name in available_files:
                    file_path = os.path.join(directory, file_name)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        
                        # Extract title
                        title = data.get("paper_title") or data.get("title", file_name)
                        if title in paper_titles_map: # Handle duplicate titles
                            title = f"{title} ({file_name})"
                        
                        # Extract year
                        year_str = data.get("year") or data.get("published", "")
                        year = "N/A"
                        if year_str:
                            try:
                                year = parser.parse(str(year_str)).year
                            except parser.ParserError:
                                match = re.search(r'\b(19|20)\d{2}\b', str(year_str))
                                if match:
                                    year = match.group(0)
                        
                        paper_titles_map[title] = file_name
                        paper_years_map[title] = year

                    except Exception as e:
                        st.error(f"Error loading {file_name}: {e}")
                
                return paper_titles_map, paper_years_map

            paper_titles, paper_years = load_survey_files(json_dir_survey)

            if not paper_titles:
                st.warning(f"No JSON files found in '{json_dir_survey}' folder.")
            else:
                # --- Sidebar: Paper Selection ---
                with st.expander("📂 Select Papers for Survey", expanded=True):
                    # Sort papers by year (newest first), then title
                    sorted_titles = sorted(
                        paper_titles.keys(),
                        key=lambda t: (
                            paper_years.get(t) if isinstance(paper_years.get(t), (int, float)) else 0,
                            t
                        ),
                        reverse=True
                    )
                    
                    selected_titles = []
                    for title in sorted_titles:
                        year = paper_years[title]
                        if st.checkbox(f"{title} ({year})", key=f"cb_survey_{title}"):
                            selected_titles.append(title)
                
                st.info(f"{len(selected_titles)} paper(s) selected.")

                # --- Survey Prompt Template (from survey_exhyte.py) ---
                survey_prompt_template = """
                You are a scientific writer tasked with summarizing multiple LLM-guided workflow papers based on structured JSON files.

                Each JSON file contains information about a discovery workflow with the following standardized sections:
                1. Inputs to the Workflow
                2. E1: Query Structuring
                3. E2: Data Retrieval
                4. E3: Knowledge Assembly
                5. H1: Hypothesis/Idea Generation
                6. H2: Hypothesis or Idea Prioritization
                7. T1: Experimental Design Generation
                8. T2: Iterative Refinement
                9. Publication Details (title, authors, publication date, and link)

                ---

                ### OBJECTIVE
                Generate a *scientific survey-style summary* that compares and synthesizes the workflows from all provided JSON files.

                ---

                ### OUTPUT REQUIREMENTS
                Your output **must follow the exact same section order and headings** as the input schema, formatted as follows:

                **Inputs to the Workflow** [Write one or more formal paragraphs integrating all JSONs that describe what users provided — goals, datasets, research context, or formal specifications. Cite papers using author and year.]

                **E1: Query Structuring** [Summarize how queries or tasks were structured, reformulated, or decomposed. Cite all relevant papers.]

                **E2: Data Retrieval** [Describe how relevant data, literature, or other sources were gathered or filtered. Cite all relevant papers.]

                **E3: Knowledge Assembly** [Explain how structured knowledge was constructed, encoded, or represented. Cite all relevant papers.]

                **H1: Hypothesis/Idea Generation** [Describe how the systems generated hypotheses or ideas, including tools or reasoning strategies. Cite all relevant papers.]

                **H2: Hypothesis or Idea Prioritization** [Describe how hypotheses were ranked, filtered, or evaluated. Cite all relevant papers.]

                **T1: Experimental Design Generation** [SummarSizze how experiments were planned or designed to test generated hypotheses. Cite all relevant papers.]

                **T2: Iterative Refinement** [Describe any feedback loops or iterative improvement mechanisms used in the workflow. Cite all relevant papers.]

                **Conclusion** [Provide an integrative summary comparing how the workflows collectively advance automated scientific discovery.]

                **References** [List all papers, formatted as: Authors (Year). Title. Publication Date. Link.]

                ---

                ### ADDITIONAL RULES
                1. Every section heading (Inputs to theWorkflow, E1, E2, etc.) **must appear in the output** — even if only one paper contributes.
                2. Each paragraph **must begin with a bolded heading**, as shown above.
                3. Use **formal academic writing** — complete sentences, no bullet points.
                4. Only use information contained in the JSON files.
                5. Ensure in-text citations follow the form *(Author et al., Year)*.
                6. Always include a final **References** section with full paper metadata.

                ---

                ### INPUT
                Below are the JSON workflow descriptions:

                ### OUTPUT
                A structured, stage-preserving, multi-paragraph scientific survey comparing the workflows, formatted according to the stage order above.
                """

                # --- Survey Generation Button ---
                if st.button("🚀 Generate Survey Summary"):
                    if not selected_titles:
                        st.warning("Please select at least one paper.")
                    else:
                        try:
                            json_objects = []
                            for title in selected_titles:
                                file_name = paper_titles[title]
                                file_path = os.path.join(json_dir_survey, file_name)
                                with open(file_path, "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                json_objects.append(data)

                            user_content = f"Here are {len(json_objects)} JSON files representing selected papers:\n" + "\n\n".join(
                                json.dumps(obj, indent=2) for obj in json_objects
                            )

                            messages = [
                                {"role": "system", "content": "You are a helpful assistant for writing scientific surveys."},
                                {"role": "user", "content": survey_prompt_template + "\n\n" + user_content},
                            ]

                            with st.spinner("Generating survey summary... this may take a minute ⏳"):
                                response = client.chat.completions.create(
                                    model="gpt-4-turbo", # Using a recommended model
                                    messages=messages,
                                    temperature=0.1,
                                    max_tokens=4096, 
                                )

                            survey_text = response.choices[0].message.content.strip()

                            st.subheader("📘 Generated Survey Summary")
                            st.markdown(survey_text)

                        except Exception as e:
                            st.error(f"An error during API call: {e}")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")