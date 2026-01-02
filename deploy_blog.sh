#!/bin/bash
# deploy_blog.sh - Deploy blog completo a mytechzone.dev

set -euo pipefail

# Configuración
SERVER="mytechzone"
REMOTE_WEB_DIR="/home/mytechzone/n8n-lab/website/html"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  DESPLEGANDO BLOG TÉCNICO${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# 1. Verificar conexión SSH
echo -e "${YELLOW}➤${NC} Verificando conexión al servidor..."
if ! ssh "$SERVER" "echo 'Conexión OK' > /dev/null"; then
    echo -e "${RED}✗${NC} No se puede conectar a $SERVER"
    exit 1
fi
echo -e "${GREEN}✓${NC} Conexión SSH OK"
echo ""

# 2. Desplegar index.html actualizado
echo -e "${YELLOW}➤${NC} Desplegando index.html con enlace al blog..."
scp website/index.html "$SERVER:$REMOTE_WEB_DIR/"
echo -e "${GREEN}✓${NC} index.html actualizado"
echo ""

# 3. Crear directorio del blog en el servidor
echo -e "${YELLOW}➤${NC} Creando estructura de directorios..."
ssh "$SERVER" "mkdir -p $REMOTE_WEB_DIR/blog/posts"
echo -e "${GREEN}✓${NC} Directorios creados"
echo ""

# 4. Desplegar blog index
echo -e "${YELLOW}➤${NC} Desplegando blog index..."
scp blog/index.html "$SERVER:$REMOTE_WEB_DIR/blog/"
echo -e "${GREEN}✓${NC} Blog index desplegado"
echo ""

# 5. Desplegar posts
echo -e "${YELLOW}➤${NC} Desplegando posts..."
scp blog/posts/*.html "$SERVER:$REMOTE_WEB_DIR/blog/posts/" 2>/dev/null || true
echo -e "${GREEN}✓${NC} Posts desplegados"
echo ""

# 6. Verificar deployment
echo -e "${YELLOW}➤${NC} Verificando archivos desplegados..."
ssh "$SERVER" "ls -lh $REMOTE_WEB_DIR/blog/ && echo '---' && ls -lh $REMOTE_WEB_DIR/blog/posts/"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ DEPLOYMENT COMPLETADO${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "🌐 URLs desplegadas:"
echo -e "   • Sitio principal: ${BLUE}https://mytechzone.dev/${NC}"
echo -e "   • Blog:            ${BLUE}https://mytechzone.dev/blog/${NC}"
echo -e "   • Posts:           ${BLUE}https://mytechzone.dev/blog/posts/${NC}"
echo ""
echo -e "📝 Posts publicados:"
echo -e "   1. De Notebook a Servidor: Mi Home Lab DevOps (Jul 15, 2024)"
echo -e "   2. Migración Masiva GP2 a GP3: Ahorrando Costos en AWS (Jul 28, 2024)"
echo -e "   3. Caso Real: Debugging con Asistencia de IA (Dec 12, 2024)"
echo ""
echo -e "🎯 Próximos pasos:"
echo -e "   • Escribe más posts (18 planeados en total)"
echo -e "   • Comparte en LinkedIn cuando publiques nuevos artículos"
echo -e "   • Considera agregar RSS feed"
echo ""

