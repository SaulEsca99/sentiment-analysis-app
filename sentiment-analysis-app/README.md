# Crear el archivo README.md
cat > README.md << 'EOL'
# 🎭 Sistema de Análisis de Sentimientos

Sistema de análisis de sentimientos usando Machine Learning y NLP.

## 🚀 Proyecto en Desarrollo

- **Autor**: Saúl Escamilla Lazcano
- **Inicio**: $(date +'%d/%m/%Y')
- **Status**: En desarrollo 🔨

## 📋 Descripción

Este proyecto analiza el sentimiento de textos en español e inglés utilizando 
modelos de Deep Learning (BERT) para clasificar opiniones como positivas, 
negativas o neutrales.

## 🛠️ Tecnologías

- Python 3.9+
- Flask (Backend)
- React (Frontend) - Próximamente
- Transformers (Hugging Face)
- Machine Learning con PyTorch

## 📊 Características Planeadas

- [ ] API REST para análisis de texto
- [ ] Análisis en tiempo real
- [ ] Procesamiento por lotes
- [ ] Dashboard interactivo
- [ ] Soporte multiidioma
- [ ] Exportación de resultados

## 🏗️ Instalación

```bash
# Clonar repositorio
git clone [tu-repo-url]

# Navegar al directorio
cd sentiment-analysis-app

# Activar entorno virtual (si usas conda)
conda activate sentiment-env

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python src/main.py
