import streamlit as st

st.set_page_config(
    page_title="Python Academy — Mission Air Liquide",
    page_icon="🎯",
    layout="wide"
)

if "progression" not in st.session_state:
    st.session_state.progression = {
        "S1": {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False},
        "S2": {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False},
        "S3": {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False},
        "S4": {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False},
        "S5": {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False},
        "S6": {"J1": False, "J2": False, "J3": False, "J4": False, "J5": False},
    }

total = 30
done = sum(1 for s in st.session_state.progression.values() for j in s.values() if j)

st.title("Python Academy — Mission Akeneo Air Liquide")
st.caption("James Alassane · 6 semaines · 1h/jour · Opérationnel le 15 juillet")

pct = round(done / total * 100)
st.progress(pct / 100)
col1, col2, col3 = st.columns(3)
col1.metric("Jours complétés", f"{done} / {total}")
col2.metric("Progression", f"{pct}%")
col3.metric("Jours restants", f"{total - done}")

st.divider()

semaines = {
    "S1": "Semaine 1 — Variables, types, boucles, fonctions, pandas",
    "S2": "Semaine 2 — Nettoyage, merge, comparaison CSV",
    "S3": "Semaine 3 — JSON & structures imbriquées",
    "S4": "Semaine 4 — API REST & Akeneo",
    "S5": "Semaine 5 — Script de migration complet",
    "S6": "Semaine 6 — Consolidation & simulation mission",
}

semaine_choisie = st.selectbox(
    "Choisir une semaine",
    options=list(semaines.keys()),
    format_func=lambda x: semaines[x]
)

st.subheader(semaines[semaine_choisie])
st.divider()

if semaine_choisie == "S1":
    jours = {
        "J1": "Lundi — Variables & types",
        "J2": "Mardi — Boucles & conditions",
        "J3": "Mercredi — Fonctions",
        "J4": "Jeudi — pandas bases",
        "J5": "Vendredi — Filtrer, trier & exporter",
    }
    jour_choisi = st.radio("Choisir un jour", options=list(jours.keys()),
                           format_func=lambda x: jours[x], horizontal=True)

    if jour_choisi == "J1":
        st.markdown("### Définitions à connaître")

        with st.expander("str — chaîne de texte"):
            st.write("Tout ce qui est entre guillemets. Utilisé pour les codes, labels, descriptions produits.")
            st.code('sku = "FLUKE-117"\nmarque = "Fluke"', language="python")

        with st.expander("int — nombre entier"):
            st.write("Un nombre sans virgule. Utilisé pour les stocks, les statuts.")
            st.code("stock = 12\nenabled = 1", language="python")

        with st.expander("float — nombre décimal"):
            st.write("Un nombre avec virgule. Utilisé pour les prix, les poids.")
            st.code("poids = 0.3\nprix = 249.90", language="python")

        with st.expander("list — liste ordonnée"):
            st.write("Une suite de valeurs entre crochets. L'index commence à 0.")
            st.code('skus = ["FLUKE-117", "FLUKE-175", "TESTO-865"]\nprint(skus[0])  # FLUKE-117\nprint(len(skus))  # 3', language="python")

        with st.expander("dict — dictionnaire clé:valeur"):
            st.write("Un objet avec des paires clé:valeur. C'est exactement la structure d'un produit Akeneo en JSON.")
            st.code('produit = {\n    "sku": "FLUKE-117",\n    "family": "multimetre",\n    "marque": "Fluke",\n    "enabled": 1,\n    "poids": 0.3\n}\nprint(produit["marque"])  # Fluke', language="python")

        st.divider()
        st.success("Quand l'API Akeneo retourne un produit c'est un dictionnaire. Quand elle retourne plusieurs produits c'est une liste de dictionnaires.")

        st.divider()
        st.markdown("### Code de référence — à taper à la main dans Jupyter")
        st.code('''# str, int, float
sku = "FLUKE-117"
stock = 12
poids = 0.3

# list
skus = ["FLUKE-117", "FLUKE-175", "TESTO-865"]
print(skus[0])    # FLUKE-117
print(len(skus))  # 3

# dict — un produit Akeneo
produit = {
    "sku": "FLUKE-117",
    "family": "multimetre",
    "marque": "Fluke",
    "enabled": 1,
    "poids": 0.3
}
print(produit["marque"])  # Fluke

# list de dicts — un catalogue
catalogue = [
    {"sku": "FLUKE-117", "family": "multimetre", "enabled": 1},
    {"sku": "TESTO-865", "family": "camera_thermique", "enabled": 0},
]''', language="python")

        st.warning("Règle d'or : tape ce code à la main dans Jupyter. Ne copie jamais.")

        st.divider()
        st.markdown("### Exercices")

        with st.expander("Exercice 1 — Créer les variables d'un produit Testoon (10 min)"):
            st.write("Crée les variables pour le RIGOL-DS1054Z : SKU, famille, marque, plage de mesure, poids, enabled. Affiche chaque variable et son type avec type().")
            st.info("Indice : str pour les textes, int pour le statut, float pour le poids.")
            code1 = st.text_area("Colle ton code ici après l'avoir tapé dans Jupyter :", key="e1j1", height=150)
            if st.button("Soumettre exercice 1"):
                if code1:
                    st.success("Bien ! Vérifie que chaque print(type(...)) affiche le bon type.")
                else:
                    st.error("Tape d'abord ton code dans Jupyter, puis colle-le ici.")

        with st.expander("Exercice 2 — Créer une liste de SKUs (15 min)"):
            st.write("Crée une liste avec les 5 SKUs Testoon. Affiche le premier, le dernier, la longueur. Ajoute un SKU avec append().")
            st.info("Indice : dernier élément = liste[-1]")
            code2 = st.text_area("Colle ton code ici :", key="e2j1", height=150)
            if st.button("Soumettre exercice 2"):
                if code2:
                    st.success("Vérifie que tu utilises bien skus[-1] pour le dernier élément.")
                else:
                    st.error("Tape d'abord ton code dans Jupyter.")

        with st.expander("Exercice 3 — Dictionnaire produit complet (20 min)"):
            st.write("Crée un dict pour le FLIR-E5-XT avec 6 attributs. Affiche la certification. Modifie enabled à 0. Compte les clés avec len().")
            code3 = st.text_area("Colle ton code ici :", key="e3j1", height=150)
            if st.button("Soumettre exercice 3"):
                if code3:
                    st.success("Vérifie que len(produit) retourne bien 6.")
                else:
                    st.error("Tape d'abord ton code dans Jupyter.")

        with st.expander("Exercice final — Mini-catalogue liste de dicts (15 min)"):
            st.write("Crée une liste de 3 dicts produits Testoon avec 4 attributs chacun. Affiche le SKU du 2e et la famille du 3e.")
            codef = st.text_area("Colle ton code ici :", key="efj1", height=150)
