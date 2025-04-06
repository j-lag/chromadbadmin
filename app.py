from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
import os
import json
from datetime import datetime
from modules.db_manager import ChromaDBManager
from modules.collection_manager import CollectionManager
from modules.document_manager import DocumentManager
from modules.embedding import EmbeddingService
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# Instances globales
db_manager = None
collection_manager = None
document_manager = None
embedding_service = None

def init_services():
    global embedding_service
    if embedding_service is None:
        embedding_service = EmbeddingService(app.config['OPENAI_API_KEY'])

@app.template_filter('now')
def filter_now(value, format='%Y-%m-%d %H:%M:%S'):
    """Filtre qui retourne la date et l'heure actuelles"""
    return datetime.now().strftime(format)

@app.route('/')
def index():
    global db_manager
    init_services()
    if db_manager is None:
        return render_template('setup.html')
    else:
        collections = collection_manager.list_collections()
        return render_template('index.html', collections=collections)

@app.route('/setup', methods=['POST'])
def setup():
    global db_manager, collection_manager, document_manager
    db_path = request.form.get('db_path')
    
    if not os.path.exists(db_path):
        os.makedirs(db_path, exist_ok=True)
    
    try:
        db_manager = ChromaDBManager(db_path)
        collection_manager = CollectionManager(db_manager)
        document_manager = DocumentManager(db_manager)
        init_services()
        flash('ChromaDB connected successfully!', 'success')
    except Exception as e:
        flash(f'Erreur lors de la connexion à ChromaDB: {str(e)}', 'danger')
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/collections')
def list_collections():
    collections = collection_manager.list_collections()
    return jsonify(collections)

@app.route('/collection/create', methods=['POST'])
def create_collection():
    name = request.form.get('name')
    metadata = request.form.get('metadata', '{}')
    try:
        collection = collection_manager.create_collection(name, metadata)
        return jsonify({"status": "success", "message": f"Collection {name} créée avec succès"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/collection/<name>/delete', methods=['POST'])
def delete_collection(name):
    try:
        collection_manager.delete_collection(name)
        return jsonify({"status": "success", "message": f"Collection {name} supprimée avec succès"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/collection/<name>')
def view_collection(name):
    collection = collection_manager.get_collection(name)
    return render_template('collection.html', collection=collection, name=name)

@app.route('/collection/<name>/documents')
def get_documents(name):
    # Paramètres optionnels pour filtrage
    where = request.args.get('where', None)
    where_document = request.args.get('where_document', None)
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    
    documents = document_manager.get_documents(
        name, where=where, where_document=where_document, 
        limit=limit, offset=offset
    )
    return jsonify(documents)

@app.route('/collection/<name>/document/add', methods=['POST'])
def add_document(name):
    document = request.json.get('document')
    metadata = request.json.get('metadata', {})
    document_id = request.json.get('id', None)
    
    # Générer embedding si nécessaire
    embedding = None
    if request.json.get('generate_embedding', False):
        embedding = embedding_service.create_embedding(document)
    
    result = document_manager.add_document(
        name, document, metadata=metadata, 
        document_id=document_id, embedding=embedding
    )
    return jsonify(result)

@app.route('/collection/<name>/document/<doc_id>/update', methods=['POST'])
def update_document(name, doc_id):
    document = request.json.get('document')
    metadata = request.json.get('metadata', None)
    
    # Générer embedding si nécessaire
    embedding = None
    if request.json.get('generate_embedding', False):
        embedding = embedding_service.create_embedding(document)
    
    result = document_manager.update_document(
        name, doc_id, document=document, 
        metadata=metadata, embedding=embedding
    )
    return jsonify(result)

@app.route('/collection/<name>/document/<doc_id>/delete', methods=['POST'])
def delete_document(name, doc_id):
    result = document_manager.delete_document(name, doc_id)
    return jsonify(result)

@app.route('/collection/<name>/query', methods=['POST'])
def query_collection(name):
    query_text = request.json.get('query_text')
    n_results = int(request.json.get('n_results', 10))
    where = request.json.get('where', None)
    where_document = request.json.get('where_document', None)
    
    # Générer embedding pour requête
    query_embedding = embedding_service.create_embedding(query_text)
    
    results = document_manager.query_documents(
        name, query_embedding, n_results=n_results,
        where=where, where_document=where_document
    )
    return jsonify(results)

@app.route('/collection/<name>/count')
def count_documents(name):
    where = request.args.get('where', None)
    where_document = request.args.get('where_document', None)
    
    count = document_manager.count_documents(
        name, where=where, where_document=where_document
    )
    return jsonify({"count": count})

@app.route('/get_embedding', methods=['POST'])
def get_embedding():
    text = request.json.get('text')
    embedding = embedding_service.create_embedding(text)
    return jsonify({"embedding": embedding})

if __name__ == '__main__':
    app.run(debug=True)