"""
Gestor de datos y almacenamiento de resultados
"""

import json
import os
from datetime import datetime
from typing import Dict, List
import pandas as pd


class DataManager:
    def __init__(self):
        """Inicializa el gestor de datos"""
        # Crear directorio de datos si no existe
        self.data_dir = 'data'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Archivos de almacenamiento
        self.history_file = os.path.join(self.data_dir, 'analysis_history.json')
        self.stats_file = os.path.join(self.data_dir, 'statistics.json')

        # Cargar historial existente
        self.history = self._load_history()

    def _load_history(self) -> List[Dict]:
        """Carga el historial de análisis previos"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_analysis(self, result: Dict) -> None:
        """
        Guarda un resultado de análisis en el historial.

        Args:
            result: Resultado del análisis
        """
        # Agregar timestamp
        result['timestamp'] = datetime.now().isoformat()

        # Agregar al historial
        self.history.append(result)

        # Mantener solo los últimos 1000 registros
        if len(self.history) > 1000:
            self.history = self.history[-1000:]

        # Guardar a archivo
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando historial: {e}")

    def get_statistics(self) -> Dict:
        """
        Calcula estadísticas del historial.

        Returns:
            Diccionario con estadísticas
        """
        if not self.history:
            return {
                'total_analyzed': 0,
                'message': 'No hay datos históricos aún'
            }

        # Filtrar solo resultados válidos (sin errores)
        valid_results = [h for h in self.history if 'sentiment' in h]

        if not valid_results:
            return {
                'total_analyzed': len(self.history),
                'valid_results': 0,
                'errors': len(self.history)
            }

        # Calcular estadísticas
        sentiments = [r['sentiment'] for r in valid_results]
        confidences = [r['confidence'] for r in valid_results]
        stars = [r.get('stars', 0) for r in valid_results if 'stars' in r]
        processing_times = [r.get('processing_time', 0) for r in valid_results if 'processing_time' in r]

        stats = {
            'total_analyzed': len(self.history),
            'valid_results': len(valid_results),
            'errors': len(self.history) - len(valid_results),
            'sentiments': {
                'positive': sentiments.count('POSITIVE'),
                'negative': sentiments.count('NEGATIVE'),
                'neutral': sentiments.count('NEUTRAL')
            },
            'percentages': {
                'positive': round(sentiments.count('POSITIVE') / len(sentiments) * 100, 2),
                'negative': round(sentiments.count('NEGATIVE') / len(sentiments) * 100, 2),
                'neutral': round(sentiments.count('NEUTRAL') / len(sentiments) * 100, 2)
            },
            'average_confidence': round(sum(confidences) / len(confidences), 4) if confidences else 0,
            'average_stars': round(sum(stars) / len(stars), 2) if stars else 0,
            'average_processing_time': round(sum(processing_times) / len(processing_times),
                                             3) if processing_times else 0,
            'last_analysis': valid_results[-1]['timestamp'] if valid_results else None
        }

        # Guardar estadísticas
        self._save_statistics(stats)

        return stats

    def _save_statistics(self, stats: Dict) -> None:
        """Guarda las estadísticas a archivo"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando estadísticas: {e}")

    def load_csv_data(self, filepath: str) -> pd.DataFrame:
        """
        Carga datos desde un archivo CSV.

        Args:
            filepath: Ruta al archivo CSV

        Returns:
            DataFrame con los datos
        """
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            return df
        except Exception as e:
            print(f"Error cargando CSV: {e}")
            return pd.DataFrame()

    def export_results(self, results: List[Dict], format: str = 'csv') -> str:
        """
        Exporta resultados a archivo.

        Args:
            results: Lista de resultados
            format: Formato de exportación ('csv' o 'json')

        Returns:
            Ruta del archivo generado
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if format == 'csv':
            filename = f'results_{timestamp}.csv'
            filepath = os.path.join(self.data_dir, filename)

            df = pd.DataFrame(results)
            df.to_csv(filepath, index=False, encoding='utf-8')

        else:  # json
            filename = f'results_{timestamp}.json'
            filepath = os.path.join(self.data_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        return filepath

    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene los análisis más recientes.

        Args:
            limit: Número máximo de resultados

        Returns:
            Lista de análisis recientes
        """
        return self.history[-limit:] if self.history else []

    def clear_history(self) -> None:
        """Limpia el historial de análisis"""
        self.history = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        print("✅ Historial limpiado")