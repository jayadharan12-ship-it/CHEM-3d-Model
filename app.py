
import io
import json
import urllib.parse
import urllib.request

import pandas as pd
import streamlit as st


# --------------------------------------------------
# OPTIONAL LIBRARIES
# --------------------------------------------------

RDKIT_AVAILABLE = False
RDKIT_ERROR = ""

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, Draw, rdMolDescriptors
    from rdkit.Chem import rdDepictor
    RDKIT_AVAILABLE = True
except Exception as e:
    RDKIT_ERROR = str(e)

THREE_D_AVAILABLE = False

try:
    import py3Dmol
    from stmol import showmol
    THREE_D_AVAILABLE = True
except Exception:
    pass

PDF_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    PDF_AVAILABLE = True
except Exception:
    pass

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NEXCHEM Virtual Lab",
    page_icon="🧪",
    layout="wide"
)

# --------------------------------------------------
# STUDENT DETAILS
# --------------------------------------------------

STUDENT_NAME = "R. JAYADHARAN"
REGISTER_NUMBER = "RA2611026050288"
INSTITUTION = "SRM Institute of Science and Technology, Tiruchirappalli"

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

.stApp {
    background:
    radial-gradient(circle at 10% 10%, #173d52, transparent 35%),
    radial-gradient(circle at 90% 15%, #29285b, transparent 35%),
    linear-gradient(135deg, #07111f, #10152c);
    color: #eaf3ff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
}

section[data-testid="stSidebar"] {
    background: #0b192b;
}

.hero {
    padding: 35px;
    border-radius: 24px;
    margin-bottom: 25px;
    background: linear-gradient(110deg, #10475a, #263b78, #47356f);
    border: 1px solid #54f0d0;
    box-shadow: 0 15px 45px #00000055;
}

.hero h1 {
    color: white;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
}

.hero p {
    color: #d9f8ff;
    font-size: 16px;
}

div[data-testid="stMetric"] {
    background: #142943;
    border: 1px solid #31536b;
    border-radius: 15px;
    padding: 15px;
}

.stButton button {
    background: linear-gradient(100deg, #54f0d0, #72c8ff);
    color: #07111f;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

.element {
    text-align: center;
    border-radius: 8px;
    padding: 5px 2px;
    color: #102030;
    min-height: 65px;
}

.element b {
    font-size: 19px;
}

.element small {
    font-size: 10px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# PERIODIC TABLE DATA
# --------------------------------------------------

ELEMENTS_DATA = [
("H","Hydrogen"),("He","Helium"),
("Li","Lithium"),("Be","Beryllium"),("B","Boron"),
("C","Carbon"),("N","Nitrogen"),("O","Oxygen"),
("F","Fluorine"),("Ne","Neon"),
("Na","Sodium"),("Mg","Magnesium"),("Al","Aluminium"),
("Si","Silicon"),("P","Phosphorus"),("S","Sulfur"),
("Cl","Chlorine"),("Ar","Argon"),
("K","Potassium"),("Ca","Calcium"),("Sc","Scandium"),
("Ti","Titanium"),("V","Vanadium"),("Cr","Chromium"),
("Mn","Manganese"),("Fe","Iron"),("Co","Cobalt"),
("Ni","Nickel"),("Cu","Copper"),("Zn","Zinc"),
("Ga","Gallium"),("Ge","Germanium"),("As","Arsenic"),
("Se","Selenium"),("Br","Bromine"),("Kr","Krypton"),
("Rb","Rubidium"),("Sr","Strontium"),("Y","Yttrium"),
("Zr","Zirconium"),("Nb","Niobium"),("Mo","Molybdenum"),
("Tc","Technetium"),("Ru","Ruthenium"),("Rh","Rhodium"),
("Pd","Palladium"),("Ag","Silver"),("Cd","Cadmium"),
("In","Indium"),("Sn","Tin"),("Sb","Antimony"),
("Te","Tellurium"),("I","Iodine"),("Xe","Xenon"),
("Cs","Caesium"),("Ba","Barium"),("La","Lanthanum"),
("Ce","Cerium"),("Pr","Praseodymium"),("Nd","Neodymium"),
("Pm","Promethium"),("Sm","Samarium"),("Eu","Europium"),
("Gd","Gadolinium"),("Tb","Terbium"),("Dy","Dysprosium"),
("Ho","Holmium"),("Er","Erbium"),("Tm","Thulium"),
("Yb","Ytterbium"),("Lu","Lutetium"),
("Hf","Hafnium"),("Ta","Tantalum"),("W","Tungsten"),
("Re","Rhenium"),("Os","Osmium"),("Ir","Iridium"),
("Pt","Platinum"),("Au","Gold"),("Hg","Mercury"),
("Tl","Thallium"),("Pb","Lead"),("Bi","Bismuth"),
("Po","Polonium"),("At","Astatine"),("Rn","Radon"),
("Fr","Francium"),("Ra","Radium"),("Ac","Actinium"),
("Th","Thorium"),("Pa","Protactinium"),("U","Uranium"),
("Np","Neptunium"),("Pu","Plutonium"),("Am","Americium"),
("Cm","Curium"),("Bk","Berkelium"),("Cf","Californium"),
("Es","Einsteinium"),("Fm","Fermium"),("Md","Mendelevium"),
("No","Nobelium"),("Lr","Lawrencium"),
("Rf","Rutherfordium"),("Db","Dubnium"),("Sg","Seaborgium"),
("Bh","Bohrium"),("Hs","Hassium"),("Mt","Meitnerium"),
("Ds","Darmstadtium"),("Rg","Roentgenium"),("Cn","Copernicium"),
("Nh","Nihonium"),("Fl","Flerovium"),("Mc","Moscovium"),
("Lv","Livermorium"),("Ts","Tennessine"),("Og","Oganesson")
]

ELEMENT_DF = pd.DataFrame(
    [(i + 1, symbol, name) for i, (symbol, name) in enumerate(ELEMENTS_DATA)],
    columns=["Atomic Number", "Symbol", "Element"]
)

# --------------------------------------------------
# CHEMISTRY FUNCTIONS
# --------------------------------------------------

def parse_smiles(smiles):
    if not RDKIT_AVAILABLE:
        return None, "RDKit is unavailable. Check requirements.txt."

    mol = Chem.MolFromSmiles(smiles.strip())

    if mol is None:
        return None, "Invalid SMILES. Please check your input."

    return mol, None


def calculate_descriptors(mol):
    return {
        "Molecular Formula":
            rdMolDescriptors.CalcMolFormula(mol),

        "Molecular Weight (g/mol)":
            round(Descriptors.MolWt(mol), 3),

        "Exact Molecular Weight":
            round(Descriptors.ExactMolWt(mol), 4),

        "LogP":
            round(Descriptors.MolLogP(mol), 3),

        "TPSA (Å²)":
            round(Descriptors.TPSA(mol), 3),

        "Hydrogen Bond Donors":
            Descriptors.NumHDonors(mol),

        "Hydrogen Bond Acceptors":
            Descriptors.NumHAcceptors(mol),

        "Rotatable Bonds":
            Descriptors.NumRotatableBonds(mol),

        "Number of Rings":
            rdMolDescriptors.CalcNumRings(mol),

        "Heavy Atoms":
            mol.GetNumHeavyAtoms(),

        "Total Atoms":
            Chem.AddHs(mol).GetNumAtoms(),

        "Fraction Csp3":
            round(rdMolDescriptors.CalcFractionCSP3(mol), 3)
    }


def draw_2d(mol):
    molecule = Chem.Mol(mol)
    rdDepictor.Compute2DCoords(molecule)
    return Draw.MolToImage(molecule, size=(650, 450))


def generate_3d(mol):
    molecule = Chem.AddHs(Chem.Mol(mol))

    parameters = AllChem.ETKDGv3()
    parameters.randomSeed = 42

    result = AllChem.EmbedMolecule(molecule, parameters)

    if result != 0:
        raise ValueError("Could not generate 3D coordinates.")

    try:
        AllChem.MMFFOptimizeMolecule(molecule)
    except Exception:
        AllChem.UFFOptimizeMolecule(molecule)

    return molecule


def display_3d(mol, style):
    molecule = generate_3d(mol)

    viewer = py3Dmol.view(width=850, height=520)

    viewer.addModel(
        Chem.MolToMolBlock(molecule),
        "mol"
    )

    styles = {
        "Ball and Stick": {
            "stick": {"radius": 0.16},
            "sphere": {"scale": 0.28}
        },
        "Stick": {
            "stick": {"radius": 0.22}
        },
        "Space Filling": {
            "sphere": {"scale": 0.85}
        },
        "Wireframe": {
            "line": {"linewidth": 2}
        }
    }

    viewer.setStyle(styles[style])
    viewer.setBackgroundColor("#101820")
    viewer.zoomTo()

    showmol(viewer, height=540, width=900)


def search_pubchem(compound):
    name = urllib.parse.quote(compound.strip())

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
        f"compound/name/{name}/property/"
        "MolecularFormula,MolecularWeight,IUPACName,"
        "CanonicalSMILES,IsomericSMILES/JSON"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "NEXCHEM-Virtual-Lab"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def create_pdf(compound, properties):
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 60

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(45, y, "NEXCHEM VIRTUAL LAB")

    y -= 35

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(45, y, "Molecular Properties Report")

    y -= 35

    pdf.setFont("Helvetica", 10)

    lines = [
        f"Student: {STUDENT_NAME}",
        f"Register Number: {REGISTER_NUMBER}",
        f"Institution: {INSTITUTION}",
        f"Compound: {compound}",
        "",
        "Calculated Properties:"
    ]

    for line in lines:
        pdf.drawString(45, y, line)
        y -= 18

    for key, value in properties.items():

        if y < 60:
            pdf.showPage()
            y = height - 60

        pdf.drawString(55, y, f"{key}: {value}")
        y -= 18

    pdf.save()

    buffer.seek(0)

    return buffer


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🧪 NEXCHEM VIRTUAL LAB")

st.sidebar.caption(STUDENT_NAME)
st.sidebar.caption(REGISTER_NUMBER)

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "3D Molecular Visualization",
        "Molecular Properties",
        "Periodic Table",
        "PubChem Search",
        "Structure–Property Analysis",
        "Theory & Learning",
        "Assessment",
        "Student Project Report"
    ]
)

# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(f"""
<div class="hero">
    <h1>🧪 NEXCHEM VIRTUAL LAB</h1>
    <p>Explore Molecules. Discover Properties. Experience Chemistry in 3D.</p>
    <p>Interactive Cheminformatics Learning Platform</p>
    <p>Student Project · {STUDENT_NAME}</p>
</div>
""", unsafe_allow_html=True)

if not RDKIT_AVAILABLE:
    st.warning(
        "RDKit is unavailable. Molecular visualization and "
        "descriptor features are disabled until RDKit is installed."
    )

    with st.expander("RDKit diagnostic"):
        st.code(RDKIT_ERROR or "No additional error information.")


# ==================================================
# HOME
# ==================================================

if page == "Home":

    st.subheader("Welcome to Cheminformatics Virtual Laboratory")

    st.write(
        "This educational application introduces chemical "
        "elements, molecular structures, molecular descriptors "
        "and compound information."
    )

    a, b, c = st.columns(3)

    a.metric("Chemical Elements", "118")
    b.metric("Molecular Visualization", "2D + 3D")
    c.metric("Learning Modules", "9")

    st.markdown("### Main Features")

    st.markdown("""
    - Interactive molecular visualization.
    - Molecular property calculation.
    - Complete 118-element periodic table.
    - PubChem compound search.
    - Structure-property comparison.
    - Downloadable PDF reports.
    - Chemistry theory and assessment.
    """)

    st.markdown("### Example Compounds")

    examples = pd.DataFrame([
        ["Water", "O"],
        ["Ethanol", "CCO"],
        ["Benzene", "c1ccccc1"],
        ["Phenol", "Oc1ccccc1"],
        ["Acetic Acid", "CC(=O)O"],
        ["Aspirin", "CC(=O)Oc1ccccc1C(=O)O"],
        ["Caffeine", "Cn1c(=O)c2c(ncn2C)n(C)c1=O"]
    ], columns=["Compound", "SMILES"])

    st.dataframe(examples, use_container_width=True, hide_index=True)


# ==================================================
# 3D MOLECULAR VISUALIZATION
# ==================================================

elif page == "3D Molecular Visualization":

    st.subheader("Interactive 3D Molecular Visualization")

    compounds = {
        "Ethanol": "CCO",
        "Benzene": "c1ccccc1",
        "Phenol": "Oc1ccccc1",
        "Acetic Acid": "CC(=O)O",
        "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
        "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
        "Water": "O",
        "Custom SMILES": ""
    }

    choice = st.selectbox(
        "Select Compound",
        list(compounds.keys())
    )

    smiles = st.text_input(
        "Enter SMILES",
        value=compounds[choice]
    )

    style = st.selectbox(
        "Molecular Display Style",
        [
            "Ball and Stick",
            "Stick",
            "Space Filling",
            "Wireframe"
        ]
    )

    if st.button("Visualize Molecule", type="primary"):

        mol, error = parse_smiles(smiles)

        if error:
            st.error(error)

        else:

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 2D Structure")
                st.image(draw_2d(mol), use_container_width=True)

            with col2:
                st.markdown("### 3D Structure")

                if THREE_D_AVAILABLE:

                    try:
                        display_3d(mol, style)

                    except Exception as e:
                        st.error(f"3D visualization error: {e}")

                else:
                    st.info(
                        "Install py3Dmol and stmol to enable "
                        "interactive 3D visualization."
                    )

            st.session_state["last_smiles"] = smiles

            st.success("Molecular structure successfully loaded.")


# ==================================================
# MOLECULAR PROPERTIES
# ==================================================

elif page == "Molecular Properties":

    st.subheader("Molecular Properties Calculator")

    smiles = st.text_input(
        "Enter SMILES",
        value=st.session_state.get("last_smiles", "CCO")
    )

    compound = st.text_input(
        "Compound Name",
        "User Compound"
    )

    if st.button("Calculate Properties", type="primary"):

        mol, error = parse_smiles(smiles)

        if error:
            st.error(error)

        else:

            properties = calculate_descriptors(mol)

            st.session_state["last_properties"] = properties
            st.session_state["last_compound"] = compound

            st.markdown("### 2D Molecular Structure")

            st.image(draw_2d(mol), use_container_width=False)

            st.markdown("### Calculated Molecular Properties")

            col1, col2 = st.columns(2)

            items = list(properties.items())
            middle = (len(items) + 1) // 2

            with col1:
                for key, value in items[:middle]:
                    st.metric(key, value)

            with col2:
                for key, value in items[middle:]:
                    st.metric(key, value)

            if PDF_AVAILABLE:

                st.download_button(
                    "📄 Download PDF Report",
                    data=create_pdf(compound, properties),
                    file_name="molecular_properties_report.pdf",
                    mime="application/pdf"
                )

            else:
                st.info("Install ReportLab to enable PDF downloads.")


# ==================================================
# PERIODIC TABLE
# ==================================================

elif page == "Periodic Table":

    st.subheader("Periodic Table – All 118 Elements")

    search = st.text_input("Search Element")

    filtered = ELEMENT_DF.copy()

    if search:
        filtered = filtered[
            filtered["Element"].str.contains(
                search, case=False, na=False
            )
            |
            filtered["Symbol"].str.contains(
                search, case=False, na=False
            )
        ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    selected = st.selectbox(
        "Select an Element",
        ELEMENT_DF["Element"].tolist()
    )

    element = ELEMENT_DF[
        ELEMENT_DF["Element"] == selected
    ].iloc[0]

    a, b, c = st.columns(3)

    a.metric("Element", element["Element"])
    b.metric("Symbol", element["Symbol"])
    c.metric("Atomic Number", int(element["Atomic Number"]))

    st.info(
        "The table includes all 118 elements. "
        "This section provides atomic numbers and element symbols."
    )


# ==================================================
# PUBCHEM SEARCH
# ==================================================

elif page == "PubChem Search":

    st.subheader("PubChem Compound Search")

    query = st.text_input(
        "Enter Compound Name",
        placeholder="Example: Aspirin, Caffeine, Glucose"
    )

    if st.button("Search PubChem", type="primary"):

        if not query.strip():
            st.warning("Enter a compound name.")

        else:

            try:

                with st.spinner("Searching PubChem..."):

                    result = search_pubchem(query)

                properties = result["PropertyTable"]["Properties"][0]

                st.success("Compound found!")

                st.json(properties)

                smiles = (
                    properties.get("ConnectivitySMILES")
                    or properties.get("CanonicalSMILES")
                    or properties.get("IsomericSMILES")
                )

                if smiles:

                    st.markdown("### SMILES Structure")

                    st.code(smiles)

                    st.session_state["last_smiles"] = smiles

                    if RDKIT_AVAILABLE:

                        mol, error = parse_smiles(smiles)

                        if not error:
                            st.image(draw_2d(mol))

                cid = properties.get("CID")

                if cid:

                    st.markdown(
                        f"[Open compound in PubChem]"
                        f"(https://pubchem.ncbi.nlm.nih.gov/compound/{cid})"
                    )

            except Exception as e:

                st.error(f"PubChem search failed: {e}")

                st.info(
                    "Check the spelling and internet connection."
                )


# ==================================================
# STRUCTURE PROPERTY ANALYSIS
# ==================================================

elif page == "Structure–Property Analysis":

    st.subheader("Compare Two Molecular Structures")

    smiles1 = st.text_input("Molecule 1 SMILES", "CCO")

    smiles2 = st.text_input("Molecule 2 SMILES", "c1ccccc1")

    if st.button("Compare Molecules", type="primary"):

        mol1, error1 = parse_smiles(smiles1)
        mol2, error2 = parse_smiles(smiles2)

        if error1 or error2:

            st.error(error1 or error2)

        else:

            d1 = calculate_descriptors(mol1)
            d2 = calculate_descriptors(mol2)

            comparison = pd.DataFrame({
                "Molecule 1": d1,
                "Molecule 2": d2
            })

            st.dataframe(
                comparison,
                use_container_width=True
            )

            chart_data = pd.DataFrame({
                "Molecule 1": [
                    d1["Molecular Weight (g/mol)"],
                    d1["LogP"],
                    d1["TPSA (Å²)"]
                ],
                "Molecule 2": [
                    d2["Molecular Weight (g/mol)"],
                    d2["LogP"],
                    d2["TPSA (Å²)"]
                ]
            }, index=["Molecular Weight", "LogP", "TPSA"])

            st.markdown("### Property Comparison Chart")

            st.bar_chart(chart_data)


# ==================================================
# THEORY AND LEARNING
# ==================================================

elif page == "Theory & Learning":

    st.subheader("Cheminformatics Theory & Learning")

    topics = {
        "What is Cheminformatics?":
            "Cheminformatics uses computational and information "
            "methods to store, search, analyze and visualize chemical data.",

        "What is SMILES?":
            "SMILES is a text-based notation used to represent "
            "chemical structures. For example, CCO represents ethanol.",

        "What is a Molecular Descriptor?":
            "A molecular descriptor is a numerical or categorical "
            "value that describes a molecular property.",

        "What is LogP?":
            "LogP is a descriptor used to estimate the partitioning "
            "of a compound between octanol and water.",

        "What is TPSA?":
            "Topological Polar Surface Area estimates the polar "
            "surface area of a molecule.",

        "What is 3D Molecular Visualization?":
            "A 3D molecular model displays atoms and bonds in "
            "three-dimensional space.",

        "What is PubChem?":
            "PubChem is a public chemical database containing "
            "compound information and chemical structures."
    }

    for title, explanation in topics.items():

        with st.expander(title):
            st.write(explanation)


# ==================================================
# ASSESSMENT
# ==================================================

elif page == "Assessment":

    st.subheader("Chemistry Self Assessment")

    questions = [
        (
            "1. What does SMILES represent?",
            [
                "Chemical structure as text",
                "A microscope",
                "A pressure unit"
            ],
            0
        ),

        (
            "2. What is the atomic number of Carbon?",
            ["4", "6", "8"],
            1
        ),

        (
            "3. Which descriptor is associated with lipophilicity?",
            ["TPSA", "LogP", "Ring Count"],
            1
        ),

        (
            "4. How many elements are in the periodic table?",
            ["108", "118", "128"],
            1
        ),

        (
            "5. Which library is used for molecular calculations?",
            ["RDKit", "Word", "PowerPoint"],
            0
        )
    ]

    answers = []

    for question, options, correct in questions:

        answer = st.radio(
            question,
            options,
            key=question
        )

        answers.append(answer)

    if st.button("Submit Assessment", type="primary"):

        score = 0

        for i, (question, options, correct) in enumerate(questions):

            if options.index(answers[i]) == correct:
                score += 1

        st.success(
            f"Your Score: {score} / {len(questions)}"
        )

        if score == len(questions):
            st.balloons()
            st.write("Excellent work!")

        else:
            st.write("Review the theory section and try again.")


# ==================================================
# STUDENT PROJECT REPORT
# ==================================================

elif page == "Student Project Report":

    st.subheader("Student Project Report")

    st.markdown("### Project Title")

    st.title("NEXCHEM VIRTUAL LAB")

    st.markdown("### Student Details")

    st.write(f"**Name:** {STUDENT_NAME}")

    st.write(f"**Register Number:** {REGISTER_NUMBER}")

    st.write(f"**Institution:** {INSTITUTION}")

    st.write("**Project Area:** Chemistry / Cheminformatics")

    st.markdown("### Aim")

    st.write(
        "To develop an educational web application that "
        "helps students explore chemical elements, molecular "
        "structures and molecular properties."
    )

    st.markdown("### Objectives")

    st.markdown("""
    1. Display all 118 chemical elements.
    2. Visualize molecular structures in 2D and 3D.
    3. Calculate molecular descriptors.
    4. Search chemical compounds using PubChem.
    5. Compare molecular properties.
    6. Generate downloadable PDF reports.
    """)

    st.markdown("### Technologies Used")

    st.markdown("""
    - Python
    - Streamlit
    - RDKit
    - py3Dmol
    - stmol
    - Pandas
    - ReportLab
    """)

    st.markdown("### Conclusion")

    st.write(
        "The NEXCHEM Virtual Lab provides an interactive "
        "environment for learning basic cheminformatics concepts "
        "and exploring chemical structures and properties."
    )

    st.info(
        "This application is intended for educational purposes. "
        "Calculated molecular properties are computational estimates."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("### 🎓 Student Information")

st.write(f"**Name:** {STUDENT_NAME}")

st.write(f"**Register Number:** {REGISTER_NUMBER}")

st.write(f"**Institution:** {INSTITUTION}")

st.caption("NEXCHEM VIRTUAL LAB · Student Educational Project")
