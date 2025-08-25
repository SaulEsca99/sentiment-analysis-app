"""
Utilidades de preprocesamiento de texto
"""

import re
import string
from typing import List, Dict


class TextPreprocessor:
    def __init__(self):
        """Inicializa el preprocesador con configuraciones por defecto"""
        # Palabras vacías comunes en español
        self.stop_words_es = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se',
            'no', 'haber', 'por', 'con', 'su', 'para', 'como', 'estar',
            'tener', 'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o',
            'poder', 'decir', 'este', 'ir', 'otro', 'ese', 'si', 'me',
            'ya', 'ver', 'porque', 'dar', 'cuando', 'muy', 'sin', 'vez',
            'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo',
            'yo', 'también', 'hasta', 'año', 'dos', 'querer', 'entre'
        }

        # Emojis comunes y su significado
        self.emoji_dict = {
            '😊': 'feliz',
            '😃': 'feliz',
            '😄': 'muy feliz',
            '😁': 'muy feliz',
            '😍': 'amor',
            '❤️': 'amor',
            '😔': 'triste',
            '😢': 'triste',
            '😭': 'muy triste',
            '😡': 'enojado',
            '😠': 'enojado',
            '😤': 'frustrado',
            '👍': 'bien',
            '👎': 'mal',
            '⭐': 'estrella',
            '✨': 'excelente',
            '💔': 'decepcion',
            '🤮': 'asco',
            '😐': 'neutral',
            '😑': 'neutral',
            '🙄': 'molesto'
        }

    def clean_text(self, text: str) -> str:
        """
        Limpia el texto para análisis.

        Args:
            text: Texto a limpiar

        Returns:
            Texto limpio
        """
        if not text:
            return ""

        # Convertir a string si no lo es
        text = str(text)

        # Mantener emojis pero convertirlos a texto
        text = self._convert_emojis(text)

        # Eliminar URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # Eliminar menciones (@usuario)
        text = re.sub(r'@\w+', '', text)

        # Eliminar hashtags pero mantener la palabra
        text = re.sub(r'#(\w+)', r'\1', text)

        # Eliminar caracteres HTML
        text = re.sub(r'<.*?>', '', text)

        # Normalizar espacios en blanco
        text = re.sub(r'\s+', ' ', text)

        # Eliminar espacios al inicio y final
        text = text.strip()

        return text

    def _convert_emojis(self, text: str) -> str:
        """Convierte emojis a palabras"""
        for emoji, word in self.emoji_dict.items():
            text = text.replace(emoji, f' {word} ')
        return text

    def remove_stopwords(self, text: str, language: str = 'es') -> str:
        """
        Elimina palabras vacías del texto.

        Args:
            text: Texto a procesar
            language: Idioma ('es' para español)

        Returns:
            Texto sin palabras vacías
        """
        if language == 'es':
            stop_words = self.stop_words_es
        else:
            stop_words = set()

        words = text.lower().split()
        filtered_words = [w for w in words if w not in stop_words]

        return ' '.join(filtered_words)

    def normalize_text(self, text: str) -> str:
        """
        Normalización avanzada del texto.

        Args:
            text: Texto a normalizar

        Returns:
            Texto normalizado
        """
        # Convertir a minúsculas
        text = text.lower()

        # Eliminar acentos (opcional, puede afectar el sentimiento)
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n', 'ü': 'u'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        # Eliminar puntuación excesiva
        text = re.sub(r'[' + string.punctuation + ']+', ' ', text)

        # Normalizar números
        text = re.sub(r'\d+', 'NUM', text)

        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def extract_features(self, text: str) -> Dict:
        """
        Extrae características del texto para análisis.

        Args:
            text: Texto a analizar

        Returns:
            Diccionario con características
        """
        features = {
            'length': len(text),
            'word_count': len(text.split()),
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / max(len(text), 1),
            'has_emoji': any(emoji in text for emoji in self.emoji_dict.keys()),
            'repeated_chars': bool(re.search(r'(.)\1{2,}', text)),
            'all_caps': text.isupper() and len(text) > 3
        }

        return features

    def batch_clean(self, texts: List[str]) -> List[str]:
        """
        Limpia múltiples textos.

        Args:
            texts: Lista de textos

        Returns:
            Lista de textos limpios
        """
        return [self.clean_text(text) for text in texts]