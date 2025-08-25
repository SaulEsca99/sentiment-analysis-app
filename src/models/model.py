"""
Modelo de Análisis de Sentimientos
Utiliza BERT multilingüe para clasificar sentimientos en español e inglés
"""

from transformers import pipeline
import torch
import time
from typing import Dict, List, Union


class SentimentAnalyzer:
    def __init__(self):
        """
        Inicializa el modelo de análisis de sentimientos.
        Usa un modelo preentrenado de Hugging Face.
        """
        print("🔄 Cargando modelo de análisis de sentimientos...")
        print("   (Esto puede tardar 1-2 minutos la primera vez)")

        try:
            # Modelo multilingüe que funciona bien con español
            self.model = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                device=-1  # -1 para CPU, 0 para GPU
            )
            print("✅ Modelo cargado exitosamente!")

        except Exception as e:
            print(f"❌ Error cargando el modelo: {e}")
            # Modelo de respaldo más ligero
            print("🔄 Intentando con modelo alternativo...")
            self.model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1
            )
            print("✅ Modelo alternativo cargado!")

    def analyze(self, text: str) -> Dict:
        """
        Analiza el sentimiento de un texto.

        Args:
            text: Texto a analizar

        Returns:
            Diccionario con resultados del análisis
        """
        if not text or len(text.strip()) == 0:
            raise ValueError("El texto no puede estar vacío")

        # Limitar longitud del texto (BERT tiene límite de 512 tokens)
        text_truncated = text[:500] if len(text) > 500 else text

        # Medir tiempo de procesamiento
        start_time = time.time()

        try:
            # Realizar análisis
            result = self.model(text_truncated)[0]

            # Procesar resultado según el modelo
            sentiment_data = self._process_result(result)

            # Agregar metadatos
            sentiment_data.update({
                'text_original': text,
                'text_analyzed': text_truncated,
                'text_truncated': len(text) > 500,
                'text_length': len(text),
                'processing_time': round(time.time() - start_time, 3)
            })

            return sentiment_data

        except Exception as e:
            return {
                'error': str(e),
                'text_original': text,
                'processing_time': round(time.time() - start_time, 3)
            }

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analiza múltiples textos en lote.

        Args:
            texts: Lista de textos a analizar

        Returns:
            Lista de resultados
        """
        results = []

        for i, text in enumerate(texts):
            try:
                result = self.analyze(text)
                result['index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'index': i,
                    'error': str(e),
                    'text_original': text[:100] + '...' if len(text) > 100 else text
                })

        return results

    def _process_result(self, result: Dict) -> Dict:
        """
        Procesa el resultado del modelo y lo estandariza.

        Args:
            result: Resultado crudo del modelo

        Returns:
            Diccionario estandarizado
        """
        label = result['label']
        score = result['score']

        # Para el modelo nlptown (5 estrellas)
        if 'star' in label.lower():
            stars = int(label.split()[0])

            if stars <= 2:
                sentiment = 'NEGATIVE'
                emoji = '😔'
                sentiment_score = -score
            elif stars == 3:
                sentiment = 'NEUTRAL'
                emoji = '😐'
                sentiment_score = 0
            else:
                sentiment = 'POSITIVE'
                emoji = '😊'
                sentiment_score = score

            return {
                'sentiment': sentiment,
                'confidence': round(score, 4),
                'stars': stars,
                'emoji': emoji,
                'sentiment_score': round(sentiment_score, 4),
                'raw_label': label
            }

        # Para otros modelos (POSITIVE/NEGATIVE)
        else:
            if label.upper() == 'POSITIVE' or label == 'LABEL_1':
                sentiment = 'POSITIVE'
                emoji = '😊'
                stars = 4 if score > 0.9 else 5
                sentiment_score = score
            else:
                sentiment = 'NEGATIVE'
                emoji = '😔'
                stars = 2 if score > 0.9 else 1
                sentiment_score = -score

            return {
                'sentiment': sentiment,
                'confidence': round(score, 4),
                'stars': stars,
                'emoji': emoji,
                'sentiment_score': round(sentiment_score, 4),
                'raw_label': label
            }

    def get_model_info(self) -> Dict:
        """
        Obtiene información sobre el modelo cargado.

        Returns:
            Información del modelo
        """
        return {
            'model_name': self.model.model.name_or_path if hasattr(self.model.model, 'name_or_path') else 'unknown',
            'task': 'sentiment-analysis',
            'framework': 'transformers',
            'device': 'CPU' if self.model.device.type == 'cpu' else 'GPU'
        }


# Singleton para mantener una sola instancia del modelo
_analyzer_instance = None


def get_analyzer() -> SentimentAnalyzer:
    """
    Obtiene la instancia única del analizador.
    Patrón Singleton para evitar cargar el modelo múltiples veces.
    """
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = SentimentAnalyzer()
    return _analyzer_instance