#!/bin/bash

# Deployment Verification Script
# Run this after deployment to verify all services are working

echo "========================================="
echo "Gitta Trader AI - Deployment Verification"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get VM IP (or use localhost for local testing)
if [ -z "$1" ]; then
    echo -e "${YELLOW}No IP provided, using localhost${NC}"
    VM_IP="localhost"
else
    VM_IP="$1"
fi

echo "Testing deployment at: $VM_IP"
echo ""

# Test 1: Docker Services
echo "1. Checking Docker services..."
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓ Docker services are running${NC}"
else
    echo -e "${RED}✗ Docker services are not running${NC}"
    exit 1
fi
echo ""

# Test 2: Backend Health
echo "2. Checking Backend API health..."
HEALTH_RESPONSE=$(curl -s http://$VM_IP:5001/health)
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Backend API is healthy${NC}"
    echo "   Response: $HEALTH_RESPONSE"
else
    echo -e "${RED}✗ Backend API health check failed${NC}"
    echo "   Response: $HEALTH_RESPONSE"
fi
echo ""

# Test 3: Frontend
echo "3. Checking Frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:5173)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✓ Frontend is accessible (HTTP $FRONTEND_STATUS)${NC}"
else
    echo -e "${RED}✗ Frontend is not accessible (HTTP $FRONTEND_STATUS)${NC}"
fi
echo ""

# Test 4: Redis
echo "4. Checking Redis..."
if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo -e "${GREEN}✓ Redis is responding${NC}"
else
    echo -e "${RED}✗ Redis is not responding${NC}"
fi
echo ""

# Test 5: Database
echo "5. Checking Database..."
if docker-compose exec -T backend test -f /app/backend/data/gitta.db; then
    echo -e "${GREEN}✓ Database file exists${NC}"
else
    echo -e "${YELLOW}⚠ Database file not found (will be created on first run)${NC}"
fi
echo ""

# Test 6: API Endpoints
echo "6. Testing API endpoints..."

# Test stocks endpoint
STOCKS_RESPONSE=$(curl -s http://$VM_IP:5001/api/stocks)
if echo "$STOCKS_RESPONSE" | grep -q "stocks"; then
    echo -e "${GREEN}✓ /api/stocks endpoint working${NC}"
else
    echo -e "${RED}✗ /api/stocks endpoint failed${NC}"
fi

# Test system status
STATUS_RESPONSE=$(curl -s http://$VM_IP:5001/api/system/status)
if echo "$STATUS_RESPONSE" | grep -q "timestamp"; then
    echo -e "${GREEN}✓ /api/system/status endpoint working${NC}"
else
    echo -e "${RED}✗ /api/system/status endpoint failed${NC}"
fi

# Test scheduler jobs
JOBS_RESPONSE=$(curl -s http://$VM_IP:5001/api/scheduler/jobs)
if echo "$JOBS_RESPONSE" | grep -q "jobs"; then
    echo -e "${GREEN}✓ /api/scheduler/jobs endpoint working${NC}"
    echo "   Scheduled jobs:"
    echo "$JOBS_RESPONSE" | python3 -m json.tool 2>/dev/null | grep -E "name|next_run_time" | head -8
else
    echo -e "${RED}✗ /api/scheduler/jobs endpoint failed${NC}"
fi
echo ""

# Test 7: Monitoring
echo "7. Checking Monitoring services..."

# Prometheus
PROM_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:9090)
if [ "$PROM_STATUS" = "200" ]; then
    echo -e "${GREEN}✓ Prometheus is accessible${NC}"
else
    echo -e "${YELLOW}⚠ Prometheus is not accessible (HTTP $PROM_STATUS)${NC}"
fi

# Grafana
GRAFANA_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:3001)
if [ "$GRAFANA_STATUS" = "200" ] || [ "$GRAFANA_STATUS" = "302" ]; then
    echo -e "${GREEN}✓ Grafana is accessible${NC}"
else
    echo -e "${YELLOW}⚠ Grafana is not accessible (HTTP $GRAFANA_STATUS)${NC}"
fi
echo ""

# Test 8: Environment Variables
echo "8. Checking Environment Configuration..."
if docker-compose exec -T backend printenv | grep -q "GROQ_API_KEY"; then
    echo -e "${GREEN}✓ GROQ_API_KEY is set${NC}"
else
    echo -e "${YELLOW}⚠ GROQ_API_KEY not set${NC}"
fi

if docker-compose exec -T backend printenv | grep -q "YOUTUBE_API_KEY"; then
    echo -e "${GREEN}✓ YOUTUBE_API_KEY is set${NC}"
else
    echo -e "${YELLOW}⚠ YOUTUBE_API_KEY not set (optional)${NC}"
fi
echo ""

# Summary
echo "========================================="
echo "Verification Complete!"
echo "========================================="
echo ""
echo "Access your application at:"
echo "  Frontend:   http://$VM_IP:5173"
echo "  Backend:    http://$VM_IP:5001"
echo "  Grafana:    http://$VM_IP:3001 (admin/admin)"
echo "  Prometheus: http://$VM_IP:9090"
echo ""
echo "Next steps:"
echo "  1. Configure API keys in .env if not done"
echo "  2. Monitor logs: docker-compose logs -f"
echo "  3. Wait for scheduled tasks (8 AM, 5 PM)"
echo ""
