# Routes package
from .boards import boards_bp
from .lists import lists_bp
from .cards import cards_bp
from .auth import auth_bp

__all__ = ['boards_bp', 'lists_bp', 'cards_bp', 'auth_bp']
