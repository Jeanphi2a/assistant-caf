import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Assistant CAF 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "chat"

menu = st.radio("Menu", ["💬 Agent CAF", "🧮 Simulation"])

# =========================
# 💬 CHAT
# =========================
if menu == "💬 Agent CAF":

    st.subheader("Assistant CAF 🤖")

    for msg in st.session_state.messages:
        role = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f"**{role} :** {msg['content']}")

    if st.button("🧮 Aller au simulateur"):
        st.session_state.page = "simulation"
        st.experimental_rerun()

    user_input = st.text_input("Pose ta question")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": "Tu es un conseiller CAF clair et utile."
            }] + st.session_state.messages
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.experimental_rerun()

# =========================
# 🧮 SIMULATION
# =========================
if menu == "🧮 Simulation" or st.session_state.page == "simulation":

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

        if st.button("Simuler APL"):

            # 💥 LOGIQUE SIMPLE
            base = 300
            if revenu > 1500:
                base -= 100
            if loyer > 500:
                base += 50
            if personnes > 1:
                base += 50

            estimation = max(base, 0)

            st.write(f"### 💰 Estimation : {estimation} € / mois")

            # IA en complément
            prompt = f"""
Explique ce résultat APL simplement.

revenu={revenu}, loyer={loyer}, personnes={personnes}
montant={estimation}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Expert CAF"},
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

            estimation = 0
            if revenu < 1500 and statut != "Chômage":
                estimation = 150 + (personnes * 50)

            st.write(f"### 💰 Estimation : {estimation} € / mois")

            prompt = f"Explique ce résultat de prime activité : {estimation}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Expert CAF"},
                    {"role":"user","content":prompt}
                ]
            )

            st.write(response.choices[0].message.content)

    # -------- RSA --------
    elif type_simulation == "RSA":

        age = st.number_input("Âge", 18)
        revenu = st.number_input("Revenu (€)", 0)
        situation = st.selectbox("Situation", ["Seul", "Couple"])

        if st.button("Simuler RSA"):

            if age < 25:
                estimation = 0
            else:
                estimation = 600 if situation == "Seul" else 900

            if revenu > 500:
                estimation -= 200

            estimation = max(estimation, 0)

            st.write(f"### 💰 Estimation : {estimation} € / mois")

            prompt = f"Explique ce RSA : {estimation}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"Expert RSA"},
                    {"role":"user","content":prompt}
                ]
            )

            st.write(response.choices[0].message.content)
