
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors
from rdkit.Chem import AllChem
from rdkit.Chem import rdchem
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="NEXCHEM | Virtual Laboratory",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# STUDENT DETAILS
# -----------------------------------------

STUDENT_NAME = "R. JAYADHARAN"
REGISTER_NUMBER = "RA2611026050288"
INSTITUTION = "SRM Institute of Science and Technology, Tiruchirappalli"

# -----------------------------------------
# CUSTOM CSS AND ANIMATIONS
# -----------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

.stApp {
    background:
      radial-gradient(circle at 10% 10%, #123e52 0%, transparent 35%),
      radial-gradient(circle at 90% 20%, #29265d 0%, transparent 35%),
      linear-gradient(135deg, #07111f, #101a31, #10132a);
    background-attachment: fixed;
    color: #eaf3ff;
    font-family: Inter, sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091a2d, #151a38);
    border-right: 1px solid #254b65;
}

.hero {
    padding: 35px;
    border-radius: 24px;
    background: linear-gradient(120deg, #10445b, #23447e, #49316e);
    border: 1px solid #4c8baf;
    box-shadow: 0 15px 45px rgba(0,0,0,.3);
    animation: appear 1s ease;
    margin-bottom: 25px;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    color: white;
}

.hero p {
    color: #d3eaff;
    font-size: 16px;
}

.hero-tag {
    display: inline-block;
    padding: 8px 15px;
    background: rgba(84,240,208,.13);
    border: 1px solid #54f0d0;
    border-radius: 30px;
    color: #aaf9e8;
    font-size: 12px;
}

div[data-testid="stMetric"] {
    background: rgba(23, 48, 76, .8);
    border: 1px solid #315b7b;
    padding: 18px;
    border-radius: 16px;
    transition: .3s;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: #54f0d0;
}

.stButton button {
    background: linear-gradient(100deg, #54f0d0, #72c8ff);
    color: #071827;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    transition: .25s;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px #1b9f9b55;
}

.element-card {
    background: rgba(23, 48, 76, .85);
    border: 1px solid #42627c;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    margin: 4px;
}

@keyframes appear {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# HEADER
# -----------------------------------------

st.markdown(f"""
<div class="hero">
    <h1>🧪 NEXCHEM VIRTUAL LAB</h1>
    <p>Explore molecules. Discover properties. Experience chemistry.</p>
    <p>Interactive Cheminformatics Learning Platform</p>
    <span class="hero-tag">STUDENT PROJECT | SRM IST</span>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:
    st.title("🧪 NEXCHEM")
    st.caption("CHEMISTRY VIRTUAL LAB")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "⚛️ Periodic Table",
            "🧬 Molecular Explorer",
            "📊 Molecular Properties",
            "🔬 Chemistry Theory",
            "📝 Quiz",
            "📄 Student Report"
        ]
    )

    st.divider()

    st.markdown("### Student Profile")
    st.write(STUDENT_NAME)
    st.caption(REGISTER_NUMBER)
    st.caption("SRM Institute of Science and Technology")

# -----------------------------------------
# DASHBOARD
# -----------------------------------------

if page == "🏠 Dashboard":

    st.title("Welcome to NEXCHEM")

    st.write(
        "A digital chemistry laboratory for exploring "
        "chemical elements, molecular structures and properties."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Elements", "118")
    c2.metric("Molecular Tools", "3")
    c3.metric("Learning Modules", "4")

    st.divider()

    st.subheader("Explore the Laboratory")

    cards = st.columns(3)

    with cards[0]:
        st.markdown("### ⚛️ Periodic Table")
        st.write("Explore all 118 chemical elements.")

    with cards[1]:
        st.markdown("### 🧬 Molecule Explorer")
        st.write("Enter SMILES and visualize molecules.")

    with cards[2]:
        st.markdown("### 📊 Molecular Properties")
        st.write("Calculate important molecular descriptors.")

    st.info(
        "Start exploring using the navigation menu on the left."
    )

# -----------------------------------------
# PERIODIC TABLE
# -----------------------------------------

elif page == "⚛️ Periodic Table":

    st.title("⚛️ Interactive Periodic Table")

    periodic_table = Chem.GetPeriodicTable()

    atomic_number = st.selectbox(
        "Select Atomic Number",
        range(1, 119)
    )

    symbol = periodic_table.GetElementSymbol(atomic_number)
    name = periodic_table.GetElementName(atomic_number)
    atomic_mass = periodic_table.GetAtomicWeight(atomic_number)

    st.markdown(
        f"""
        <div class="element-card">
            <h1 style="font-size:65px;color:#54f0d0;">{symbol}</h1>
            <h2>{name}</h2>
            <p>Atomic Number: {atomic_number}</p>
            <p>Atomic Mass: {atomic_mass:.3f} u</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Element Information")

    a, b, c = st.columns(3)
    a.metric("Atomic Number", atomic_number)
    b.metric("Symbol", symbol)
    c.metric("Atomic Mass", f"{atomic_mass:.3f} u")

    st.caption(
        "Element information is provided through RDKit's periodic table."
    )

# -----------------------------------------
# MOLECULAR EXPLORER
# -----------------------------------------

elif page == "🧬 Molecular Explorer":

    st.title("🧬 Molecular Structure Explorer")

    examples = {
        "Water": "O",
        "Methane": "C",
        "Ethanol": "CCO",
        "Acetic Acid": "CC(=O)O",
        "Benzene": "c1ccccc1",
        "Aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "Glucose": "C(C1C(C(C(C(O1)O)O)O)O)O"
    }

    selected = st.selectbox(
        "Choose an example molecule",
        list(examples.keys())
    )

    smiles = st.text_input(
        "Enter SMILES notation",
        value=examples[selected]
    )

    if st.button("Generate Molecular Structure"):

        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            st.error("Invalid SMILES notation. Please try again.")

        else:
            st.success("Molecule generated successfully!")

            mol = Chem.AddHs(mol)

            AllChem.Compute2DCoords(mol)

            image = Draw.MolToImage(
                mol,
                size=(650, 450),
                legend="NEXCHEM Molecular Structure"
            )

            st.image(
                image,
                caption="2D Molecular Structure",
                use_container_width=True
            )

            st.subheader("Molecular Information")

            st.write("SMILES:", Chem.MolToSmiles(mol))
            st.write("Atoms:", mol.GetNumAtoms())
            st.write("Bonds:", mol.GetNumBonds())

            st.download_button(
                "Download Molecular Image",
                data=BytesIO(
                    image.save(BytesIO(), format="PNG")
                ).getvalue() if False else _image_bytes(image),
                file_name="molecule.png",
                mime="image/png"
            )

# -----------------------------------------
# IMAGE HELPER
# -----------------------------------------

def _image_bytes(image):
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()

# -----------------------------------------
# MOLECULAR PROPERTIES
# -----------------------------------------

elif page == "📊 Molecular Properties":

    st.title("📊 Molecular Property Calculator")

    smiles = st.text_input(
        "Enter a molecule's SMILES",
        "CCO"
    )

    if st.button("Calculate Properties"):

        mol = Chem.MolFromSmiles(smiles)

        if mol is None:
            st.error("Invalid molecular structure.")

        else:
            data = {
                "Molecular Weight": Descriptors.MolWt(mol),
                "LogP": Descriptors.MolLogP(mol),
                "TPSA": Descriptors.TPSA(mol),
                "H-Bond Donors": Descriptors.NumHDonors(mol),
                "H-Bond Acceptors": Descriptors.NumHAcceptors(mol),
                "Rotatable Bonds": Descriptors.NumRotatableBonds(mol),
                "Heavy Atoms": Descriptors.HeavyAtomCount(mol),
                "Molecular Formula": rdMolDescriptors.CalcMolFormula(mol)
            }

            st.subheader("Calculated Properties")

            c1, c2 = st.columns(2)

            c1.metric(
                "Molecular Weight",
                f"{data['Molecular Weight']:.2f} g/mol"
            )

            c2.metric(
                "LogP",
                f"{data['LogP']:.2f}"
            )

            st.dataframe(
                pd.DataFrame(
                    list(data.items()),
                    columns=["Property", "Value"]
                ),
                use_container_width=True
            )

            numeric_data = {
                key: value for key, value in data.items()
                if isinstance(value, (int, float))
            }

            fig, ax = plt.subplots(figsize=(9, 4))
            ax.bar(
                numeric_data.keys(),
                numeric_data.values()
            )
            ax.set_title("Molecular Descriptor Overview")
            ax.tick_params(axis="x", rotation=35)
            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

# -----------------------------------------
# CHEMISTRY THEORY
# -----------------------------------------

elif page == "🔬 Chemistry Theory":

    st.title("🔬 Chemistry Learning Centre")

    topics = {
        "Quantum Mechanics": """
        Quantum mechanics describes the behaviour of matter at atomic
        and subatomic scales.

        Important concepts:
        - Wave-particle duality
        - Quantization of energy
        - Probability interpretation
        - Schrödinger wave equation
        """,

        "Schrödinger Equation": r"""
        The time-independent Schrödinger equation is:

        Hψ = Eψ

        Where:
        - H = Hamiltonian operator
        - ψ = Wave function
        - E = Energy eigenvalue
        """,

        "Molecular Orbitals": """
        Molecular orbital theory explains chemical bonding by combining
        atomic orbitals to form molecular orbitals.

        Main types:
        - Bonding orbitals
        - Antibonding orbitals
        """,

        "Chemical Bonding": """
        Chemical bonding explains how atoms combine to form molecules.

        Main types:
        - Ionic bonding
        - Covalent bonding
        - Metallic bonding
        - Hydrogen bonding
        """,

        "Thermodynamics": """
        Thermodynamics studies energy, heat and work.

        Important quantities:
        - Internal energy
        - Enthalpy
        - Entropy
        - Gibbs free energy
        """
    }

    topic = st.selectbox(
        "Choose a topic",
        list(topics.keys())
    )

    st.markdown("### " + topic)
    st.write(topics[topic])

# -----------------------------------------
# QUIZ
# -----------------------------------------

elif page == "📝 Quiz":

    st.title("📝 Chemistry Knowledge Quiz")

    questions = [
        {
            "question": "What is the chemical symbol for Oxygen?",
            "options": ["O", "Ox", "Og", "On"],
            "answer": "O"
        },
        {
            "question": "What is the molecular formula of water?",
            "options": ["CO2", "H2O", "O2", "H2"],
            "answer": "H2O"
        },
        {
            "question": "Which scientist developed the wave equation?",
            "options": [
                "Newton",
                "Schrödinger",
                "Faraday",
                "Dalton"
            ],
            "answer": "Schrödinger"
        },
        {
            "question": "What is the atomic number of Carbon?",
            "options": ["4", "6", "8", "12"],
            "answer": "6"
        },
        {
            "question": "Which bond involves sharing electrons?",
            "options": [
                "Ionic",
                "Covalent",
                "Metallic",
                "None"
            ],
            "answer": "Covalent"
        }
    ]

    with st.form("chemistry_quiz"):

        answers = []

        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")

            answer = st.radio(
                "Choose your answer",
                q["options"],
                key=f"question_{i}"
            )

            answers.append(answer)
            st.divider()

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:

        score = sum(
            answers[i] == questions[i]["answer"]
            for i in range(len(questions))
        )

        st.success(
            f"Your score: {score}/{len(questions)}"
        )

        st.progress(score / len(questions))

        for i, q in enumerate(questions):
            if answers[i] == q["answer"]:
                st.write(f"Q{i+1}: Correct")
            else:
                st.write(
                    f"Q{i+1}: Correct answer: {q['answer']}"
                )

# -----------------------------------------
# STUDENT REPORT
# -----------------------------------------

elif page == "📄 Student Report":

    st.title("📄 Student Project Report")

    st.subheader("Student Information")

    st.write("**Name:**", STUDENT_NAME)
    st.write("**Register Number:**", REGISTER_NUMBER)
    st.write("**Institution:**", INSTITUTION)

    st.divider()

    st.subheader("Project Information")

    st.write("**Project:** Cheminformatics Virtual Laboratory")

    st.write("""
    This project provides an interactive chemistry learning
    environment using Python, Streamlit and RDKit.

    Features include:
    - Interactive periodic table
    - Molecular structure visualization
    - Molecular property calculation
    - Chemistry theory modules
    - Knowledge assessment quiz
    """)

    if st.button("Generate Student PDF Report"):

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 70

        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(50, y, "CHEMINFORMATICS VIRTUAL LAB")

        y -= 55

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Student Details")

        y -= 30

        pdf.setFont("Helvetica", 11)

        lines = [
            f"Name: {STUDENT_NAME}",
            f"Register Number: {REGISTER_NUMBER}",
            f"Institution: {INSTITUTION}",
            "",
            "Project: Cheminformatics Virtual Laboratory",
            "",
            "Project Features:",
            "- Periodic Table",
            "- Molecular Structure Visualization",
            "- Molecular Property Calculator",
            "- Chemistry Theory",
            "- Chemistry Quiz",
            "",
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
        ]

        for line in lines:
            pdf.drawString(50, y, line)
            y -= 22

        pdf.save()
        buffer.seek(0)

        st.download_button(
            "Download PDF Report",
            data=buffer,
            file_name="NEXCHEM_Student_Report.pdf",
            mime="application/pdf"
        )

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.markdown(
    f"""
    <div style="text-align:center;padding:15px;color:#9fb2cc;">
        <b style="color:#54f0d0;">NEXCHEM VIRTUAL LAB</b><br>
        {STUDENT_NAME} | {REGISTER_NUMBER}<br>
        {INSTITUTION}<br>
        <small>Built with Python, Streamlit and RDKit</small>
    </div>
    """,
    unsafe_allow_html=True
)
