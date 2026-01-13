
class BaseAppException(Exception):
    """Exception de base pour l'application."""
    pass

class DALException(BaseAppException):
    """Exception levée pour les erreurs de la couche d'accès aux données (DAL)."""
    def __init__(self, message: str, original_exception: Exception = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)

class BLLException(BaseAppException):
    """Exception de base pour les erreurs de la couche métier (BLL)."""
    pass

class NotFoundBLLException(BLLException):
    """Levée lorsqu'une ressource n'est pas trouvée."""
    def __init__(self, resource_name: str, resource_id: int | str):
        message = f"{resource_name} avec l'ID '{resource_id}' non trouvé."
        super().__init__(message)

class ValidationBLLException(BLLException):
    """Levée pour les erreurs de validation des règles métier."""
    pass
