"""
Cheminformatics Virtual Laboratory
Student: R. JAYADHARAN | Register No.: RA2611026050288
Institution: SRM Institute of Science and Technology, Tiruchirappalli

Run:
    pip install -r requirements.txt
    streamlit run app.py

Notes:
- The periodic table contains all 118 officially named elements.
- Molecular 3D generation uses RDKit when installed.
- PubChem lookup is optional and uses its public PUG REST service.
- The existing professor attribution is retained as supplied by the student.
"""

import io
import json
import math
import urllib.parse
import urllib.request

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Optional chemistry/3D dependencies
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, Draw, rdMolDescriptors
    RDKIT_AVAILABLE = True
except Exception:
    RDKIT_AVAILABLE = False

try:
    import py3Dmol
    from stmol import showmol
    THREE_D_AVAILABLE = True
except Exception:
    THREE_D_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False


st.set_page_config(
    page_title="Cheminformatics Virtual Laboratory",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --ink: #eaf3ff;
  --muted: #9fb2cc;
  --cyan: #54f0d0;
  --blue: #69a9ff;
}
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
  color: var(--ink);
  background:
    radial-gradient(ellipse at 12% 8%, rgba(32, 205, 190, .18), transparent 34%),
    radial-gradient(ellipse at 88% 18%, rgba(91, 116, 255, .20), transparent 34%),
    radial-gradient(ellipse at 55% 100%, rgba(0, 183, 255, .12), transparent 42%),
    linear-gradient(135deg, #07111f 0%, #0a1426 48%, #10152c 100%);
  background-attachment: fixed;
}
[data-testid="stHeader"] { background: rgba(5, 12, 25, .30); }
[data-testid="stAppViewContainer"] { background: transparent; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1450px; }
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(9,22,40,.98), rgba(14,20,43,.97));
  border-right: 1px solid rgba(110, 230, 224, .18);
}
section[data-testid="stSidebar"] * { color: #e6f2ff; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
  padding: .48rem .65rem; border-radius: 10px; transition: all .22s ease;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(84,240,208,.12); transform: translateX(3px);
}
.hero {
  position: relative; overflow: hidden; isolation: isolate;
  padding: 2rem 2.1rem; border-radius: 24px;
  background: linear-gradient(115deg, rgba(14,49,70,.96), rgba(24,55,105,.92) 55%, rgba(65,44,112,.90));
  border: 1px solid rgba(117, 237, 224, .30);
  box-shadow: 0 18px 55px rgba(0,0,0,.28), inset 0 1px rgba(255,255,255,.12);
  color: white; margin-bottom: 1.5rem;
  animation: riseIn .8s ease both;
}
.hero:before, .hero:after {
  content:""; position:absolute; z-index:-1; border-radius:50%;
  filter: blur(2px); opacity:.38; pointer-events:none;
}
.hero:before { width:250px; height:250px; right:8%; top:-145px; background:#54f0d0; animation: floatOrb 9s ease-in-out infinite; }
.hero:after { width:190px; height:190px; right:28%; bottom:-145px; background:#788bff; animation: floatOrb 11s ease-in-out infinite reverse; }
.hero h1 { color:white; font-family:'Space Grotesk',sans-serif; font-size:clamp(1.8rem,3.5vw,3rem); line-height:1.12; margin:0 0 .55rem 0; }
.hero p { color:#d9f8ff; margin:.25rem 0; }
.hero .tag { display:inline-block; margin-top:1rem; padding:.42rem .8rem; border-radius:999px; background:rgba(84,240,208,.13); border:1px solid rgba(84,240,208,.35); color:#bffcf0; font-size:.82rem; }
h1, h2, h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.02em; }
h2, h3 { color:#d9f4ff !important; }
div[data-testid="stMetric"] {
  background: linear-gradient(145deg, rgba(18,39,66,.86), rgba(21,31,58,.82));
  border:1px solid rgba(115,196,230,.22); border-radius:18px;
  padding:1rem 1.1rem; box-shadow:0 10px 30px rgba(0,0,0,.16);
  transition:transform .25s ease, border-color .25s ease;
}
div[data-testid="stMetric"]:hover { transform:translateY(-4px); border-color:rgba(84,240,208,.55); }
div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button {
  border:1px solid rgba(84,240,208,.55); border-radius:12px;
  color:#041923; font-weight:700;
  background:linear-gradient(110deg,#54f0d0,#72c8ff);
  box-shadow:0 7px 22px rgba(38,210,202,.18);
  transition:transform .2s ease, box-shadow .2s ease, filter .2s ease;
}
div[data-testid="stButton"] > button:hover, div[data-testid="stDownloadButton"] > button:hover {
  transform:translateY(-2px); filter:brightness(1.06);
  box-shadow:0 10px 28px rgba(38,210,202,.28);
}
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
div[data-testid="stTextArea"] textarea {
  background:rgba(5,15,29,.72); color:#eaf3ff;
  border:1px solid rgba(125,175,220,.28); border-radius:11px;
}
div[data-testid="stExpander"] {
  background:rgba(13,29,51,.62); border:1px solid rgba(110,180,220,.20);
  border-radius:14px; overflow:hidden;
}
div[data-testid="stAlert"] { border-radius:13px; }
.stTabs [data-baseweb="tab-list"] { gap:.45rem; }
.stTabs [data-baseweb="tab"] { background:rgba(22,42,70,.7); border-radius:10px 10px 0 0; padding:.65rem 1rem; }
.element-tile {
  border:1px solid rgba(155,205,230,.30); border-radius:10px; padding:5px 2px;
  text-align:center; min-height:70px; background:rgba(15,35,58,.76);
  color:#eaf3ff; transition:transform .18s ease, box-shadow .18s ease;
}
.element-tile:hover { transform:translateY(-3px) scale(1.03); box-shadow:0 7px 20px rgba(84,240,208,.15); }
.element-symbol {font-size:1.25rem; font-weight:800;}
.element-number {font-size:.68rem; opacity:.8;}
.element-name {font-size:.64rem; overflow-wrap:anywhere;}
.small-muted {color:var(--muted); font-size:.9rem;}
@keyframes riseIn { from {opacity:0; transform:translateY(18px)} to {opacity:1; transform:translateY(0)} }
@keyframes floatOrb { 0%,100% {transform:translate3d(0,0,0)} 50% {transform:translate3d(-22px,18px,0)} }
@media (prefers-reduced-motion: reduce) {
  *, *:before, *:after { animation-duration:.01ms !important; transition-duration:.01ms !important; }
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------------
# Student and faculty information
# -------------------------------------------------------------------
STUDENT_NAME = "R. JAYADHARAN"
REGISTER_NUMBER = "RA2611026050288"
INSTITUTION = "SRM Institute of Science and Technology, Tiruchirappalli"
FACULTY_NAME = "Dr. C. Manivannan"
FACULTY_DESIGNATION = "Assistant Professor"
FACULTY_DEPARTMENT = "Division of Chemistry, School of Sciences"
FACULTY_CONTACT = "cmanivannan89@gmail.com"


# -------------------------------------------------------------------
# Complete periodic table: 118 elements
# Layout group and period values follow the conventional long-form table.
# Lanthanoids and actinoids are displayed in their own two rows.
# -------------------------------------------------------------------
ELEMENT_ROWS = [
    # Z, symbol, name, atomic mass (standard/representative), category, period, group
    (1,"H","Hydrogen","1.008","Nonmetal",1,1),
    (2,"He","Helium","4.0026","Noble gas",1,18),
    (3,"Li","Lithium","6.94","Alkali metal",2,1),
    (4,"Be","Beryllium","9.0122","Alkaline earth metal",2,2),
    (5,"B","Boron","10.81","Metalloid",2,13),
    (6,"C","Carbon","12.011","Nonmetal",2,14),
    (7,"N","Nitrogen","14.007","Nonmetal",2,15),
    (8,"O","Oxygen","15.999","Nonmetal",2,16),
    (9,"F","Fluorine","18.998","Halogen",2,17),
    (10,"Ne","Neon","20.180","Noble gas",2,18),
    (11,"Na","Sodium","22.990","Alkali metal",3,1),
    (12,"Mg","Magnesium","24.305","Alkaline earth metal",3,2),
    (13,"Al","Aluminium","26.982","Post-transition metal",3,13),
    (14,"Si","Silicon","28.085","Metalloid",3,14),
    (15,"P","Phosphorus","30.974","Nonmetal",3,15),
    (16,"S","Sulfur","32.06","Nonmetal",3,16),
    (17,"Cl","Chlorine","35.45","Halogen",3,17),
    (18,"Ar","Argon","39.948","Noble gas",3,18),
    (19,"K","Potassium","39.098","Alkali metal",4,1),
    (20,"Ca","Calcium","40.078","Alkaline earth metal",4,2),
    (21,"Sc","Scandium","44.956","Transition metal",4,3),
    (22,"Ti","Titanium","47.867","Transition metal",4,4),
    (23,"V","Vanadium","50.942","Transition metal",4,5),
    (24,"Cr","Chromium","51.996","Transition metal",4,6),
    (25,"Mn","Manganese","54.938","Transition metal",4,7),
    (26,"Fe","Iron","55.845","Transition metal",4,8),
    (27,"Co","Cobalt","58.933","Transition metal",4,9),
    (28,"Ni","Nickel","58.693","Transition metal",4,10),
    (29,"Cu","Copper","63.546","Transition metal",4,11),
    (30,"Zn","Zinc","65.38","Transition metal",4,12),
    (31,"Ga","Gallium","69.723","Post-transition metal",4,13),
    (32,"Ge","Germanium","72.630","Metalloid",4,14),
    (33,"As","Arsenic","74.922","Metalloid",4,15),
    (34,"Se","Selenium","78.971","Nonmetal",4,16),
    (35,"Br","Bromine","79.904","Halogen",4,17),
    (36,"Kr","Krypton","83.798","Noble gas",4,18),
    (37,"Rb","Rubidium","85.468","Alkali metal",5,1),
    (38,"Sr","Strontium","87.62","Alkaline earth metal",5,2),
    (39,"Y","Yttrium","88.906","Transition metal",5,3),
    (40,"Zr","Zirconium","91.224","Transition metal",5,4),
    (41,"Nb","Niobium","92.906","Transition metal",5,5),
    (42,"Mo","Molybdenum","95.95","Transition metal",5,6),
    (43,"Tc","Technetium","[98]","Transition metal",5,7),
    (44,"Ru","Ruthenium","101.07","Transition metal",5,8),
    (45,"Rh","Rhodium","102.91","Transition metal",5,9),
    (46,"Pd","Palladium","106.42","Transition metal",5,10),
    (47,"Ag","Silver","107.87","Transition metal",5,11),
    (48,"Cd","Cadmium","112.41","Transition metal",5,12),
    (49,"In","Indium","114.82","Post-transition metal",5,13),
    (50,"Sn","Tin","118.71","Post-transition metal",5,14),
    (51,"Sb","Antimony","121.76","Metalloid",5,15),
    (52,"Te","Tellurium","127.60","Metalloid",5,16),
    (53,"I","Iodine","126.90","Halogen",5,17),
    (54,"Xe","Xenon","131.29","Noble gas",5,18),
    (55,"Cs","Caesium","132.91","Alkali metal",6,1),
    (56,"Ba","Barium","137.33","Alkaline earth metal",6,2),
    (57,"La","Lanthanum","138.91","Lanthanide",6,3),
    (58,"Ce","Cerium","140.12","Lanthanide",6,4),
    (59,"Pr","Praseodymium","140.91","Lanthanide",6,5),
    (60,"Nd","Neodymium","144.24","Lanthanide",6,6),
    (61,"Pm","Promethium","[145]","Lanthanide",6,7),
    (62,"Sm","Samarium","150.36","Lanthanide",6,8),
    (63,"Eu","Europium","151.96","Lanthanide",6,9),
    (64,"Gd","Gadolinium","157.25","Lanthanide",6,10),
    (65,"Tb","Terbium","158.93","Lanthanide",6,11),
    (66,"Dy","Dysprosium","162.50","Lanthanide",6,12),
    (67,"Ho","Holmium","164.93","Lanthanide",6,13),
    (68,"Er","Erbium","167.26","Lanthanide",6,14),
    (69,"Tm","Thulium","168.93","Lanthanide",6,15),
    (70,"Yb","Ytterbium","173.05","Lanthanide",6,16),
    (71,"Lu","Lutetium","174.97","Lanthanide",6,17),
    (72,"Hf","Hafnium","178.49","Transition metal",6,4),
    (73,"Ta","Tantalum","180.95","Transition metal",6,5),
    (74,"W","Tungsten","183.84","Transition metal",6,6),
    (75,"Re","Rhenium","186.21","Transition metal",6,7),
    (76,"Os","Osmium","190.23","Transition metal",6,8),
    (77,"Ir","Iridium","192.22","Transition metal",6,9),
    (78,"Pt","Platinum","195.08","Transition metal",6,10),
    (79,"Au","Gold","196.97","Transition metal",6,11),
    (80,"Hg","Mercury","200.59","Transition metal",6,12),
    (81,"Tl","Thallium","204.38","Post-transition metal",6,13),
    (82,"Pb","Lead","207.2","Post-transition metal",6,14),
    (83,"Bi","Bismuth","208.98","Post-transition metal",6,15),
    (84,"Po","Polonium","[209]","Post-transition metal",6,16),
    (85,"At","Astatine","[210]","Halogen",6,17),
    (86,"Rn","Radon","[222]","Noble gas",6,18),
    (87,"Fr","Francium","[223]","Alkali metal",7,1),
    (88,"Ra","Radium","[226]","Alkaline earth metal",7,2),
    (89,"Ac","Actinium","[227]","Actinide",7,3),
    (90,"Th","Thorium","232.04","Actinide",7,4),
    (91,"Pa","Protactinium","231.04","Actinide",7,5),
    (92,"U","Uranium","238.03","Actinide",7,6),
    (93,"Np","Neptunium","[237]","Actinide",7,7),
    (94,"Pu","Plutonium","[244]","Actinide",7,8),
    (95,"Am","Americium","[243]","Actinide",7,9),
    (96,"Cm","Curium","[247]","Actinide",7,10),
    (97,"Bk","Berkelium","[247]","Actinide",7,11),
    (98,"Cf","Californium","[251]","Actinide",7,12),
    (99,"Es","Einsteinium","[252]","Actinide",7,13),
    (100,"Fm","Fermium","[257]","Actinide",7,14),
    (101,"Md","Mendelevium","[258]","Actinide",7,15),
    (102,"No","Nobelium","[259]","Actinide",7,16),
    (103,"Lr","Lawrencium","[266]","Actinide",7,17),
    (104,"Rf","Rutherfordium","[267]","Transition metal",7,4),
    (105,"Db","Dubnium","[268]","Transition metal",7,5),
    (106,"Sg","Seaborgium","[269]","Transition metal",7,6),
    (107,"Bh","Bohrium","[270]","Transition metal",7,7),
    (108,"Hs","Hassium","[277]","Transition metal",7,8),
    (109,"Mt","Meitnerium","[278]","Transition metal",7,9),
    (110,"Ds","Darmstadtium","[281]","Transition metal",7,10),
    (111,"Rg","Roentgenium","[282]","Transition metal",7,11),
    (112,"Cn","Copernicium","[285]","Transition metal",7,12),
    (113,"Nh","Nihonium","[286]","Post-transition metal",7,13),
    (114,"Fl","Flerovium","[289]","Post-transition metal",7,14),
    (115,"Mc","Moscovium","[290]","Post-transition metal",7,15),
    (116,"Lv","Livermorium","[293]","Post-transition metal",7,16),
    (117,"Ts","Tennessine","[294]","Halogen",7,17),
    (118,"Og","Oganesson","[294]","Noble gas",7,18),
]

ELEMENTS = pd.DataFrame(
    ELEMENT_ROWS,
    columns=["Atomic number", "Symbol", "Element", "Atomic mass", "Category", "Period", "Group"],
)

CATEGORY_COLORS = {
    "Alkali metal": "#f7c6c7",
    "Alkaline earth metal": "#f4d6a0",
    "Transition metal": "#c8d8f0",
    "Post-transition metal": "#c8e6d0",
    "Metalloid": "#d9d0f0",
    "Nonmetal": "#bce8e5",
    "Halogen": "#f4c8e5",
    "Noble gas": "#d8e8ff",
    "Lanthanide": "#f7dfb5",
    "Actinide": "#e9c9d9",
}


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------
def pubchem_get(path):
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/" + path
    req = urllib.request.Request(url, headers={"User-Agent": "ChemistryVirtualLab/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


@st.cache_data(show_spinner=False)
def pubchem_compound(name):
    safe_name = urllib.parse.quote(name.strip())
    data = pubchem_get(f"compound/name/{safe_name}/property/MolecularFormula,MolecularWeight,IUPACName,CanonicalSMILES,IsomericSMILES/JSON")
    props = data["PropertyTable"]["Properties"][0]
    cid = props.get("CID")
    return props, cid


def parse_smiles(smiles):
    if not RDKIT_AVAILABLE:
        return None, "RDKit is not installed. Install the packages in requirements.txt."
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, "Invalid SMILES string. Please check the structure."
    return mol, None


def molecule_descriptors(mol):
    return {
        "Molecular formula": rdMolDescriptors.CalcMolFormula(mol),
        "Molecular weight (g/mol)": round(Descriptors.MolWt(mol), 3),
        "Exact molecular weight": round(Descriptors.ExactMolWt(mol), 4),
        "LogP": round(Descriptors.MolLogP(mol), 3),
        "TPSA (Å²)": round(Descriptors.TPSA(mol), 3),
        "H-bond donors": Descriptors.NumHDonors(mol),
        "H-bond acceptors": Descriptors.NumHAcceptors(mol),
        "Rotatable bonds": Descriptors.NumRotatableBonds(mol),
        "Rings": rdMolDescriptors.CalcNumRings(mol),
        "Heavy atoms": mol.GetNumHeavyAtoms(),
        "Total atoms (including H)": Chem.AddHs(mol).GetNumAtoms(),
        "Fraction Csp3": round(rdMolDescriptors.CalcFractionCSP3(mol), 3),
    }


def make_2d_png(mol):
    m = Chem.Mol(mol)
    Chem.rdDepictor.Compute2DCoords(m)
    return Draw.MolToImage(m, size=(650, 450))


def make_3d_block(mol):
    m = Chem.AddHs(Chem.Mol(mol))
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    status = AllChem.EmbedMolecule(m, params)
    if status != 0:
        raise ValueError("RDKit could not generate 3D coordinates for this molecule.")
    try:
        AllChem.MMFFOptimizeMolecule(m, maxIters=250)
    except Exception:
        AllChem.UFFOptimizeMolecule(m, maxIters=250)
    return m


def show_3d_molecule(mol, style_name="stick"):
    m3d = make_3d_block(mol)
    block = Chem.MolToMolBlock(m3d)
    viewer = py3Dmol.view(width=850, height=520)
    viewer.addModel(block, "mol")
    styles = {
        "Ball and stick": {"stick": {"radius": 0.16}, "sphere": {"scale": 0.28}},
        "Stick": {"stick": {"radius": 0.22}},
        "Space filling": {"sphere": {"scale": 0.85}},
        "Wireframe": {"line": {"linewidth": 2}},
    }
    viewer.setStyle(styles.get(style_name, styles["Ball and stick"]))
    viewer.setBackgroundColor("#101820")
    viewer.zoomTo()
    showmol(viewer, height=540, width=900)


def create_pdf_report(compound_name, descriptors):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 55
    c.setFont("Helvetica-Bold", 18)
    c.drawString(48, y, "CHEMINFORMATICS VIRTUAL LABORATORY")
    y -= 35
    c.setFont("Helvetica-Bold", 13)
    c.drawString(48, y, "Molecular Properties Report")
    y -= 30
    c.setFont("Helvetica", 10)
    lines = [
        f"Student: {STUDENT_NAME}",
        f"Register Number: {REGISTER_NUMBER}",
        f"Institution: {INSTITUTION}",
        f"Compound: {compound_name}",
        "",
        "Molecular descriptors:",
    ]
    for line in lines:
        c.drawString(48, y, line)
        y -= 17
    for key, value in descriptors.items():
        c.drawString(60, y, f"{key}: {value}")
        y -= 17
    y -= 12
    c.setFont("Helvetica-Bold", 11)
    c.drawString(48, y, "Faculty")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(48, y, f"{FACULTY_NAME} - {FACULTY_DESIGNATION}")
    y -= 16
    c.drawString(48, y, FACULTY_DEPARTMENT)
    y -= 16
    c.drawString(48, y, INSTITUTION)
    c.save()
    buffer.seek(0)
    return buffer


def show_student_footer():
    st.divider()
    left, right = st.columns(2)
    with left:
        st.markdown("### 🎓 Student Details")
        st.write(f"**Name:** {STUDENT_NAME}")
        st.write(f"**Register Number:** {REGISTER_NUMBER}")
        st.write(f"**Institution:** {INSTITUTION}")
    with right:
        st.markdown("### 👨‍🏫 Developed by")
        st.write(f"**{FACULTY_NAME}**")
        st.write(FACULTY_DESIGNATION)
        st.write(FACULTY_DEPARTMENT)
        st.write("Faculty of Engineering and Technology")
        st.write(INSTITUTION)
        st.info(f"📧 For queries, contact: {FACULTY_CONTACT}")


# -------------------------------------------------------------------
# Sidebar navigation
# -------------------------------------------------------------------
st.sidebar.title("🧪 Chemistry Virtual Lab")
st.sidebar.caption(f"{STUDENT_NAME} | {REGISTER_NUMBER}")
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "3D Molecular Visualization",
        "Molecular Properties",
        "Periodic Table (118 Elements)",
        "PubChem Compound Search",
        "Structure–Property Analysis",
        "Theory & Learning",
        "Assessment",
        "Student Project Report",
    ],
)

st.markdown(
    f"""<div class="hero">
    <h1>🧪 Cheminformatics Virtual Laboratory</h1>
    <p>Explore molecules. Discover properties. Experience chemistry in 3D.</p>
    <p>Interactive learning space featuring molecular visualization, descriptors and all 118 elements.</p>
    <span class="tag">✦ STUDENT PROJECT · {STUDENT_NAME} · {REGISTER_NUMBER}</span>
    </div>""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------
# Home
# -------------------------------------------------------------------
if page == "Home":
    st.subheader("Welcome to the Cheminformatics Virtual Laboratory")
    st.write(
        "This educational application introduces molecular structures, "
        "molecular descriptors, 3D visualization, and the periodic table."
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Elements", "118")
    c2.metric("Molecular views", "2D + 3D")
    c3.metric("Student project", "Chemistry")
    st.markdown("### Main features")
    st.markdown("""
    - Interactive 3D molecular visualization using RDKit and 3Dmol.js.
    - Molecular descriptors such as formula, molecular weight, LogP and TPSA.
    - Complete periodic table with element details.
    - PubChem compound search, when an internet connection is available.
    - Downloadable molecular property report in PDF format.
    """)
    st.markdown("### Example molecules")
    examples = {
        "Water": "O",
        "Ethanol": "CCO",
        "Benzene": "c1ccccc1",
        "Phenol": "Oc1ccccc1",
        "Acetic acid": "CC(=O)O",
        "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
        "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    }
    st.dataframe(pd.DataFrame(examples.items(), columns=["Compound", "SMILES"]), hide_index=True, use_container_width=True)


# -------------------------------------------------------------------
# Molecular visualization
# -------------------------------------------------------------------
elif page == "3D Molecular Visualization":
    st.subheader("Interactive 3D Compound Visualization")
    examples = {
        "Ethanol": "CCO",
        "Benzene": "c1ccccc1",
        "Phenol": "Oc1ccccc1",
        "Acetic Acid": "CC(=O)O",
        "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
        "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
        "Water": "O",
        "Custom SMILES": "",
    }
    selected = st.selectbox("Choose a compound", list(examples.keys()))
    default_smiles = examples[selected]
    smiles = st.text_input("Enter SMILES", value=default_smiles, help="Example: CCO for ethanol")
    style = st.selectbox("3D display style", ["Ball and stick", "Stick", "Space filling", "Wireframe"])
    if st.button("Visualize molecule", type="primary"):
        mol, error = parse_smiles(smiles)
        if error:
            st.error(error)
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 2D structure")
                st.image(make_2d_png(mol), use_container_width=True)
            with col2:
                st.markdown("#### 3D structure")
                if THREE_D_AVAILABLE:
                    try:
                        show_3d_molecule(mol, style)
                    except Exception as exc:
                        st.error(f"3D visualization error: {exc}")
                else:
                    st.warning("3D viewer packages are missing. Install py3Dmol and stmol.")
            st.success(f"Valid molecular structure. SMILES: {smiles}")
            st.session_state["last_smiles"] = smiles
    st.caption("Tip: use your mouse to rotate, zoom and inspect the 3D molecular model.")


# -------------------------------------------------------------------
# Molecular properties
# -------------------------------------------------------------------
elif page == "Molecular Properties":
    st.subheader("Molecular Properties Calculator")
    smiles = st.text_input("Enter compound SMILES", value=st.session_state.get("last_smiles", "CCO"))
    compound_label = st.text_input("Compound name", value="User compound")
    if st.button("Calculate properties", type="primary"):
        mol, error = parse_smiles(smiles)
        if error:
            st.error(error)
        else:
            descriptors = molecule_descriptors(mol)
            st.session_state["last_descriptors"] = descriptors
            st.session_state["last_compound"] = compound_label
            st.session_state["last_smiles"] = smiles
            st.markdown("#### 2D molecular structure")
            st.image(make_2d_png(mol), use_container_width=False)
            st.markdown("#### Calculated descriptors")
            a, b = st.columns(2)
            items = list(descriptors.items())
            midpoint = math.ceil(len(items) / 2)
            with a:
                for key, value in items[:midpoint]:
                    st.metric(key, value)
            with b:
                for key, value in items[midpoint:]:
                    st.metric(key, value)
            if REPORTLAB_AVAILABLE:
                pdf = create_pdf_report(compound_label, descriptors)
                st.download_button(
                    "📄 Download PDF report",
                    data=pdf,
                    file_name="molecular_properties_report.pdf",
                    mime="application/pdf",
                )
            else:
                st.warning("Install reportlab to enable PDF reports.")


# -------------------------------------------------------------------
# Periodic table
# -------------------------------------------------------------------
elif page == "Periodic Table (118 Elements)":
    st.subheader("Complete Interactive Periodic Table")
    st.write("Select any element to view its atomic number, symbol, atomic mass, category, period and group.")
    categories = ["All categories"] + sorted(ELEMENTS["Category"].unique().tolist())
    selected_category = st.selectbox("Filter by category", categories)
    filtered = ELEMENTS if selected_category == "All categories" else ELEMENTS[ELEMENTS["Category"] == selected_category]

    # Standard grid positions, with f-block displayed separately.
    main_elements = ELEMENTS[~ELEMENTS["Category"].isin(["Lanthanide", "Actinide"])]
    for period in range(1, 8):
        cols = st.columns(18, gap="small")
        row_elements = main_elements[main_elements["Period"] == period]
        for _, el in row_elements.iterrows():
            group = int(el["Group"])
            if selected_category != "All categories" and el["Category"] != selected_category:
                continue
            color = CATEGORY_COLORS.get(el["Category"], "#eeeeee")
            with cols[group - 1]:
                st.markdown(
                    f"""<div class="element-tile" style="background:{color}">
                    <div class="element-number">{el['Atomic number']}</div>
                    <div class="element-symbol">{el['Symbol']}</div>
                    <div class="element-name">{el['Element']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                if st.button("Select", key=f"element_{int(el['Atomic number'])}", use_container_width=True):
                    st.session_state["selected_element"] = int(el["Atomic number"])

    st.markdown("#### Lanthanides")
    lan_cols = st.columns(15, gap="small")
    lanths = ELEMENTS[ELEMENTS["Category"] == "Lanthanide"]
    for i, (_, el) in enumerate(lanths.iterrows()):
        with lan_cols[i]:
            st.markdown(
                f"<div class='element-tile' style='background:{CATEGORY_COLORS['Lanthanide']}'><div class='element-number'>{el['Atomic number']}</div><div class='element-symbol'>{el['Symbol']}</div><div class='element-name'>{el['Element']}</div></div>",
                unsafe_allow_html=True,
            )
            if st.button("Select", key=f"element_{int(el['Atomic number'])}", use_container_width=True):
                st.session_state["selected_element"] = int(el["Atomic number"])

    st.markdown("#### Actinides")
    act_cols = st.columns(15, gap="small")
    acts = ELEMENTS[ELEMENTS["Category"] == "Actinide"]
    for i, (_, el) in enumerate(acts.iterrows()):
        with act_cols[i]:
            st.markdown(
                f"<div class='element-tile' style='background:{CATEGORY_COLORS['Actinide']}'><div class='element-number'>{el['Atomic number']}</div><div class='element-symbol'>{el['Symbol']}</div><div class='element-name'>{el['Element']}</div></div>",
                unsafe_allow_html=True,
            )
            if st.button("Select", key=f"element_{int(el['Atomic number'])}", use_container_width=True):
                st.session_state["selected_element"] = int(el["Atomic number"])

    selected_z = st.session_state.get("selected_element", 6)
    selected_row = ELEMENTS[ELEMENTS["Atomic number"] == selected_z].iloc[0]
    st.markdown("### Selected element")
    x, y, z = st.columns(3)
    x.metric("Element", f"{selected_row['Element']} ({selected_row['Symbol']})")
    y.metric("Atomic number", int(selected_row["Atomic number"]))
    z.metric("Atomic mass", selected_row["Atomic mass"])
    st.write(f"**Category:** {selected_row['Category']}")
    st.write(f"**Period:** {int(selected_row['Period'])}  |  **Group:** {int(selected_row['Group'])}")
    st.markdown("#### All 118 elements")
    st.dataframe(filtered.sort_values("Atomic number"), hide_index=True, use_container_width=True)


# -------------------------------------------------------------------
# PubChem search
# -------------------------------------------------------------------
elif page == "PubChem Compound Search":
    st.subheader("Search Chemical Compounds in PubChem")
    query = st.text_input("Enter compound name", placeholder="e.g. aspirin, caffeine, glucose")
    if st.button("Search PubChem", type="primary") and query.strip():
        try:
            with st.spinner("Searching PubChem..."):
                props, cid = pubchem_compound(query)
            st.success(f"Found compound: PubChem CID {cid}")
            st.json(props)
            canonical = props.get("ConnectivitySMILES") or props.get("CanonicalSMILES")
            if canonical:
                st.code(canonical, language="text")
                st.session_state["last_smiles"] = canonical
                if RDKIT_AVAILABLE:
                    mol, error = parse_smiles(canonical)
                    if not error:
                        st.image(make_2d_png(mol), caption="2D structure", use_container_width=False)
                        if THREE_D_AVAILABLE and st.button("Show 3D structure"):
                            show_3d_molecule(mol)
            st.markdown(f"[Open this compound on PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/{cid})")
        except Exception as exc:
            st.error(f"PubChem search failed: {exc}")
            st.info("Check the spelling and internet connection, then try again.")


# -------------------------------------------------------------------
# Structure-property analysis
# -------------------------------------------------------------------
elif page == "Structure–Property Analysis":
    st.subheader("Compare Molecular Properties")
    if not RDKIT_AVAILABLE:
        st.error("RDKit is required for this section.")
    else:
        first = st.text_input("Molecule 1 SMILES", "CCO")
        second = st.text_input("Molecule 2 SMILES", "c1ccccc1")
        if st.button("Compare molecules"):
            mol1, err1 = parse_smiles(first)
            mol2, err2 = parse_smiles(second)
            if err1 or err2:
                st.error(err1 or err2)
            else:
                d1 = molecule_descriptors(mol1)
                d2 = molecule_descriptors(mol2)
                comparison = pd.DataFrame({"Molecule 1": d1, "Molecule 2": d2})
                st.dataframe(comparison, use_container_width=True)
                numeric_keys = [
                    "Molecular weight (g/mol)", "LogP", "TPSA (Å²)",
                    "H-bond donors", "H-bond acceptors", "Rotatable bonds", "Rings",
                ]
                chart_data = pd.DataFrame({
                    "Descriptor": numeric_keys,
                    "Molecule 1": [d1[k] for k in numeric_keys],
                    "Molecule 2": [d2[k] for k in numeric_keys],
                }).set_index("Descriptor")
                st.bar_chart(chart_data)


# -------------------------------------------------------------------
# Theory
# -------------------------------------------------------------------
elif page == "Theory & Learning":
    st.subheader("Basic Cheminformatics Concepts")
    with st.expander("What is cheminformatics?"):
        st.write("Cheminformatics uses computational and information methods to store, search, analyze and visualize chemical information.")
    with st.expander("What is SMILES?"):
        st.write("SMILES is a text notation that represents atoms and bonds in a molecule. For example, CCO represents ethanol.")
    with st.expander("What is a molecular descriptor?"):
        st.write("A molecular descriptor is a numerical or categorical value that describes a property of a molecule, such as molecular weight, LogP or topological polar surface area.")
    with st.expander("What is 3D molecular visualization?"):
        st.write("A 3D molecular model displays atoms and bonds in three-dimensional space. It can be rotated and zoomed to inspect molecular geometry.")
    with st.expander("What is the periodic table?"):
        st.write("The periodic table arranges chemical elements by increasing atomic number and recurring chemical properties.")


# -------------------------------------------------------------------
# Assessment
# -------------------------------------------------------------------
elif page == "Assessment":
    st.subheader("Chemistry Assessment")
    questions = [
        ("What does SMILES represent?", ["A chemical structure as text", "A type of microscope", "A unit of pressure"], 0),
        ("What is the atomic number of carbon?", ["4", "6", "8"], 1),
        ("Which descriptor is commonly associated with lipophilicity?", ["TPSA", "LogP", "Ring count"], 1),
        ("How many officially named elements are in the periodic table?", ["108", "118", "128"], 1),
        ("Which tool can generate molecular conformers in this project?", ["RDKit", "Spreadsheet only", "Word processor"], 0),
    ]
    answers = {}
    for i, (question, options, correct) in enumerate(questions):
        answers[i] = st.radio(question, options, key=f"quiz_{i}")
    if st.button("Submit assessment"):
        score = sum(1 for i, (_, options, correct) in enumerate(questions) if options.index(answers[i]) == correct)
        st.success(f"Your score: {score} / {len(questions)}")
        st.write("Review the theory section for concepts you would like to practise again.")


# -------------------------------------------------------------------
# Final student report
# -------------------------------------------------------------------
elif page == "Student Project Report":
    st.subheader("Student Project Report")
    st.markdown("### Cheminformatics Virtual Laboratory")
    st.write(f"**Student Name:** {STUDENT_NAME}")
    st.write(f"**Register Number:** {REGISTER_NUMBER}")
    st.write(f"**Institution:** {INSTITUTION}")
    st.write(f"**Project Area:** Chemistry / Cheminformatics")
    st.markdown("### Aim")
    st.write("To develop an educational web application that helps students explore chemical elements, molecular structures and molecular properties.")
    st.markdown("### Objectives")
    st.markdown("""
    1. Display the complete periodic table containing 118 elements.
    2. Visualize chemical compounds in two and three dimensions.
    3. Calculate selected molecular descriptors using RDKit.
    4. Search compound information through PubChem when internet access is available.
    5. Generate a downloadable molecular properties report.
    """)
    st.markdown("### Software and libraries")
    st.write("Python, Streamlit, RDKit, py3Dmol, stmol, pandas, Matplotlib and ReportLab.")
    st.markdown("### Faculty details")
    st.write(f"**{FACULTY_NAME}**")
    st.write(FACULTY_DESIGNATION)
    st.write(FACULTY_DEPARTMENT)
    st.write(INSTITUTION)
    st.info(f"Contact: {FACULTY_CONTACT}")


show_student_footer()
