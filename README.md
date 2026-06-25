# Guide d'Expérimentation — Système Multi-Agents (Version CLI)

Ce dépôt contient une application en ligne de commande (CLI) conçue pour la formation et l'apprentissage des systèmes multi-agents. Elle permet d'observer la coordination simple et séquentielle de deux agents IA : un **Chercheur** et un **Rédacteur**.

---

## 🛠️ Configuration Initiale (Essentiel)

Avant de lancer le programme, vous devez configurer vos clés d'API.

1. Créez un fichier nommé `.env` à la racine du projet.
2. Ajoutez-y vos configurations selon le fournisseur (Provider) choisi.

### Option A : Utiliser Mistral AI (Recommandé)

```env
MODEL_PROVIDER=mistral
MISTRAL_API_KEY=votre_cle_api_mistral_ici
# Optionnel : MISTRAL_MODEL=mistral-small-latest
```

### Option B : Utiliser OpenAI

```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=votre_cle_api_openai_ici
# Optionnel : OPENAI_MODEL=gpt-4o-mini
```

---

## 🐳 Méthode 1 : Usage avec Docker (Recommandé pour les stagiaires)

Cette méthode est la plus simple car elle évite d'avoir à installer Python ou des dépendances directement sur votre machine.

### 1. Construire l'image Docker

Ouvrez un terminal dans le dossier du projet et exécutez :

```bash
docker build -t multi-agent-demo .

```

### 2. Exécuter le programme

Vous pouvez maintenant lancer des tâches directement depuis votre console :

* **Avec le sujet par défaut** (L'histoire de la tour Eiffel) :
```bash
docker run --rm --env-file .env multi-agent-demo

```


* **Avec un sujet de votre choix** :
```bash
docker run --rm --env-file .env multi-agent-demo "La découverte de la planète Mars"

```


* **En changeant de fournisseur (provider) à la volée** :
```bash
docker run --rm --env-file .env multi-agent-demo "La recette du croissant" --provider openai

```



---

## 🐍 Méthode 2 : Installation en local (Pour aller plus loin)

Si vous souhaitez modifier directement le code et voir le résultat instantanément sans reconstruire l'image Docker :

### 1. Installation de l'environnement

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement
# Sur macOS/Linux :
source .venv/bin/activate
# Sur Windows (Prompt classique) :
.venv\Scripts\activate

# Installer les dépendances indispensables
pip install -r requirements.txt

```

### 2. Lancement en ligne de commande

```bash
# Utiliser le sujet par défaut
python demo_multiagent.py

# Explorer un sujet spécifique
python demo_multiagent.py "L'histoire de la cryptographie"

# Forcer l'utilisation d'un provider spécifique
python demo_multiagent.py "L'histoire de la cryptographie" --provider mistral

```

---

## 🧪 Exercices pratiques et défis pour les stagiaires

Pour bien comprendre le fonctionnement des agents, voici quelques modifications que vous pouvez tenter dans le fichier `demo_multiagent.py` :

1. **Modifier le comportement d'un agent** : Allez dans la classe `MultiAgentSystem` et modifiez le texte du `researcher_role` ou du `writer_role`. Par exemple, demandez au chercheur de trouver 5 faits au lieu de 3, ou demandez au rédacteur d'adopter un ton humoristique, poétique ou journalistique.
2. **Jouer avec la créativité (La température)** : Dans la méthode `execute_workflow`, modifiez le paramètre `temperature` lors de l'appel à `.run()` (ex: mettez `temperature=0.1` pour des réponses très factuelles et froides, ou `temperature=1.0` pour plus de fantaisie).
3. **Le défi ultime (Ajouter un 3ème agent)** : Modifiez le code pour ajouter un agent **"Correcteur"** (ou Traducteur). Cet agent devra prendre le texte produit par le Rédacteur et corriger les fautes d'orthographe ou le traduire en anglais avant d'afficher le résultat final.
