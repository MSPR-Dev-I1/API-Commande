import os
import json
from google.cloud.pubsub_v1 import PublisherClient

google_project = os.getenv('GOOGLE_PROJECT')

def create_publisher(): # pragma: no cover
    """
        Créer un publisher
    """
    return PublisherClient()

def notification_remboursement_commande_client_message(id_commande: int, token: str):
    """
        Public un message sur le topic annulation-commande-client-message-topic avec l'id commande et le token
    """
    publisher = create_publisher()
    
    notification_remboursement_commande_client_path = publisher.topic_path(
        google_project, 'annulation-commande-client-message-topic')
    data = {
        "id_commande": id_commande,
        "token": token,
    }
    message = bytes(json.dumps(data), 'utf-8')
    publisher.publish(notification_remboursement_commande_client_path, message)
