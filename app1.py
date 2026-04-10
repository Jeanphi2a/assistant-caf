import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Assistant CAF 🤖")

# mémoire
if "messages" not in st.session_state:
    st.session_state.messages = []

if "menu" not in st.session_state:
    st.session_state.menu = "💬 Agent CAF"

menu = st.radio(
    "Menu",
    ["💬 Agent CAF", "🧮 Simulation"],
    index=0 if st.session_state.menu == "💬 Agent CAF" else 1
)

st.session_state.menu = menu

# =========================
# 💬 CHAT
# =========================
if menu == "💬 Agent CAF":

    st.subheader("Assistant CAF 🤖")

    for msg in st.session_state.messages:
        role = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f"**{role} :** {msg['content']}")

    if st.button("🧮 Faire une simulation"):
        st.session_state.menu = "🧮 Simulation"
        st.rerun()

    user_input = st.text_input("Pose ta question")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un conseiller CAF clair et utile."}
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.rerun()

# =========================
# 🧮 SIMULATION
# =========================
elif menu == "🧮 Simulation":

    st.subheader("Simulation CAF")

    type_simulation = st.selectbox(
        "Choisis une aide",
        ["APL", "Prime d'activité", "RSA"]
    )

    # -------- APL --------
    if type_simulation == "APL":

        revenu = st.number_input("Revenu mensuel (€)", 0)
        loyer = st.number_input("Loyer (€)", 0)
        personnes = st.selectbox("Personnes dans le foyer", [1,2,3,4])
        zone = st.selectbox("Zone", ["Zone 1", "Zone 2", "Zone 3"])

        if st.button("Simuler APL"):

            # 🔥 plafonds réalistes
            plafonds = {"Zone 1": 500, "Zone 2": 450, "Zone 3": 400}
            plafond = plafonds[zone]

            loyer_retenu = min(loyer, plafond)

            # 💥 calcul dynamique (beaucoup plus fort)
            apl = loyer_retenu * 0.7
            apl -= revenu * 0.35   # IMPACT FORT
            apl += personnes * 120

            if revenu < 900:
                apl += 150

            apl = max(apl, 0)
            apl = int(apl)

            st.write(f"### 💰 Estimation APL : {apl} € / mois")

            # 🤖 IA
            prompt = f"""
Analyse cette situation CAF :

revenu={revenu}
loyer={loyer}
personnes={personnes}
zone={zone}
apl={apl}

Explique :
- pourquoi ce montant
- si c'est faible ou élevé
- donne 2 conseils utiles

Réponse courte.
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Conseiller CAF"},
                    {"role":"user","content":prompt}
                ]
            )

            st.write(response.choices[0].message.content)

    # -------- PRIME ACTIVITÉ --------
    elif type_simulation == "Prime d'activité":

        revenu = st.number_input("Revenu (€)", 0)
        statut = st.selectbox("Statut", ["Salarié", "Indépendant", "Chômage"])
        personnes = st.selectbox("Personnes", [1,2,3])

        if st.button("Simuler Prime"):

            if statut == "Chômage":
                estimation = 0
            else:
                base = 300
                estimation = base + (personnes * 80) - (revenu * 0.25)

            estimation = max(estimation, 0)
            estimation = int(estimation)

            st.write(f"### 💰 Estimation : {estimation} € / mois")

    # -------- RSA --------
    elif type_simulation == "RSA":

        age = st.number_input("Âge", 18)
        revenu = st.number_input("Revenu (€)", 0)
        statut = st.selectbox("Statut", ["Sans emploi", "Salarié"])
        situation = st.selectbox("Situation", ["Seul", "Couple"])

        if st.button("Simuler RSA"):

            if age < 25 and statut == "Salarié":
                estimation = 0
            else:
                base = 607 if situation == "Seul" else 911
                estimation = base - (revenu * 0.4)

            estimation = max(estimation, 0)
            estimation = int(estimation)

            st.write(f"### 💰 Estimation : {estimation} € / mois")
