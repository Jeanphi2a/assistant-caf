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

            plafonds = {"Zone 1": 450, "Zone 2": 400, "Zone 3": 350}
            plafond_loyer = plafonds[zone]

            loyer_retenu = min(loyer, plafond_loyer)

            apl = (loyer_retenu * 0.75)
            apl -= (revenu * 0.25)
            apl += (personnes - 1) * 80

            if revenu < 1000:
                apl += 100

            apl = max(apl, 0)
            apl = int(apl)

            st.write(f"### 💰 Estimation APL : {apl} € / mois")

    # -------- PRIME ACTIVITÉ --------
    elif type_simulation == "Prime d'activité":

        revenu = st.number_input("Revenu (€)", 0)
        statut = st.selectbox("Statut", ["Salarié", "Indépendant", "Chômage"])
        personnes = st.selectbox("Personnes", [1,2,3])

        if st.button("Simuler Prime"):

            if statut == "Chômage":
                estimation = 0
            else:
                base = 250
                bonus = personnes * 70
                reduction = revenu * 0.2

                estimation = base + bonus - reduction

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
                base = 600 if situation == "Seul" else 900

                if statut == "Salarié":
                    base -= revenu * 0.3

                estimation = max(base, 0)

            estimation = int(estimation)

            st.write(f"### 💰 Estimation : {estimation} € / mois")
