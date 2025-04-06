# ChromaDBAdmin

ChromaDBAdmin is a comprehensive web-based administration tool for ChromaDB vector databases. It provides an intuitive interface to manage your ChromaDB collections, documents, and embeddings.

## Features

- **Database Management**: Connect to any ChromaDB persistent database directory
- **Collection Management**: Create, view, edit, and delete collections
- **Document Management**: Add, edit, delete and filter documents in collections
- **Metadata Support**: Full support for metadata on both collections and documents
- **Vector Search**: Perform semantic searches using the OpenAI embedding API
- **Filtering**: Apply filters on metadata and document content
- **Pagination**: Navigate through large collections with ease
- **Embedding Generation**: Automatically generate embeddings using OpenAI API

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/chromadbadmin.git
cd chromadbadmin
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://127.0.0.1:5000/`

3. On the first run, you'll be prompted to select or create a ChromaDB directory.

## Key Components

- **Flask Web Server**: Provides the web interface and API endpoints
- **ChromaDB Client**: Connects to the underlying vector database
- **Document Manager**: Handles CRUD operations for documents
- **Embedding Service**: Generates embeddings using OpenAI's API
- **Collection Manager**: Manages ChromaDB collections

## Fonctionnalités de filtrage

ChromaDBAdmin propose deux types de filtrage puissants qui correspondent directement aux capacités de requête de ChromaDB :

### Filtrage par métadonnées (JSON)

Ce filtrage permet de rechercher des documents selon leurs métadonnées structurées associées :

```json
{"categorie": "rapport", "auteur": "jean.dupont"}
```

Cette requête retournera uniquement les documents dont les métadonnées satisfont ces DEUX conditions simultanément.

Vous pouvez utiliser des opérateurs spéciaux pour des requêtes plus complexes :

- Opérateurs de comparaison : `$gt` (supérieur à), `$gte` (supérieur ou égal), `$lt` (inférieur à), `$lte` (inférieur ou égal)
  ```json
  {"date": {"$gte": "2023-01-01", "$lt": "2023-02-01"}}
  ```

- `$ne` (différent de)
  ```json
  {"statut": {"$ne": "archivé"}}
  ```

- `$in` (dans un tableau de valeurs)
  ```json
  {"categorie": {"$in": ["actualités", "blog", "article"]}}
  ```

- `$nin` (pas dans un tableau)
  ```json
  {"categorie": {"$nin": ["brouillon", "privé"]}}
  ```

### Filtrage par contenu de document (JSON)

Ce filtrage recherche directement dans le contenu textuel des documents :

```json
{"$contains": "intelligence artificielle"}
```

Cette requête retournera les documents dont le contenu contient l'expression "intelligence artificielle".

Le filtrage par contenu utilise principalement l'opérateur `$contains` qui effectue une recherche de sous-chaîne dans le texte du document. Ceci est utile pour trouver des termes, expressions ou motifs spécifiques indépendamment des métadonnées.

### Cas d'utilisation

- **Filtrage par métadonnées** : Idéal pour les données structurées comme les dates, catégories, auteurs, statuts
- **Filtrage par contenu** : Optimal pour la recherche plein texte, pour trouver des termes ou expressions spécifiques
- **Filtrage combiné** : Utilisez les deux types pour des requêtes précises nécessitant à la fois des critères de métadonnées et de contenu

Pour des recherches sémantiques plus complexes, utilisez plutôt la fonction "Recherche sémantique" qui exploite les embeddings pour trouver du contenu sémantiquement similaire plutôt que des correspondances textuelles exactes.

## API Endpoints

The application exposes several REST API endpoints that can be used programmatically:

- `/collections` - List all collections
- `/collection/create` - Create a new collection
- `/collection/<name>/delete` - Delete a collection
- `/collection/<name>/documents` - Get documents in a collection
- `/collection/<name>/document/add` - Add a document
- `/collection/<name>/document/<id>/update` - Update a document
- `/collection/<name>/document/<id>/delete` - Delete a document
- `/collection/<name>/query` - Perform semantic search
- `/get_embedding` - Generate an embedding for text

## Requirements

- Python 3.8+
- ChromaDB
- Flask
- OpenAI API (for embeddings)

## Extending

The application has a modular design that makes it easy to extend:

- Add new embeddings providers in `modules/embedding.py`
- Add new document processors in `modules/document_manager.py`
- Extend the UI by modifying the templates in the `templates/` directory

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.