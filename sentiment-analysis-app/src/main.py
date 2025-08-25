"""
API REST para Análisis de Sentimientos
Autor: Saúl Escamilla Lazcano
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
from datetime import datetime
import os
import sys

# Agregar el directorio padre al path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.model import get_analyzer
from src.utils.preprocessing import TextPreprocessor
from src.data.data_loader import DataManager

# Inicializar Flask
app = Flask(__name__)
CORS(app, origins="*")  # Permitir todas las origenes en desarrollo

# Inicializar componentes
print("🚀 Inicializando API de Análisis de Sentimientos...")
analyzer = get_analyzer()
preprocessor = TextPreprocessor()
data_manager = DataManager()


# ============== RUTAS BÁSICAS ==============

@app.route('/')
def home():
    """Ruta principal con información del API"""
    return jsonify({
        'name': '🎭 Sentiment Analysis API',
        'version': '1.0.0',
        'author': 'Saúl Escamilla Lazcano',
        'status': 'running',
        'endpoints': {
            'GET /': 'Esta información',
            'GET /health': 'Estado del servicio',
            'POST /api/analyze': 'Analizar un texto',
            'POST /api/analyze-batch': 'Analizar múltiples textos',
            'GET /api/stats': 'Estadísticas del servicio',
            'GET /api/model-info': 'Información del modelo'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/health')
def health():
    """Verificación de salud del servicio"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': analyzer is not None,
        'timestamp': datetime.now().isoformat()
    })


# ============== RUTAS DE ANÁLISIS ==============

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analiza el sentimiento de un texto individual.

    Body JSON:
    {
        "text": "texto a analizar",
        "preprocess": true/false (opcional)
    }
    """
    try:
        # Obtener datos del request
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({
                'error': 'No se proporcionó texto para analizar',
                'code': 'MISSING_TEXT'
            }), 400

        text = data['text']
        preprocess = data.get('preprocess', True)

        # Validar longitud
        if len(text) > 5000:
            return jsonify({
                'error': 'El texto excede el límite de 5000 caracteres',
                'code': 'TEXT_TOO_LONG'
            }), 400

        # Preprocesar si se solicita
        if preprocess:
            text_processed = preprocessor.clean_text(text)
        else:
            text_processed = text

        # Analizar sentimiento
        result = analyzer.analyze(text_processed)

        # Guardar en historial
        data_manager.save_analysis(result)

        return jsonify({
            'success': True,
            'result': result,
            'metadata': {
                'preprocessed': preprocess,
                'api_version': '1.0.0'
            }
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'ANALYSIS_ERROR'
        }), 500


@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """
    Analiza múltiples textos.

    Body JSON:
    {
        "texts": ["texto1", "texto2", ...],
        "preprocess": true/false (opcional)
    }
    """
    try:
        data = request.get_json()

        if not data or 'texts' not in data:
            return jsonify({
                'error': 'No se proporcionaron textos',
                'code': 'MISSING_TEXTS'
            }), 400

        texts = data['texts']

        # Limitar cantidad
        if len(texts) > 50:
            return jsonify({
                'error': 'Máximo 50 textos por solicitud',
                'code': 'TOO_MANY_TEXTS'
            }), 400

        preprocess = data.get('preprocess', True)

        # Preprocesar si es necesario
        if preprocess:
            texts_processed = [preprocessor.clean_text(t) for t in texts]
        else:
            texts_processed = texts

        # Analizar en lote
        results = analyzer.analyze_batch(texts_processed)

        # Calcular estadísticas
        stats = calculate_batch_stats(results)

        return jsonify({
            'success': True,
            'results': results,
            'statistics': stats,
            'metadata': {
                'total_texts': len(texts),
                'preprocessed': preprocess,
                'api_version': '1.0.0'
            }
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': 'BATCH_ANALYSIS_ERROR'
        }), 500


# ============== RUTAS DE INFORMACIÓN ==============

@app.route('/api/stats')
def get_stats():
    """Obtiene estadísticas del servicio"""
    stats = data_manager.get_statistics()
    return jsonify(stats)


@app.route('/api/model-info')
def model_info():
    """Información sobre el modelo cargado"""
    info = analyzer.get_model_info()
    return jsonify(info)


@app.route('/api/examples')
def get_examples():
    """Ejemplos de uso del API"""
    return jsonify({
        'single_analysis': {
            'endpoint': 'POST /api/analyze',
            'body': {
                'text': 'Este producto es increíble, lo recomiendo totalmente!',
                'preprocess': True
            }
        },
        'batch_analysis': {
            'endpoint': 'POST /api/analyze-batch',
            'body': {
                'texts': [
                    'Excelente servicio',
                    'Muy decepcionado con la compra',
                    'Está bien, nada especial'
                ],
                'preprocess': True
            }
        }
    })


# ============== FUNCIONES AUXILIARES ==============

def calculate_batch_stats(results):
    """Calcula estadísticas de un análisis por lotes"""
    valid_results = [r for r in results if 'sentiment' in r]

    if not valid_results:
        return {}

    sentiments = [r['sentiment'] for r in valid_results]
    confidences = [r['confidence'] for r in valid_results]

    return {
        'total': len(results),
        'valid': len(valid_results),
        'errors': len(results) - len(valid_results),
        'sentiments': {
            'positive': sentiments.count('POSITIVE'),
            'negative': sentiments.count('NEGATIVE'),
            'neutral': sentiments.count('NEUTRAL')
        },
        'average_confidence': round(sum(confidences) / len(confidences), 4) if confidences else 0,
        'percentages': {
            'positive': round(sentiments.count('POSITIVE') / len(sentiments) * 100, 2) if sentiments else 0,
            'negative': round(sentiments.count('NEGATIVE') / len(sentiments) * 100, 2) if sentiments else 0,
            'neutral': round(sentiments.count('NEUTRAL') / len(sentiments) * 100, 2) if sentiments else 0
        }
    }


# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint no encontrado',
        'code': 'NOT_FOUND',
        'message': 'Verifica la documentación en GET /'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Error interno del servidor',
        'code': 'INTERNAL_ERROR'
    }), 500


# ============== MAIN ==============

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🎭 API de Análisis de Sentimientos")
    print("=" * 50)
    print("📍 Servidor: http://localhost:5000")
    print("📚 Documentación: http://localhost:5000/")
    print("💡 Presiona CTRL+C para detener")
    print("=" * 50 + "\n")

    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False  # Evita cargar el modelo dos veces
    )