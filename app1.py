import streamlit as st
from openai import OpenAI
import time

# ─────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Assistant CAF",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CSS PERSONNALISÉ – UX MODERNE
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 60%, #f5f0ff 100%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1f3a 0%, #2d3561 100%);
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #e8ecff !important;
}
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 4px 0;
    display: block;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.95rem;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.15);
}

/* ── Titre sidebar ── */
.sidebar-logo {
    text-align: center;
    padding: 1.5rem 0 2rem;
}
.sidebar-logo h1 {
    font-size: 1.5rem !important;
    font-weight: 700;
    color: #ffffff !important;
    margin: 0;
}
.sidebar-logo p {
    font-size: 0.75rem;
    color: #a0aacc !important;
    margin: 4px 0 0;
}

/* ── Badge statut ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(34, 197, 94, 0.15);
    color: #22c55e !important;
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

/* ── Bulles de chat ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 1rem 0;
    max-height: 62vh;
    overflow-y: auto;
}

.msg-user {
    display: flex;
    justify-content: flex-end;
}
.msg-user .bubble {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.55;
    box-shadow: 0 4px 15px rgba(79,70,229,0.25);
}

.msg-bot {
    display: flex;
    justify-content: flex-start;
    gap: 10px;
    align-items: flex-end;
}
.bot-avatar {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, #1a1f3a, #4f46e5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.msg-bot .bubble {
    background: white;
    color: #1e2040;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.55;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border: 1px solid rgba(0,0,0,0.06);
}

/* ── Typing indicator ── */
.typing-indicator {
    display: flex;
    gap: 5px;
    padding: 14px 18px;
    background: white;
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.typing-dot {
    width: 8px;
    height: 8px;
    background: #9ca3af;
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-8px); }
}

/* ── Input zone ── */
.stTextInput input {
    border-radius: 25px !important;
    border: 2px solid #e5e7eb !important;
    padding: 12px 20px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.93rem !important;
    transition: border-color 0.2s !important;
    background: white !important;
}
.stTextInput input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 4px rgba(79,70,229,0.1) !important;
}

/* ── Boutons ── */
.stButton > button {
    border-radius: 25px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(79,70,229,0.3) !important;
}

/* ── Cards simulation ── */
.sim-card {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    border: 1px solid rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}

/* ── Résultat simulation ── */
.result-card {
    background: linear-gradient(135deg, #f0f4ff, #f5f0ff);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    border: 1px solid rgba(79,70,229,0.15);
    margin-top: 1rem;
}

/* ── Titres de page ── */
.page-header {
    margin-bottom: 1.5rem;
}
.page-header h2 {
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1f3a;
    margin: 0 0 4px;
}
.page-header p {
    color: #6b7280;
    font-size: 0.9rem;
    margin: 0;
}

/* ── Chips aide rapide ── */
.quick-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1rem;
}
.chip {
    background: white;
    border: 1.5px solid #e5e7eb;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.82rem;
    color: #4f46e5;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}
.chip:hover {
    background: #4f46e5;
    color: white;
    border-color: #4f46e5;
}

/* ── Selectbox / number input ── */
.stSelectbox > div, .stNumberInput > div {
    border-radius: 12px !important;
}

/* ── Séparateur ── */
hr { border-color: rgba(0,0,0,0.06) !important; }

/* ── Cacher hamburger menu ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# CLIENT OPENAI
# ─────────────────────────────────────────


# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_input" not in st.session_state:
    st.session_state.quick_input = ""

# ─────────────────────────────────────────
# SYSTEM PROMPT CAF COMPLET
# ─────────────────────────────────────────
SYSTEM_PROMPT = """
Tu es CAFI, un conseiller CAF (Caisse d'Allocations Familiales) français expert et bienveillant.
Tu connais PARFAITEMENT toutes les aides et prestations CAF.

═══════════════════════════════════════════
📋 AIDES QUE TU MAÎTRISES TOTALEMENT
═══════════════════════════════════════════

🏠 AIDES AU LOGEMENT :
- APL (Aide Personnalisée au Logement) : pour locataires, résidence principale, calculée selon revenus N-2, loyer, zone géographique, composition foyer
- ALS (Allocation de Logement Sociale) : pour ceux non éligibles APL
- ALF (Allocation de Logement Familiale) : pour familles avec enfants ou femme enceinte
- Critères : être locataire ou en FJT/résidence étudiante, logement décent, revenus sous plafond

💰 MINIMA SOCIAUX :
- RSA (Revenu de Solidarité Active) : 635,71€/mois pour une personne seule (2024), majoré si enfants, versé sous conditions de ressources et de résidence
- RSA socle : pour sans revenus. RSA activité fusionné dans prime d'activité
- Conditions RSA : +25 ans (ou +18 ans avec enfant), résider en France, ressources sous plafond

💼 AIDES À L'ACTIVITÉ :
- Prime d'activité : complément de revenus pour travailleurs modestes, calculée trimestriellement, déclaration trimestrielle obligatoire
- Montant moyen : ~170€/mois mais varie selon revenus, situation familiale
- Éligible : salarié, indépendant, apprenti avec revenus mensuels entre ~600€ et ~1 800€ (seul)

👶 PRESTATIONS FAMILIALES :
- Allocations familiales : à partir du 2e enfant, 141,55€/mois pour 2 enfants, +181,56€ par enfant supplémentaire (2024)
- Complément familial : pour familles 3+ enfants de 3 à 21 ans, sous conditions ressources
- PAJE (Prestation d'Accueil du Jeune Enfant) : prime naissance (1 017€), allocation de base (184,62€/mois), CMG (Complément Mode de Garde)
- CLCA/PrePare : complément libre choix d'activité
- AEEH (Allocation Enfant Handicapé) : 141,79€/mois de base + compléments selon handicap
- Bourse lycée/collège : selon revenus

🏥 SANTÉ & HANDICAP :
- CSS (Complémentaire Santé Solidaire) : ancienne CMU-C, gratuite ou quasi-gratuite selon revenus
- AAH (Allocation Adulte Handicapé) : 971,37€/mois (2024), conditions : taux incapacité ≥80%, ou 50-80% + restriction emploi, sous conditions ressources
- PCH (Prestation Compensation Handicap) : gérée par Conseil Départemental

🎓 AIDES ÉTUDIANT :
- ALS pour étudiants : si non logé chez parents
- APL en résidence universitaire
- Aide à la mobilité (Visale, garantie Visale)

📅 DÉMARCHES & INFOS PRATIQUES :
- Espace Mon Compte CAF : caf.fr
- Déclaration trimestrielle de ressources : obligatoire pour RSA et Prime d'activité
- Délai de traitement : généralement 2 à 4 semaines
- Rétroactivité APL : possible sur 2 ans si droits non ouverts
- Trop-perçu : remboursement possible par mensualités

═══════════════════════════════════════════
🎯 TON COMPORTEMENT
═══════════════════════════════════════════

STYLE :
- Réponds toujours en français, de façon chaleureuse et accessible
- Sois précis et concret, donne des montants réels quand tu peux
- Réponds court (3-5 phrases max sauf si on te demande des détails)
- Utilise des émojis pertinents pour aérer
- Si tu ne sais pas exactement, dis-le et oriente vers caf.fr ou 3230

GUIDE L'UTILISATEUR :
- Pose des questions ciblées pour mieux cerner sa situation
- Propose des pistes d'aides auxquelles il n'aurait pas pensé
- Signale si une aide est cumulable avec une autre
- Mentionne les pièces justificatives souvent demandées

NEVER :
- N'invente pas de montants si tu n'es pas sûr
- Ne donne pas de conseils juridiques ou fiscaux complexes
- Ne prends pas de décisions à la place de la CAF

Si l'utilisateur est en difficulté financière grave → mentionne aussi les Banques Alimentaires, CCAS, assistante sociale.
"""

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h1>🏠 CAF Assistant</h1>
        <p>Votre conseiller allocations</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="status-badge">🟢 En ligne</div>', unsafe_allow_html=True)

    st.markdown("**Navigation**")
    page = st.radio(
        "",
        ["💬 Conseiller IA", "🧮 Simulateur d'aides", "ℹ️ Infos utiles"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**💡 Aides disponibles**")
    aides = ["🏠 APL / ALS / ALF", "💰 RSA", "💼 Prime d'activité",
             "👶 Allocations familiales", "🎓 Aides étudiants", "♿ AAH / AEEH"]
    for a in aides:
        st.markdown(f"<small style='color:#a0aacc'>• {a}</small>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<small style='color:#6b7a99'>📞 3230 – Numéro CAF<br>🌐 caf.fr</small>", unsafe_allow_html=True)

    # Bouton reset chat
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────
# PAGE : CONSEILLER IA
# ─────────────────────────────────────────
if page == "💬 Conseiller IA":

    st.markdown("""
    <div class="page-header">
        <h2>💬 Conseiller CAF intelligent</h2>
        <p>Posez n'importe quelle question sur vos droits et aides CAF</p>
    </div>
    """, unsafe_allow_html=True)

    # Questions rapides (chips cliquables)
    st.markdown("**Questions fréquentes :**")
    cols = st.columns(4)
    quick_questions = [
        ("🏠 Ai-je droit à l'APL ?", cols[0]),
        ("💰 Montant RSA 2024 ?", cols[1]),
        ("💼 Prime d'activité ?", cols[2]),
        ("👶 Aides bébé ?", cols[3]),
    ]
    for question, col in quick_questions:
        with col:
            if st.button(question, use_container_width=True):
                st.session_state.quick_input = question.split(" ", 1)[1]
                st.rerun()

    st.markdown("---")

    # Affichage des messages
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding: 2rem; color: #9ca3af;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <p style="font-size:1rem; font-weight:600; color:#4f46e5;">Bonjour ! Je suis CAFI, votre conseiller CAF.</p>
            <p style="font-size:0.88rem;">Posez-moi n'importe quelle question sur vos allocations, aides au logement, RSA, prime d'activité...</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Rendu des bulles
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="msg-user">
                    <div class="bubble">{msg['content']}</div>
                </div>"""
            else:
                content = msg['content'].replace('\n', '<br>')
                chat_html += f"""
                <div class="msg-bot">
                    <div class="bot-avatar">🤖</div>
                    <div class="bubble">{content}</div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

    # Zone de saisie
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        default_val = st.session_state.quick_input
        user_input = st.text_input(
            "",
            value=default_val,
            placeholder="Ex: J'ai 2 enfants et un loyer de 700€, ai-je droit à l'APL ?",
            label_visibility="collapsed",
            key="chat_input"
        )
    with col_btn:
        send = st.button("Envoyer ➤", use_container_width=True, type="primary")

    # Reset quick input
    if st.session_state.quick_input:
        st.session_state.quick_input = ""

    # Traitement
    if send and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})

        with st.spinner("CAFI réfléchit..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
                temperature=0.7,
                max_tokens=600,
            )
            reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ─────────────────────────────────────────
# PAGE : SIMULATEUR
# ─────────────────────────────────────────
elif page == "🧮 Simulateur d'aides":

    st.markdown("""
    <div class="page-header">
        <h2>🧮 Simulateur d'aides CAF</h2>
        <p>Estimez vos droits en quelques secondes</p>
    </div>
    """, unsafe_allow_html=True)

    type_sim = st.selectbox(
        "Quelle aide souhaitez-vous simuler ?",
        ["🏠 APL – Aide au Logement", "💼 Prime d'activité", "💰 RSA"]
    )

    st.markdown('<div class="sim-card">', unsafe_allow_html=True)

    # ── APL ──
    if "APL" in type_sim:
        st.markdown("#### 🏠 Simulation APL")
        col1, col2 = st.columns(2)
        with col1:
            revenu = st.number_input("Revenus mensuels nets (€)", min_value=0, value=0, step=50)
            loyer = st.number_input("Montant du loyer charges comprises (€)", min_value=0, value=0, step=10)
            code_postal = st.text_input("Code postal du logement")
        with col2:
            situation = st.selectbox("Situation familiale", ["Célibataire", "Couple", "Famille monoparentale"])
            enfants = st.selectbox("Nombre d'enfants à charge", [0, 1, 2, 3, 4, "5+"])
            logement = st.selectbox("Type de logement", ["Appartement", "Maison", "Résidence étudiante / FJT", "Colocation"])

        if st.button("✨ Calculer mon APL estimée", type="primary", use_container_width=True):
            prompt = f"""
Tu es un simulateur APL précis.
Données saisies : revenus={revenu}€/mois, loyer={loyer}€/mois, code_postal={code_postal}, situation={situation}, enfants={enfants}, logement={logement}

Réponds EXACTEMENT dans ce format :

📊 ÉLIGIBILITÉ : ✅ Éligible / ⚠️ Probablement éligible / ❌ Non éligible

💶 MONTANT ESTIMÉ : XX à XX € / mois

📝 POURQUOI : (2 phrases précises sur le calcul)

✅ POUR EN BÉNÉFICIER :
1. Se connecter sur caf.fr > Faire une demande d'APL
2. Fournir : justificatif de loyer, avis d'imposition, contrat de bail
3. Délai de traitement : 2 à 4 semaines

⚠️ POINT D'ATTENTION : (1 info utile ou mise en garde)

Sois réaliste et précis dans les montants.
"""
            with st.spinner("Calcul en cours..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Expert CAF, simulateur APL précis et réaliste. Donne des montants vraisemblables basés sur les barèmes 2024."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                )
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── PRIME D'ACTIVITÉ ──
    elif "Prime" in type_sim:
        st.markdown("#### 💼 Simulation Prime d'activité")
        col1, col2 = st.columns(2)
        with col1:
            revenu = st.number_input("Revenu mensuel net (€)", min_value=0, value=0, step=50)
            statut = st.selectbox("Statut professionnel", ["Salarié (CDI/CDD)", "Temps partiel", "Indépendant / Auto-entrepreneur", "Apprenti", "En recherche d'emploi"])
            heures = st.number_input("Heures travaillées / mois (si applicable)", min_value=0, value=0, step=5)
        with col2:
            situation = st.selectbox("Situation familiale", ["Célibataire", "Couple (un seul revenu)", "Couple (deux revenus)", "Parent isolé"])
            enfants = st.selectbox("Nombre d'enfants à charge", [0, 1, 2, 3, "4+"])
            loyer_pa = st.number_input("Loyer mensuel (€) – optionnel", min_value=0, value=0, step=10)

        if st.button("✨ Calculer ma Prime d'activité estimée", type="primary", use_container_width=True):
            prompt = f"""
Tu es un simulateur Prime d'activité précis (barèmes 2024).
Données : revenu={revenu}€, statut={statut}, heures={heures}h/mois, situation={situation}, enfants={enfants}, loyer={loyer_pa}€

Format STRICT :

📊 ÉLIGIBILITÉ : ✅ Éligible / ⚠️ Probablement éligible / ❌ Non éligible

💶 MONTANT ESTIMÉ : XX € / mois

📝 CALCUL SIMPLIFIÉ : (formule ou raisonnement en 2 phrases)

✅ DÉMARCHES :
1. ...
2. ...
3. Renouveler la déclaration trimestrielle sur caf.fr

⚠️ À SAVOIR : (1 point clé : ex délai, cumul possible, etc.)
"""
            with st.spinner("Calcul en cours..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Expert CAF simulateur Prime d'activité 2024."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                )
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── RSA ──
    elif "RSA" in type_sim:
        st.markdown("#### 💰 Simulation RSA")
        col1, col2 = st.columns(2)
        with col1:
            revenu = st.number_input("Revenus mensuels (€) – 0 si sans ressources", min_value=0, value=0, step=50)
            age = st.number_input("Votre âge", min_value=18, max_value=99, value=30)
            situation = st.selectbox("Situation familiale", ["Célibataire", "Couple", "Parent isolé (monoparent)"])
        with col2:
            enfants = st.selectbox("Nombre d'enfants à charge", [0, 1, 2, 3, "4+"])
            logement = st.selectbox("Situation logement", ["Locataire", "Hébergé gratuitement", "Propriétaire", "Sans domicile fixe"])
            nationalite = st.selectbox("Nationalité / titre de séjour", ["Française", "UE/EEE", "Extra-UE (titre séjour valide +5 ans)", "Autre"])

        if st.button("✨ Calculer mon RSA estimé", type="primary", use_container_width=True):
            prompt = f"""
Tu es un simulateur RSA précis (barèmes 2024).
Données : revenu={revenu}€, age={age}, situation={situation}, enfants={enfants}, logement={logement}, nationalité={nationalite}

Format STRICT :

📊 ÉLIGIBILITÉ : ✅ Éligible / ⚠️ Conditions à vérifier / ❌ Non éligible (avec raison)

💶 MONTANT ESTIMÉ RSA : XX € / mois (RSA socle = 635,71€ pour célibataire sans revenus en 2024)

📝 EXPLICATION : (comment on arrive à ce montant, en 2 phrases)

✅ DÉMARCHES :
1. Faire la demande sur caf.fr ou à la mairie
2. Pièces : CNI, justificatif domicile, RIB, avis d'imposition
3. Délai : 2 mois maximum légalement

⚠️ IMPORTANT : (droits et devoirs RSA, ex. inscription Pôle Emploi / France Travail)
"""
            with st.spinner("Calcul en cours..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Expert RSA France 2024, simulateur précis et bienveillant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                )
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(response.choices[0].message.content)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Bouton retour chat
    st.markdown("---")
    st.markdown("💬 *Une question sur votre résultat ?*")
    if st.button("→ Poser une question au conseiller IA"):
        # On ne peut pas changer la sidebar radio directement, on informe juste
        st.info("Utilisez le menu **💬 Conseiller IA** dans la barre latérale pour poser vos questions !")

# ─────────────────────────────────────────
# PAGE : INFOS UTILES
# ─────────────────────────────────────────
elif page == "ℹ️ Infos utiles":

    st.markdown("""
    <div class="page-header">
        <h2>ℹ️ Infos & Contacts utiles</h2>
        <p>Tout ce qu'il faut savoir pour contacter la CAF</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📞 Contacts CAF
        - **Téléphone :** 3230 (lun-ven 9h-17h)
        - **Site :** [caf.fr](https://www.caf.fr)
        - **Mon Compte CAF :** [cafconnect.caf.fr](https://www.caf.fr)
        - **Appli :** Mon Compte CAF (iOS & Android)

        ### 📄 Documents souvent demandés
        - Pièce d'identité
        - Justificatif de domicile
        - RIB
        - Avis d'imposition (N-2)
        - Contrat de bail / quittances de loyer
        - Bulletins de salaire (3 derniers)
        """)

    with col2:
        st.markdown("""
        ### ⏱️ Délais moyens
        | Aide | Délai traitement |
        |------|-----------------|
        | APL | 2 à 4 semaines |
        | RSA | 4 à 8 semaines |
        | Prime d'activité | 2 à 3 semaines |
        | Allocations fam. | 2 à 4 semaines |

        ### 🔄 Déclarations obligatoires
        - **RSA & Prime d'activité :** déclaration trimestrielle de ressources
        - **APL :** signaler tout changement (loyer, revenus, composition foyer)
        - **Toute aide :** signaler déménagement, naissance, changement situation
        """)

    st.markdown("---")
    st.info("💡 En cas de difficultés graves, vous pouvez aussi contacter votre **CCAS** (Centre Communal d'Action Sociale) ou une **assistante sociale** via votre mairie.")
