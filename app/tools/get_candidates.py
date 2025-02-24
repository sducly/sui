from langchain.tools import tool
import unicodedata
import json

def normalize(text: str) -> str:
    normalized_text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').lower()
    return normalized_text

@tool
def get_candidates(job: str) -> str:
    """Get candidates matching the specified job title.
       :param job (str): Le nom du métier en Francais. 
    """
    print(job)
    job = job.strip().strip("'\"")
    
    candidates = [
        {"nom": "Alice Dupont", "profession": "Plombier", "expérience": 5, "email": "python1@gmail.com"},
        {"nom": "Bob Martin", "profession": "Macon", "expérience": 8, "email": "java1@gmail.com"},
        {"nom": "Charlie Garcia", "profession": "Couvreur", "expérience": 3, "email": "python2@gmail.com"},
        {"nom": "Eve Tremblay", "profession": "Plombier", "expérience": 7, "email": "python3@gmail.com"},
    ]

    filtered = [c for c in candidates if normalize(c["profession"]) == normalize(job)]
    
    json_result = json.dumps(filtered, ensure_ascii=False, indent=2)
    
    return json_result