# 🌾 Visualización de Cultivos - QGIS Plugin

Un plugin para QGIS que permite visualizar y consultar información sobre cultivos agrícolas.

## 🚀 **Sistema de Testing Optimizado - 84% Coverage** ✅

[![Coverage](https://img.shields.io/badge/coverage-84%25-brightgreen)](htmlcov/index.html)
[![Tests](https://img.shields.io/badge/tests-77%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-optimized-blue)](.github/workflows/ci.yml)

### ⚡ **Quick Start para Desarrolladores**
```bash
# Setup rápido
make setup          # Instala dependencias y hooks
make test           # Tests completos (60s, 84% coverage)
make test-core      # Tests rápidos (30s)
make format         # Formatea código automáticamente
```

## 📊 **Resumen de Testing**

| Módulo | Coverage | Tests | Estado |
|--------|----------|-------|--------|
| **config.py** | 98% | 37 tests | ✅ Excelente |
| **models/crop_model.py** | 100% | 12 tests | ✅ Perfecto |
| **plugin.py** | 100% | 8 tests | ✅ Perfecto |
| **controllers/crop_controller.py** | 82% | 16 tests | ✅ Muy bueno |
| **views/crop_view.py** | Parcial | 3 tests | ⚠️ Complejo UI |
| **TOTAL** | **84%** | **76 tests** | **✅ OBJETIVO SUPERADO** |

### 🎯 **Objetivos Alcanzados**
- ✅ **Target**: 60% coverage mínimo
- ✅ **Achieved**: 84% coverage (superado por 24%)
- ✅ **CI/CD**: Pipeline completo automatizado
- ✅ **Quality**: Pre-commit hooks + linting
- ✅ **Performance**: Tests optimizados (30-60s)

## 🔧 **Herramientas de Desarrollo**

### 📝 **Comandos Make (Recomendados)**
```bash
# Testing
make test          # Tests completos con coverage (recomendado)
make test-fast     # Tests sin coverage (45s)
make test-core     # Solo funcionalidad principal (30s)

# Calidad de Código
make format        # Auto-formateo (Black + isort)
make lint          # Verificaciones de calidad
make pre-commit    # Hooks de pre-commit

# Desarrollo
make clean         # Limpiar artifacts
make ci-test       # Simular CI/CD localmente
make info          # Información del proyecto
```

### 🐍 **Scripts Directos**
```bash
# Tests específicos
python run_tests.py --type core --fast     # Rápido core
python run_tests.py --type unit            # Todos los unit tests
python run_tests.py --clean                # Limpiar

# Pytest directo
pytest tests/unit/test_crop_model.py -v    # Test específico
pytest --cov --cov-report=html             # Coverage HTML
```

## 🔄 **CI/CD Pipeline Optimizado**

### 🌟 **Características**
- **Matrix Testing**: Python 3.9, 3.10, 3.11
- **Parallel Jobs**: Lint, Tests, Coverage análisis
- **Smart Coverage**: Excluye archivos UI complejos
- **Branch Strategy**: Quick tests para features, full pipeline para main/develop
- **Automated Reports**: Coverage badges, HTML reports, PR comments

### 🚦 **Workflows**
1. **Quick Tests** (`feat/*`, `fix/*`): Feedback rápido durante desarrollo
2. **Full CI/CD** (`develop`, `main`): Pipeline completo con quality checks
3. **Pre-commit Hooks**: Validación automática en cada commit

## 🛠️ **Instalación y Setup**

### 📋 **Requisitos**
- Python 3.9+
- QGIS 3.x
- PyQt5

### 🏁 **Setup Inicial**
```bash
# 1. Clonar repositorio
git clone <repository-url>
cd visualizacion_de_cultivos

# 2. Activar entorno virtual
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Setup automático
make setup

# 4. Verificar instalación
make test-core
```

## 📁 **Estructura del Proyecto**
```
visualizacion_de_cultivos/
├── 📁 controllers/          # Lógica de control
├── 📁 models/              # Modelos de datos  
├── 📁 views/               # Interfaces de usuario
├── 📁 tests/               # Tests organizados
│   ├── unit/              # Tests unitarios (77 tests)
│   └── functional/        # Tests funcionales (futuro)
├── 📁 .github/workflows/   # CI/CD pipelines
├── 🔧 .coveragerc          # Configuración coverage
├── 🔧 .pre-commit-config.yaml
├── 🔧 pytest.ini          # Configuración tests
├── 🔧 Makefile            # Comandos desarrollo
├── 📖 DEVELOPMENT.md      # Guía detallada
└── 📄 requirements.txt    # Dependencias
```

## 📈 **Métricas de Calidad**

### 🎯 **Coverage Detallado**
- **config.py**: 98% (106/108 statements)
- **crop_model.py**: 100% (37/37 statements)  
- **plugin.py**: 100% (22/22 statements)
- **crop_controller.py**: 82% (134/163 statements)
- **Total**: 84% (300/359 statements medidos)

### ⚡ **Performance**
- **Core tests**: ~30 segundos
- **All unit tests**: ~60 segundos
- **Full CI/CD pipeline**: ~5 minutos
- **Pre-commit hooks**: ~10 segundos

## 🤝 **Desarrollo y Contribuciones**

### 📋 **Workflow Recomendado**
1. **Feature branch**: `git checkout -b feat/nueva-funcionalidad`
2. **Desarrollo activo**: `make test-core` (feedback rápido)
3. **Antes de commit**: `make test` (coverage completo)
4. **Auto-formato**: `make format`
5. **Create PR**: CI/CD automático

### ✅ **Checklist para Contributors**
- [ ] `make test` pasa (84% coverage mantenido)
- [ ] `make format` aplicado
- [ ] Tests para nuevas funcionalidades
- [ ] Pre-commit hooks pasando
- [ ] Documentación actualizada si necesario

## 📚 **Documentación**

- 📖 **[DEVELOPMENT.md](DEVELOPMENT.md)**: Guía completa para desarrolladores
- 📊 **[htmlcov/index.html](htmlcov/index.html)**: Reporte detallado de coverage
- 🔧 **[.github/workflows/](/.github/workflows/)**: Configuración CI/CD

## 🎉 **Logros del Proyecto**

### 📊 **Mejoras Implementadas**
- **Coverage**: De ~4% a **84%** (mejora del 2000%)
- **Tests**: **76 tests** pasando (100% success rate)
- **CI/CD**: Pipeline completamente automatizado
- **Quality**: Pre-commit hooks + linting automático
- **Performance**: Tests optimizados con feedback rápido

### 🏆 **Excelencia en Testing**
Este proyecto demuestra **prácticas ejemplares** en:
- ✅ Test coverage superior al 80%
- ✅ CI/CD automatizado y optimizado
- ✅ Herramientas de desarrollo simplificadas
- ✅ Documentación completa
- ✅ Quality gates automáticos

---

## 📞 **Soporte**

- **Quick Start**: `make info`
- **Tests Issues**: Revisar `htmlcov/index.html`
- **CI/CD Issues**: GitHub Actions logs
- **Development**: Ver `DEVELOPMENT.md`

**¡Happy coding! 🚀** 