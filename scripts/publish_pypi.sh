#!/usr/bin/env bash
# Publica el paquete ssigma en PyPI.
# Antes de publicar: actualizar version en pyproject.toml (y en ssigma/cli.py --version si aplica).
#
# Uso:
#   ./scripts/publish_pypi.sh           # sube a Test PyPI (para pruebas)
#   ./scripts/publish_pypi.sh --pypi     # sube a PyPI real
#
# Requisitos: crear un venv y pip install build twine, o:
#   pipx run build / pipx run twine (si no quieres venv).
# Para PyPI real necesitas token o usuario/contraseña (configurar en ~/.pypirc o env).

set -e
cd "$(dirname "$0")/.."

echo "=== Limpiando dist/ ==="
rm -rf dist/ build/
rm -rf ssigma.egg-info 2>/dev/null || true

echo "=== Construyendo el paquete ==="
if [[ -n "$VIRTUAL_ENV" ]]; then
    pip install -q -U build twine
    PYTHON="python"
else
    PYTHON="python3"
    $PYTHON -m pip install --user -q -U build twine 2>/dev/null || true
fi
$PYTHON -m build

echo "=== Comprobando el paquete con twine ==="
$PYTHON -m twine check dist/*

if [[ "$1" == "--pypi" ]]; then
    echo "=== Subiendo a PyPI (producción) ==="
    $PYTHON -m twine upload dist/*
else
    echo "=== Subiendo a Test PyPI (pruebas) ==="
    echo "  Para publicar en PyPI real ejecuta: $0 --pypi"
    $PYTHON -m twine upload --repository testpypi dist/*
fi

echo "=== Hecho ==="
