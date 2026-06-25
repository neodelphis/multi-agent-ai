import os
import streamlit as st
from openai import OpenAI
from mistralai import MistralClient
from mistralai.models.chat_completion import ChatMessage # Assurez-vous que cette importation est correcte pour votre version
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

# Récupérer les configurations depuis l'environnement
DEFAULT_PROVIDER = os.getenv("MODEL_PROVIDER", "openai").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")


class SimpleAgent:
    """Un agent simple avec un rôle spécifique, utilisant un fournisseur de modèle (LLM) configurable."""

    def __init__(self, name: str, role: str, provider: str, model: str):
        self.name = name
        self.role = role
        self.provider = provider
        self.model = model

        if self.provider == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("La clé API OpenAI (OPENAI_API_KEY) n'est pas configurée.")
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        elif self.provider == "mistral":
            if not MISTRAL_API_KEY:
                raise ValueError("La clé API Mistral (MISTRAL_API_KEY) n'est pas configurée.")
            self.client = MistralClient(api_key=MISTRAL_API_KEY)
        else:
            raise ValueError(f"Fournisseur de modèle non supporté : {self.provider}")

    def run(self, prompt: str, temperature: float = 0.7) -> str:
        """Exécute la tâche de l'agent en interrogeant le LLM configuré."""
        # L'affichage est géré par le spinner dans la boucle principale

        messages = [
            {"role": "system", "content": self.role},
            {"role": "user", "content": prompt},
        ]

        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            result = response.choices[0].message.content
        else:  # Mistral
            # Conversion du format des messages pour le client Mistral
            mistral_messages = [ChatMessage(role=m["role"], content=m["content"]) for m in messages] # type: ignore
            response = self.client.chat(
                model=self.model,
                messages=mistral_messages,
                temperature=temperature,
            )
            result = response.choices[0].message.content
        return result


class MultiAgentSystem:
    """Orchestre un workflow simple entre plusieurs agents IA."""

    def __init__(self, provider: str):
        self.provider = provider
        model = MISTRAL_MODEL if provider == "mistral" else OPENAI_MODEL

        # Définition de l'agent Chercheur
        researcher_role = """
        Tu es un agent de recherche expert.
        Ton objectif est de trouver des informations factuelles, précises et concises sur un sujet.
        Ta réponse doit être une liste à puces contenant les 3 faits les plus pertinents.
        """
        self.researcher = SimpleAgent(
            name="Chercheur",
            role=researcher_role,
            provider=provider,
            model=model,
        )

        # Définition de l'agent Rédacteur
        writer_role = """
        Tu es un rédacteur de contenu créatif et engageant.
        À partir de faits bruts, tu dois rédiger un paragraphe court et captivant (environ 3-4 phrases).
        N'ajoute aucune information qui ne provient pas des faits fournis.
        """
        self.writer = SimpleAgent(
            name="Rédacteur",
            role=writer_role,
            provider=provider,
            model=model,
        )

    def execute_workflow(self, topic: str):
        """Exécute la séquence de tâches : recherche puis rédaction."""
        st.info(f"🚀 Démarrage du workflow pour le sujet : **{topic}**")
        st.write(f"Provider utilisé : **{self.provider.capitalize()}**")

        # --- Étape 1: L'agent Chercheur collecte les faits ---
        research_prompt = f"Trouve les 3 faits les plus importants sur : {topic}"
        with st.spinner(f"🤖 L'agent **{self.researcher.name}** collecte des informations..."):
            research_result = self.researcher.run(research_prompt)
        st.success(f"✅ Agent **{self.researcher.name}** a terminé.")

        st.subheader("📝 Faits collectés par le Chercheur")
        st.markdown(research_result)

        # --- Étape 2: L'agent Rédacteur écrit l'article ---
        writer_prompt = f"Rédige un court paragraphe basé sur les faits suivants :\n\n{research_result}"
        with st.spinner(f"✍️ L'agent **{self.writer.name}** rédige le contenu..."):
            final_article = self.writer.run(writer_prompt)
        st.success(f"✅ Agent **{self.writer.name}** a terminé.")

        st.subheader("✨ Article final")
        st.markdown(final_article)
        st.balloons()


def main():
    """Point d'entrée principal du script."""
    st.set_page_config(page_title="Démonstration Multi-Agents", layout="centered")
    st.title("🤖 Démonstration d'un Système Multi-Agents")

    st.sidebar.header("Configuration")
    provider = st.sidebar.selectbox(
        "Choisissez le fournisseur de modèle",
        ("mistral", "openai"),
        index=0 if DEFAULT_PROVIDER == "mistral" else 1,
    )

    topic = st.text_input(
        "Quel sujet voulez-vous explorer ?",
        "L'histoire de la tour Eiffel"
    )

    if st.button("Lancer les agents !", type="primary"):
        if topic:
            try:
                agent_system = MultiAgentSystem(provider=provider)
                agent_system.execute_workflow(topic)
            except ValueError as e:
                st.error(f"Erreur de configuration : {e}")
            except Exception as e:
                st.error(f"Une erreur inattendue est survenue : {e}")
        else:
            st.warning("Veuillez entrer un sujet.")


if __name__ == "__main__":
    main()