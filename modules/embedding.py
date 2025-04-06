from openai import OpenAI
import chromadb.utils.embedding_functions as embedding_functions

class EmbeddingService:
    def __init__(self, api_key):
        """Initialise le service d'embedding avec la clé API OpenAI"""
        self.api_key = api_key
        self.model_name = "text-embedding-ada-002"
        
        # Initialiser le client OpenAI
        self.client = None
        if api_key:
            self.client = OpenAI(api_key=api_key)
            
        # Initialiser la fonction d'embedding ChromaDB (alternative)
        self.embedding_function = None
        try:
            if api_key:
                self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=api_key,
                    model_name=self.model_name
                )
        except Exception as e:
            print(f"Impossible d'initialiser la fonction d'embedding ChromaDB: {str(e)}")
    
    def create_embedding(self, text):
        """Crée un embedding en utilisant l'API OpenAI (version 1.0.0+)"""
        if not self.api_key:
            raise ValueError("Clé API OpenAI requise pour la génération d'embeddings")
        
        try:
            # Utiliser d'abord l'embedding_function de ChromaDB si disponible
            if self.embedding_function:
                try:
                    if isinstance(text, list):
                        return self.embedding_function(text)
                    else:
                        return self.embedding_function([text])[0]
                except Exception as e:
                    print(f"Erreur avec embedding_function, fallback vers client OpenAI direct: {str(e)}")
            
            # Sinon, utiliser le client OpenAI directement
            if isinstance(text, list):
                # Traitement par lots
                response = self.client.embeddings.create(
                    input=text,
                    model=self.model_name
                )
                return [item.embedding for item in response.data]
            else:
                # Traitement d'un seul texte
                response = self.client.embeddings.create(
                    input=text,
                    model=self.model_name
                )
                return response.data[0].embedding
                
        except Exception as e:
            print(f"Erreur lors de la création de l'embedding: {str(e)}")
            # Retourner un vecteur vide si erreur
            if isinstance(text, list):
                return [[0] * 1536 for _ in text]
            else:
                return [0] * 1536