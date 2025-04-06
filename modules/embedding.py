import openai

class EmbeddingService:
    def __init__(self, api_key):
        """Initialise le service d'embedding avec la clé API OpenAI"""
        openai.api_key = api_key
    
    def create_embedding(self, text):
        """Crée un embedding en utilisant l'API OpenAI"""
        if not openai.api_key:
            raise ValueError("Clé API OpenAI requise pour la génération d'embeddings")
        
        try:
            if isinstance(text, list):
                # Traitement par lots
                response = openai.Embedding.create(
                    input=text,
                    model="text-embedding-ada-002"
                )
                return [item["embedding"] for item in response["data"]]
            else:
                # Traitement d'un seul texte
                response = openai.Embedding.create(
                    input=text,
                    model="text-embedding-ada-002"
                )
                return response["data"][0]["embedding"]
        except Exception as e:
            print(f"Erreur lors de la création de l'embedding: {str(e)}")
            # Retourner un vecteur vide si erreur
            if isinstance(text, list):
                return [[0] * 1536 for _ in text]
            else:
                return [0] * 1536
