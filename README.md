# Application Web de Démonstration d'un Système Multi-Agents

Les systèmes multi-agents peuvent vite devenir complexes, donc pour une formation, il vaut mieux utiliser un scénario très visuel et facile à comprendre.

Ce dépôt contient une application web interactive (construite avec Streamlit) qui démontre la coordination de deux agents IA : un **Chercheur** et un **Rédacteur**.

## Usage avec Docker (Recommandé pour les stagiaires)

Cette méthode est la plus simple pour démarrer. Elle ne nécessite que Docker et évite d'installer Python ou des dépendances sur votre machine.

1.  **Configuration de l'API Mistral**

    Créez un fichier nommé `.env` à la racine du projet et ajoutez-y votre clé API Mistral. C'est la seule chose que vous aurez à configurer.

    ```
    # Fichier: .env
    MODEL_PROVIDER=mistral
    MISTRAL_API_KEY=votre_cle_api_mistral_ici
    
    # Optionnel: vous pouvez spécifier un modèle, sinon "mistral-small-latest" sera utilisé.
    # MISTRAL_MODEL=open-mistral-7b
    ```

2.  **Construire l'image Docker**

    Ouvrez un terminal et exécutez cette commande pour créer l'image qui contiendra l'application :

    ```sh
    docker build -t multi-agent-demo .
    ```

3.  **Lancer l'application web**

    Cette commande lance le conteneur et rend l'application accessible sur votre machine.

    ```sh
    docker run --rm --env-file .env -p 8501:8501 multi-agent-demo
    ```

4.  **Accéder à l'application**

    Ouvrez votre navigateur web et allez à l'adresse : [http://localhost:8501](http://localhost:8501)

## Installation et Usage en local (pour les développeurs)

### 1. Installation

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configuration (.env)

Placez vos clés dans un fichier `.env` à la racine. Exemples :

Mistral (recommandé pour les stagiaires si vous avez une clé gratuite) :

```
MISTRAL_API_KEY=sk-...
MODEL_PROVIDER=mistral
MISTRAL_MODEL=mistral-1
```

OpenAI :

```
OPENAI_API_KEY=sk-...
MODEL_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
```

Usage

```bash
# utiliser le provider par défaut défini dans .env
python demo_multiagent.py "Sujet de démonstration"

# forcer le provider en ligne de commande
python demo_multiagent.py "Sujet" --provider mistral
```

Notes
- L'adaptateur Mistral ici est minimal et destiné à la formation. Adaptez selon l'API réelle si besoin.
- Ne commitez jamais votre `.env` dans un dépôt public.
- Vérifiez les quotas et conditions d'utilisation du fournisseur choisi.

Améliorations possibles : ajouter un agent de validation, sauvegarder les conversations, ou visualiser le workflow en temps réel.