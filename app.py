
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors
from rdkit.Chem import AllChem
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def image_to_bytes(image):
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def generate_student_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 70

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "NEXCHEM VIRTUAL LAB")

    y -= 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Student Information")

    y -= 30

    pdf.setFont("Helvetica", 11)

    lines = [
        "Name: R. JAYADHARAN",
        "Register Number: RA2611026050288",
        "Institution: SRM Institute of Science and Technology,",
        "Tiruchirappalli",
        "",
        "Project: Cheminformatics Virtual Laboratory",
        "",
        "Project Features:",
        "- Interactive Periodic Table",
        "- Molecular Structure Visualization",
        "- Molecular Property Calculator",
        "- Chemistry Theory",
        "- Chemistry Knowledge Quiz",
        "",
        "Generated: " + datetime.now().strftime("%d-%m-%Y %H:%M")
    ]

    for line in lines:
        pdf.drawString(50, y, line)
        y -= 22

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="NEXCHEM | Virtual Laboratory",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# STUDENT DETAILS
# ==================================================

STUDENT_NAME = "R. JAYADHARAN"
REGISTER_NUMBER = "RA2611026050288"
INSTITUTION = "SRM Institute of Science and Technology, Tiruchirappalli"


# ==================================================
# CUSTOM DESIGN
# ==================================================

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
    padding: 20px;
    text-align: center;
    margin: 10px 0;
}

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="hero">
    <h1>🧪 NEXCHEM VIRTUAL LAB</h1>
    <p>Explore Molecules. Discover Properties. Experience Chemistry.</p>
    <p>Interactive Cheminformatics Learning Platform</p>
    <span class="hero-tag">STUDENT PROJECT | SRM IST</span>
</div>
""", unsafe_allow_html=True)


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

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


# ==================================================
# DASHBOARD
# ==================================================

if page == "🏠 Dashboard":

    st.title("Welcome to NEXCHEM")

    st.write(
        "A digital chemistry laboratory for exploring "
        "chemical elements, molecular structures and properties."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Chemical Elements", "118")
    c2.metric("Molecular Tools", "3")
    c3.metric("Learning Modules", "4")

    st.divider()

    st.subheader("Explore Your Laboratory")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ⚛️ Periodic Table")
        st.write("Explore chemical elements and their properties.")

    with col2:
        st.markdown("### 🧬 Molecule Explorer")
        st.write("Generate and visualize molecular structures.")

    with col3:
        st.markdown("### 📊 Property Calculator")
        st.write("Calculate molecular descriptors.")

    st.info("Select a module from the navigation menu.")


# ==================================================
# PERIODIC TABLE
# ==================================================

elif page == "⚛️ Periodic Table":

    st.title("⚛️ Interactive Periodic Table")

    periodic_table = Chem.GetPeriodicTable()

    atomic_number = st.selectbox(
        "Select Atomic Number",
        list(range(1, 119))
    )

    symbol = periodic_table.GetElementSymbol(atomic_number)
    name = periodic_table.GetElementName(atomic_number)
    atomic_mass = periodic_table.GetAtomicWeight(atomic_number)

    st.markdown(
        f"""
        <div class="element-card">
            <h1 style="font-size:70px;color:#54f0d0;">{symbol}</h1>
            <h2>{name}</h2>
            <p>Atomic Number: {atomic_number}</p>
            <p>Atomic Mass: {atomic_mass:.3f} u</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    a.metric("Atomic Number", atomic_number)
    b.metric("Symbol", symbol)
    c.metric("Atomic Mass", f"{atomic_mass:.3f} u")

    st.caption("Element information provided by RDKit.")


# ==================================================
# MOLECULAR EXPLORER
# ==================================================

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
        "Choose Example Molecule",
        list(examples.keys())
    )

    smiles = st.text_input(
        "Enter SMILES Notation",
        value=examples[selected]
    )

    if st.button("Generate Molecular Structure"):

        mol = Chem.MolFromSmiles(smiles)

        if mol is None:

            st.error("Invalid SMILES notation. Try another structure.")

        else:

            st.success("Molecule generated successfully!")

            mol = Chem.AddHs(mol)

            AllChem.Compute2DCoords(mol)

            image = Draw.MolToImage(
                mol,
                size=(700, 500),
                legend="NEXCHEM Molecular Structure"
            )

            st.image(
                image,
                caption="2D Molecular Structure",
                use_container_width=True
            )

            st.subheader("Molecular Information")

            st.write("SMILES:", Chem.MolToSmiles(mol))
            st.write("Total Atoms:", mol.GetNumAtoms())
            st.write("Total Bonds:", mol.GetNumBonds())

            st.download_button(
                "⬇️ Download Molecular Image",
                data=image_to_bytes(image),
                file_name="molecule.png",
                mime="image/png"
            )


# ==================================================
# MOLECULAR PROPERTIES
# ==================================================

elif page == "📊 Molecular Properties":

    st.title("📊 Molecular Property Calculator")

    smiles = st.text_input(
        "Enter SMILES Notation",
        value="CCO"
    )

    if st.button("Calculate Molecular Properties"):

        mol = Chem.MolFromSmiles(smiles)

        if mol is None:

            st.error("Invalid molecular structure.")

        else:

            data = {
                "Molecular Formula": rdMolDescriptors.CalcMolFormula(mol),
                "Molecular Weight": Descriptors.MolWt(mol),
                "LogP": Descriptors.MolLogP(mol),
                "TPSA": Descriptors.TPSA(mol),
                "H-Bond Donors": Descriptors.NumHDonors(mol),
                "H-Bond Acceptors": Descriptors.NumHAcceptors(mol),
                "Rotatable Bonds": Descriptors.NumRotatableBonds(mol),
                "Heavy Atoms": Descriptors.HeavyAtomCount(mol)
            }

            st.success("Properties calculated successfully!")

            col1, col2 = st.columns(2)

            col1.metric(
                "Molecular Weight",
                f"{data['Molecular Weight']:.2f} g/mol"
            )

            col2.metric(
                "LogP",
                f"{data['LogP']:.2f}"
            )

            st.subheader("Complete Property Table")

            df = pd.DataFrame(
                list(data.items()),
                columns=["Property", "Value"]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            numeric_data = {
                key: value
                for key, value in data.items()
                if isinstance(value, (int, float))
            }

            fig, ax = plt.subplots(figsize=(9, 4))

            ax.bar(
                numeric_data.keys(),
                numeric_data.values()
            )

            ax.set_title("Molecular Descriptor Overview")
            ax.set_ylabel("Calculated Value")
            ax.tick_params(axis="x", rotation=35)

            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download Properties CSV",
                data=csv,
                file_name="molecular_properties.csv",
                mime="text/csv"
            )


# ==================================================
# CHEMISTRY THEORY
# ==================================================

elif page == "🔬 Chemistry Theory":

    st.title("🔬 Chemistry Learning Centre")

    topics = {

        "Quantum Mechanics": """
        Quantum mechanics describes the behaviour of matter
        at atomic and subatomic scales.

        Important Concepts:
        - Wave-particle duality
        - Quantization of energy
        - Probability interpretation
        - Schrödinger wave equation
        """,

        "Schrödinger Equation": """
        The time-independent Schrödinger equation is:

        Hψ = Eψ

        Where:

        H = Hamiltonian operator
        ψ = Wave function
        E = Energy eigenvalue
        """,

        "Molecular Orbital Theory": """
        Molecular orbital theory explains chemical bonding
        by combining atomic orbitals to form molecular orbitals.

        Main Types:
        - Bonding orbitals
        - Antibonding orbitals
        """,

        "Chemical Bonding": """
        Chemical bonding explains how atoms combine to form molecules.

        Main Types:
        - Ionic bonding
        - Covalent bonding
        - Metallic bonding
        - Hydrogen bonding
        """,

        "Thermodynamics": """
        Thermodynamics studies energy, heat and work.

        Important Quantities:
        - Internal energy
        - Enthalpy
        - Entropy
        - Gibbs free energy
        """
    }

    topic = st.selectbox(
        "Select a Chemistry Topic",
        list(topics.keys())
    )

    st.subheader(topic)
    st.write(topics[topic])


# ==================================================
# CHEMISTRY QUIZ
# ==================================================

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
            "question": "Who developed the wave equation?",
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

            st.markdown(
                f"**Q{i + 1}. {q['question']}**"
            )

            answer = st.radio(
                "Select your answer",
                q["options"],
                key=f"quiz_{i}"
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
            f"Your Score: {score}/{len(questions)}"
        )

        st.progress(score / len(questions))

        for i, q in enumerate(questions):

            if answers[i] == q["answer"]:
                st.write(f"Question {i + 1}: Correct!")

            else:
                st.write(
                    f"Question {i + 1}: Correct answer is "
                    f"{q['answer']}"
                )


# ==================================================
# STUDENT REPORT
# ==================================================

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

    Main Features:

    - Interactive periodic table
    - Molecular structure visualization
    - Molecular property calculations
    - Chemistry theory modules
    - Knowledge assessment quiz
    - Student PDF report
    """)

    if st.button("Generate Student PDF Report"):

        pdf_data = generate_student_pdf()

        st.download_button(
            "⬇️ Download Student Report",
            data=pdf_data,
            file_name="NEXCHEM_Student_Report.pdf",
            mime="application/pdf"
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    f"""
    <div style="
        text-align:center;
        padding:20px;
        color:#9fb2cc;
    ">
        <h3 style="color:#54f0d0;">NEXCHEM VIRTUAL LAB</h3>
        {STUDENT_NAME}<br>
        {REGISTER_NUMBER}<br>
        {INSTITUTION}<br>
        <small>Built using Python, Streamlit and RDKit</small>
    </div>
    """,
    unsafe_allow_html=True
)
