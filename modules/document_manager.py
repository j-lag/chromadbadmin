import json
import uuid

class DocumentManager:
    def __init__(self, db_manager):
        """Initialise le gestionnaire de documents"""
        self.client = db_manager.get_client()
    
    def get_documents(self, collection_name, where=None, where_document=None, limit=100, offset=0):
        """Récupère les documents d'une collection avec filtrage optionnel"""
        collection = self.client.get_collection(name=collection_name)
        
        # Traiter les entrées vides ou None
        if where == "" or where is None:
            where = None
        elif isinstance(where, str):
            try:
                where = json.loads(where)
            except json.JSONDecodeError:
                where = None
                
        if where_document == "" or where_document is None:
            where_document = None
        elif isinstance(where_document, str):
            try:
                where_document = json.loads(where_document)
            except json.JSONDecodeError:
                where_document = None
        
        # Construire les arguments pour get()
        get_kwargs = {
            "limit": limit,
            "offset": offset,
            "include": ["embeddings", "metadatas", "documents"]
        }
        
        # Ajouter les filtres seulement s'ils ne sont pas None
        if where is not None:
            get_kwargs["where"] = where
            
        if where_document is not None:
            get_kwargs["where_document"] = where_document
        
        result = collection.get(**get_kwargs)
        
        # Formater la réponse
        documents = []
        for i in range(len(result['ids'])):
            # Convertir l'embedding NumPy en liste Python si présent
            embedding = None
            if 'embeddings' in result and i < len(result['embeddings']) and result['embeddings'][i] is not None:
                embedding = result['embeddings'][i].tolist() if hasattr(result['embeddings'][i], 'tolist') else result['embeddings'][i]
                
            doc = {
                "id": result['ids'][i],
                "document": result['documents'][i] if 'documents' in result and i < len(result['documents']) else None,
                "embedding": embedding,
                "metadata": result['metadatas'][i] if 'metadatas' in result and i < len(result['metadatas']) else {}
            }
            documents.append(doc)
        
        return documents
    
    def add_document(self, collection_name, document, metadata=None, document_id=None, embedding=None):
        """Ajoute un document à une collection"""
        collection = self.client.get_collection(name=collection_name)
        
        # Traiter l'ajout d'un seul document
        if isinstance(document, str):
            ids = [document_id] if document_id else [str(uuid.uuid4())]
            documents = [document]
            metadatas = [metadata] if metadata else None
            embeddings = [embedding] if embedding else None
        else:
            # Si on ajoute plusieurs documents
            ids = document_id if document_id else [str(uuid.uuid4()) for _ in document]
            documents = document
            metadatas = metadata if metadata else None
            embeddings = embedding if embedding else None
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        
        return {"status": "success", "added": len(documents), "ids": ids}
    
    def update_document(self, collection_name, document_id, document=None, metadata=None, embedding=None):
        """Met à jour un document existant"""
        collection = self.client.get_collection(name=collection_name)
        
        collection.update(
            ids=[document_id],
            documents=[document] if document else None,
            metadatas=[metadata] if metadata else None,
            embeddings=[embedding] if embedding else None
        )
        
        return {"status": "success", "updated": 1}
    
    def delete_document(self, collection_name, document_id):
        """Supprime un document"""
        collection = self.client.get_collection(name=collection_name)
        
        collection.delete(ids=[document_id])
        
        return {"status": "success", "deleted": 1}
    
    def query_documents(self, collection_name, query_embedding, n_results=10, where=None, where_document=None):
        """Effectue une recherche par similarité"""
        collection = self.client.get_collection(name=collection_name)
        
        # Traiter les entrées vides ou None
        if where == "" or where is None:
            where = None
        elif isinstance(where, str):
            try:
                where = json.loads(where)
            except json.JSONDecodeError:
                where = None
                
        if where_document == "" or where_document is None:
            where_document = None
        elif isinstance(where_document, str):
            try:
                where_document = json.loads(where_document)
            except json.JSONDecodeError:
                where_document = None
        
        # Construire les arguments pour query()
        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": n_results,
        }
        
        # Ajouter les filtres seulement s'ils ne sont pas None
        if where is not None:
            query_kwargs["where"] = where
            
        if where_document is not None:
            query_kwargs["where_document"] = where_document
        
        result = collection.query(**query_kwargs)
        
        # Formater la réponse
        documents = []
        for i in range(len(result['ids'][0])):
            # Convertir la distance en float Python standard si c'est un type NumPy
            distance = None
            if 'distances' in result and 0 < len(result['distances']) and i < len(result['distances'][0]):
                distance = float(result['distances'][0][i]) if result['distances'][0][i] is not None else None
            
            doc = {
                "id": result['ids'][0][i],
                "document": result['documents'][0][i] if 'documents' in result and 0 < len(result['documents']) else None,
                "metadata": result['metadatas'][0][i] if 'metadatas' in result and 0 < len(result['metadatas']) else {},
                "distance": distance
            }
            documents.append(doc)
        
        return documents
    
    def count_documents(self, collection_name, where=None, where_document=None):
        """Compte le nombre de documents dans une collection"""
        collection = self.client.get_collection(name=collection_name)
        
        # Traiter les entrées vides ou None
        if where == "" or where is None:
            where = None
        elif isinstance(where, str):
            try:
                where = json.loads(where)
            except json.JSONDecodeError:
                where = None
                
        if where_document == "" or where_document is None:
            where_document = None
        elif isinstance(where_document, str):
            try:
                where_document = json.loads(where_document)
            except json.JSONDecodeError:
                where_document = None
        
        # Dans les nouvelles versions de ChromaDB, count() ne prend pas d'arguments de filtrage
        # Si aucun filtre n'est appliqué, utilisez count() directement
        if where is None and where_document is None:
            return collection.count()
            
        # Sinon, utilisez get() avec des filtres et comptez les résultats
        # Remarque : "ids" n'est plus une valeur valide pour include, utilisons "metadatas" qui est généralement léger
        get_kwargs = {"include": ["metadatas"]}
        
        if where is not None:
            get_kwargs["where"] = where
            
        if where_document is not None:
            get_kwargs["where_document"] = where_document
            
        result = collection.get(**get_kwargs)
        return len(result['ids'])