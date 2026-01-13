from strawberry.extensions import Extension
from app.core.exceptions import BLLException

class BusinessLogicErrorExtension(Extension):
    def on_request_end(self):
        # On parcourt les erreurs qui ont pu se produire
        for error in self.execution_context.errors:
            original_error = error.original_error
            # Si l'erreur est une de nos exceptions métier...
            if isinstance(original_error, BLLException):
                # ...on peut reformater le message et ajouter des extensions
                error.message = f"[Business Error] {original_error}"
                if not error.extensions:
                    error.extensions = {}
                error.extensions['code'] = original_error.__class__.__name__