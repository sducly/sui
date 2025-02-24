from langchain.tools import tool
import unicodedata
import json

def normalize(text: str) -> str:
    normalized_text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').lower()
    return normalized_text

@tool
def get_candidates(job: str) -> str:
    """Get candidates matching the specified job title.
       :param job (str): Le nom du métier en Francais. Une Chaine de caractère OBLIGATOIREMENT
    """
    if isinstance(job, dict) and "job" in job:
        job = job["job"]  # Extraction si un objet a été reçu
        
    job = job.strip().strip("'\"")
    
    candidates = [
        {"nom": "Vincent DUPONT", "profession": "Plombier", "expérience": 5, "email": "vincent.dupont@gmail.com"},
        {"nom": "Bob Martin", "profession": "Macon", "expérience": 8, "email": "bob.martin@gmail.com"},
        {"nom": "Charlie Garcia", "profession": "Couvreur", "expérience": 3, "email": "charlie.garcia@gmail.com"},
        {"nom": "Jordi Tremblay", "profession": "Plombier", "expérience": 7, "email": "jordi.tremblay@gmail.com"},
    ]

    filtered = [c for c in candidates if normalize(c["profession"]) == normalize(job)]
    
    json_result = json.dumps(filtered, ensure_ascii=False, indent=2)
    
    return json_result