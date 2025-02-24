from langchain.tools import tool

@tool
def send_email(input_dict: str) -> str:
    """
    Envoi un email sur une adresse précise

    :param input_dict: Un dictionnaire contenant :
        - email (str) : L'adresse email du destinataire. Obligatoire.
        - message (str) : Le message de l'email. Obligatoire.

    :return: Un message de confirmation si l'email a été envoyé, sinon un message d'erreur
    """  
    email = input_dict.get("email")
    message = input_dict.get("message")
    
    if not email or not message:
        raise ValueError("Email and message are required")
        
    return f"Email sent to {email}: {message}"
