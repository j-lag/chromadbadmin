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
