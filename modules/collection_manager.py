import json

class CollectionManager:
    def __init__(self, db_manager):
        """Initialise le gestionnaire de collections"""
        self.client = db_manager.get_client()
    
    def list_collections(self):
        """Liste toutes les collections disponibles"""
        collection_names = self.client.list_collections()
        collections = []
        
        # Dans ChromaDB v0.6.0+, list_collections() ne retourne que les noms
        for name in collection_names:
            try:
                collection = self.client.get_collection(name=name)
                collections.append({"name": name, "metadata": collection.metadata})
            except Exception as e:
                collections.append({"name": name, "metadata": {}})
                
        return collections
    
    def create_collection(self, name, metadata=None):
        """Crée une nouvelle collection"""
        if metadata and isinstance(metadata, str):
            try:
                metadata = json.loads(metadata)
            except json.JSONDecodeError:
                metadata = {"description": metadata}
                
        collection = self.client.create_collection(name=name, metadata=metadata or {})
        return {"name": collection.name, "metadata": collection.metadata}
    
    def delete_collection(self, name):
        """Supprime une collection"""
        self.client.delete_collection(name=name)
        return True
    
    def get_collection(self, name):
        """Récupère une collection par son nom"""
        collection = self.client.get_collection(name=name)
        return {"name": collection.name, "metadata": collection.metadata}
    
    def modify_collection(self, name, new_metadata=None):
        """Modifie les métadonnées d'une collection"""
        collection = self.client.get_collection(name=name)
        
        if new_metadata:
            if isinstance(new_metadata, str):
                new_metadata = json.loads(new_metadata)
            collection.modify(metadata=new_metadata)
        
        return {"name": collection.name, "metadata": collection.metadata}
