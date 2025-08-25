"""
Script de prueba para el API de análisis de sentimientos
"""

import requests
import json
import time
from typing import Dict, List

# URL base del API
BASE_URL = "http://localhost:5000"


# Colores para la terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(title: str):
    """Imprime un encabezado bonito"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 50}{Colors.END}\n")


def print_result(result: Dict):
    """Imprime un resultado de análisis de forma bonita"""
    if 'error' in result:
        print(f"{Colors.RED}❌ Error: {result['error']}{Colors.END}")
        return

    if 'result' in result:
        res = result['result']
    else:
        res = result

    # Color según sentimiento
    sentiment = res.get('sentiment', 'UNKNOWN')
    if sentiment == 'POSITIVE':
        color = Colors.GREEN
    elif sentiment == 'NEGATIVE':
        color = Colors.RED
    else:
        color = Colors.YELLOW

    print(f"{color}Sentimiento: {sentiment} {res.get('emoji', '')}{Colors.END}")
    print(f"Confianza: {res.get('confidence', 0) * 100:.1f}%")
    print(f"Estrellas: {'⭐' * res.get('stars', 0)}")
    print(f"Tiempo: {res.get('processing_time', 0)}s")
    print("-" * 30)


def test_health():
    """Prueba el endpoint de salud"""
    print_header("PRUEBA DE SALUD")

    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ Servicio saludable{Colors.END}")
        else:
            print(f"{Colors.RED}❌ Problema con el servicio{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}❌ Error conectando al servidor: {e}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Asegúrate de que el servidor esté corriendo (python src/main.py){Colors.END}")
        return False

    return True


def test_single_analysis():
    """Prueba análisis individual"""
    print_header("ANÁLISIS INDIVIDUAL")

    textos_prueba = [
        "Este producto es increíble, lo recomiendo totalmente! 😊",
        "Terrible experiencia, nunca más compraré aquí. Muy decepcionado.",
        "Está bien, nada especial. Cumple su función.",
        "¡¡¡EXCELENTE!!! Superó todas mis expectativas ⭐⭐⭐⭐⭐",
        "No vale la pena el precio, hay mejores opciones en el mercado 👎"
    ]

    for i, texto in enumerate(textos_prueba, 1):
        print(f"{Colors.BOLD}Prueba {i}:{Colors.END}")
        print(f"Texto: \"{texto[:50]}...\"" if len(texto) > 50 else f"Texto: \"{texto}\"")

        try:
            response = requests.post(
                f"{BASE_URL}/api/analyze",
                json={"text": texto, "preprocess": True}
            )

            if response.status_code == 200:
                print_result(response.json())
            else:
                print(f"{Colors.RED}Error: {response.status_code}{Colors.END}")

        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.END}")

        time.sleep(0.5)  # Pequeña pausa entre requests


def test_batch_analysis():
    """Prueba análisis por lotes"""
    print_header("ANÁLISIS POR LOTES")

    textos = [
        "Excelente servicio al cliente",
        "Producto defectuoso, solicité devolución",
        "Normal, ni bueno ni malo",
        "Superó mis expectativas",
        "Pérdida total de dinero"
    ]

    print(f"Analizando {len(textos)} textos en lote...")

    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-batch",
            json={"texts": textos, "preprocess": True}
        )

        if response.status_code == 200:
            data = response.json()

            # Mostrar estadísticas
            if 'statistics' in data:
                stats = data['statistics']
                print(f"\n{Colors.BOLD}📊 Estadísticas:{Colors.END}")
                print(f"Total: {stats.get('total', 0)}")
                print(f"Positivos: {stats['sentiments']['positive']} ({stats['percentages']['positive']:.1f}%)")
                print(f"Negativos: {stats['sentiments']['negative']} ({stats['percentages']['negative']:.1f}%)")
                print(f"Neutrales: {stats['sentiments']['neutral']} ({stats['percentages']['neutral']:.1f}%)")
                print(f"Confianza promedio: {stats.get('average_confidence', 0) * 100:.1f}%")

            # Mostrar resultados individuales
            print(f"\n{Colors.BOLD}Resultados individuales:{Colors.END}")
            for i, result in enumerate(data.get('results', [])):
                print(f"\n{i + 1}. {textos[i][:50]}...")
                if 'sentiment' in result:
                    sentiment = result['sentiment']
                    emoji = result.get('emoji', '')
                    confidence = result.get('confidence', 0)

                    if sentiment == 'POSITIVE':
                        color = Colors.GREEN
                    elif sentiment == 'NEGATIVE':
                        color = Colors.RED
                    else:
                        color = Colors.YELLOW

                    print(f"   {color}{sentiment} {emoji} ({confidence * 100:.1f}%){Colors.END}")
                else:
                    print(f"   {Colors.RED}Error en análisis{Colors.END}")

        else:
            print(f"{Colors.RED}Error: {response.status_code}{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")


def test_model_info():
    """Obtiene información del modelo"""
    print_header("INFORMACIÓN DEL MODELO")

    try:
        response = requests.get(f"{BASE_URL}/api/model-info")

        if response.status_code == 200:
            info = response.json()
            print(f"Modelo: {info.get('model_name', 'Unknown')}")
            print(f"Tarea: {info.get('task', 'Unknown')}")
            print(f"Framework: {info.get('framework', 'Unknown')}")
            print(f"Dispositivo: {info.get('device', 'Unknown')}")
        else:
            print(f"{Colors.RED}Error obteniendo información{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")


def test_statistics():
    """Obtiene estadísticas del servicio"""
    print_header("ESTADÍSTICAS DEL SERVICIO")

    try:
        response = requests.get(f"{BASE_URL}/api/stats")

        if response.status_code == 200:
            stats = response.json()

            if stats.get('total_analyzed', 0) == 0:
                print(f"{Colors.YELLOW}No hay estadísticas aún (ningún análisis realizado){Colors.END}")
            else:
                print(f"Total analizado: {stats.get('total_analyzed', 0)}")
                print(f"Resultados válidos: {stats.get('valid_results', 0)}")
                print(f"Errores: {stats.get('errors', 0)}")

                if 'sentiments' in stats:
                    print(f"\nDistribución de sentimientos:")
                    print(f"  Positivos: {stats['sentiments']['positive']} ({stats['percentages']['positive']:.1f}%)")
                    print(f"  Negativos: {stats['sentiments']['negative']} ({stats['percentages']['negative']:.1f}%)")
                    print(f"  Neutrales: {stats['sentiments']['neutral']} ({stats['percentages']['neutral']:.1f}%)")

                print(f"\nPromedios:")
                print(f"  Confianza: {stats.get('average_confidence', 0) * 100:.1f}%")
                print(f"  Estrellas: {stats.get('average_stars', 0):.1f}")
                print(f"  Tiempo de procesamiento: {stats.get('average_processing_time', 0):.3f}s")
        else:
            print(f"{Colors.RED}Error obteniendo estadísticas{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")


def main():
    """Función principal de pruebas"""
    print(f"{Colors.BOLD}{Colors.PURPLE}")
    print("╔════════════════════════════════════════════════╗")
    print("║     🎭 PRUEBAS DEL API DE SENTIMIENTOS 🎭      ║")
    print("╚════════════════════════════════════════════════╝")
    print(f"{Colors.END}")

    # Verificar que el servidor esté corriendo
    if not test_health():
        return

    # Menú de pruebas
    while True:
        print(f"\n{Colors.BOLD}Selecciona una prueba:{Colors.END}")
        print("1. Análisis individual")
        print("2. Análisis por lotes")
        print("3. Información del modelo")
        print("4. Estadísticas del servicio")
        print("5. Ejecutar todas las pruebas")
        print("0. Salir")

        try:
            opcion = input(f"\n{Colors.PURPLE}Opción: {Colors.END}")

            if opcion == '1':
                test_single_analysis()
            elif opcion == '2':
                test_batch_analysis()
            elif opcion == '3':
                test_model_info()
            elif opcion == '4':
                test_statistics()
            elif opcion == '5':
                test_single_analysis()
                test_batch_analysis()
                test_model_info()
                test_statistics()
            elif opcion == '0':
                print(f"\n{Colors.GREEN}¡Hasta luego! 👋{Colors.END}")
                break
            else:
                print(f"{Colors.YELLOW}Opción no válida{Colors.END}")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Interrumpido por el usuario{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.END}")


if __name__ == "__main__":
    main()