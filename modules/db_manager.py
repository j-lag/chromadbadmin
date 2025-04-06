import chromadb
from chromadb.config import Settings

class ChromaDBManager:
    def __init__(self, persist_directory):
        """Initialise la connexion à ChromaDB"""
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.persist_directory = persist_directory
    
    def get_client(self):
        """Retourne le client ChromaDB"""
        return self.client
    
    def get_path(self):
        """Retourne le chemin du répertoire de persistance"""
        return self.persist_directory
