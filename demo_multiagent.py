import os
import argparse
from openai import OpenAI
from mistralai.client import Mistral
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
            # Initialisation du client Mistral avec la nouvelle syntaxe v1+
            self.client = Mistral(api_key=MISTRAL_API_KEY)
        else:
            raise ValueError(f"Fournisseur de modèle non supporté : {self.provider}")

    def run(self, prompt: str, temperature: float = 0.7) -> str:
        """Exécute la tâche de l'agent en interrogeant le LLM configuré."""
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
            return response.choices[0].message.content
        else:  # Mistral
            # Utilisation de la nouvelle méthode chat.complete de Mistral
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            return response.choices[0].message.content


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
        print(f"\n🚀 Démarrage du workflow pour le sujet : {topic}")
        print(f"Provider utilisé : {self.provider.capitalize()}\n")

        # --- Étape 1: L'agent Chercheur collecte les faits ---
        print(f"🤖 L'agent {self.researcher.name} collecte des informations...")
        research_prompt = f"Trouve les 3 faits les plus importants sur : {topic}"
        research_result = self.researcher.run(research_prompt)
        print(f"✅ Agent {self.researcher.name} a terminé.\n")

        print("📝 Faits collectés par le Chercheur :")
        print(research_result)
        print("-" * 50)

        # --- Étape 2: L'agent Rédacteur écrit l'article ---
        print(f"\n✍️ L'agent {self.writer.name} rédige le contenu...")
        writer_prompt = f"Rédige un court paragraphe basé sur les faits suivants :\n\n{research_result}"
        final_article = self.writer.run(writer_prompt)
        print(f"✅ Agent {self.writer.name} a terminé.\n")

        print("✨ Article final :")
        print(final_article)
        print("\n" + "=" * 50 + "\n")


def main():
    """Point d'entrée principal du script en ligne de commande."""
    parser = argparse.ArgumentParser(description="Démonstration d'un Système Multi-Agents en CLI")
    
    # Arguments que l'utilisateur peut passer en console
    parser.add_argument("topic", type=str, nargs="?", default="L'histoire de la tour Eiffel", help="Le sujet de recherche de l'agent")
    parser.add_argument("--provider", type=str, choices=["mistral", "openai"], default=DEFAULT_PROVIDER, help="Le fournisseur de modèle à utiliser")

    args = parser.parse_args()

    try:
        agent_system = MultiAgentSystem(provider=args.provider)
        agent_system.execute_workflow(args.topic)
    except ValueError as e:
        print(f"\n❌ Erreur de configuration : {e}")
    except Exception as e:
        print(f"\n❌ Une erreur inattendue est survenue : {e}")


if __name__ == "__main__":
    main()