import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="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")

st.title("Assistant CAF 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

option = st.radio("Menu", ["💬 Agent CAF", "🧮 Simulation"])

# =========================
# 💬 AGENT CAF
# =========================
if option == "💬 Agent CAF":

    st.subheader("Assistant CAF 🤖")

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**🧑 Toi :** {msg['content']}")
        else:
            st.markdown(f"**🤖 Assistant :** {msg['content']}")
            if st.button("🧮 Faire une simulation", key=f"btn_{msg['content']}"):
                st.session_state.page = "simulation"

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Écris ton message...")
        submit = st.form_submit_button("Envoyer")

    if submit and user_input:

        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
Tu es un conseiller CAF intelligent.

- Tu peux mentionner le site CAF
- MAIS tu proposes toujours le simulateur interne

Réponds :
- court
- clair
- utile

Si l'utilisateur parle d'aides :
👉 propose simulation ici
"""
                }
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.rerun()

# =========================
# 🧮 SIMULATION
# =========================
elif option == "🧮 Simulation":

    st.subheader("Simulation CAF")

    type_simulation = st.selectbox(
        "Choisis une aide",
        ["APL", "Prime d'activité", "RSA"]
    )

    # -------- APL --------
    if type_simulation == "APL":

        revenu = st.number_input("Revenus mensuels (€)", 0)
        loyer = st.number_input("Montant du loyer (€)", 0)
        code_postal = st.text_input("Code postal")
        situation = st.selectbox("Situation", ["Seul", "Couple"])
        enfants = st.selectbox("Nombre d'enfants", [0,1,2,3])
        logement = st.selectbox("Type de logement", ["Appartement", "Maison", "Colocation"])

        if st.button("Simuler APL"):

            prompt = f"""
Simulation APL réaliste

revenu={revenu}, loyer={loyer}, code_postal={code_postal},
situation={situation}, enfants={enfants}, logement={logement}

Réponds :
👉 Éligibilité
👉 Estimation
👉 Explication
👉 Démarches
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Expert APL réaliste"},
                    {"role":"user","content":prompt}
                ]
            )

            st.write(response.choices[0].message.content)

    # -------- PRIME ACTIVITÉ --------
    elif type_simulation == "Prime d'activité":

        revenu = st.number_input("Revenu mensuel (€)", 0)
        statut = st.selectbox(
            "Statut professionnel",
            ["Salarié", "Temps partiel", "Indépendant", "Chômage"]
        )
        heures = st.number_input("Heures travaillées / mois", 0)
        situation = st.selectbox("Situation familiale", ["Seul", "Couple"])
        enfants = st.selectbox("Nombre d'enfants", [0,1,2,3])

        if st.button("Simuler Prime"):

            prompt = f"""
Simulation prime activité réaliste

revenu={revenu}, statut={statut}, heures={heures},
situation={situation}, enfants={enfants}

Réponds :
👉 Éligibilité
👉 Estimation
👉 Explication
👉 Démarches
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Expert prime activité CAF"},
                    {"role":"user","content":prompt}
                ]
            )

            st.write(response.choices[0].message.content)

    # -------- RSA --------
    elif type_simulation == "RSA":

        revenu = st.number_input("Revenu mensuel (€)", 0)
        situation = st.selectbox("Situation", ["Seul", "Couple"])
        enfants = st.selectbox("Nombre d'enfants", [0,1,2,3])
        logement = st.selectbox("Logement", ["Locataire", "Gratuit", "Propriétaire"])

        if st.button("Simuler RSA"):

            prompt = f"""
Simulation RSA réaliste

revenu={revenu}, situation={situation},
enfants={enfants}, logement={logement}

Réponds :
👉 Éligibilité
👉 Estimation
👉 Explication
👉 Démarches
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Expert RSA CAF"},
                    {"role":"user","content":prompt}
                ]
            )

            st.write(response.choices[0].message.content)