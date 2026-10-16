#!/bin/sh
# Build de Cloudflare Pages: copia solo los archivos públicos a dist/
set -e
rm -rf dist && mkdir -p dist
cp ./*.html sitemap.xml robots.txt dist/
cp -r assets dist/
cp cf/_headers dist/_headers
echo "Sitio listo en dist/ ($(ls dist | wc -l) entradas)"
