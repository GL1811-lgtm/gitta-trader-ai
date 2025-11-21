#!/bin/bash

# Gitta Trader AI - GCP VM Setup Script
# This script automates the deployment on a fresh GCP e2-micro instance

set -e  # Exit on any error

echo "========================================="
echo "Gitta Trader AI - GCP Deployment Setup"
echo "========================================="

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose (standalone)
echo "📦 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
echo "✅ Verifying installations..."
docker --version
docker-compose --version

# Clone repository (if not already cloned)
if [ ! -d "gitta-trader-ai" ]; then
    echo "📥 Cloning repository..."
    read -p "Enter your Git repository URL: " REPO_URL
    git clone $REPO_URL gitta-trader-ai
else
    echo "📂 Repository already exists, pulling latest changes..."
    cd gitta-trader-ai
    git pull
    cd ..
fi

# Navigate to project directory
cd gitta-trader-ai

# Create .env file from template
echo "⚙️  Setting up environment variables..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📝 Created .env file from .env.example"
        echo "⚠️  IMPORTANT: Edit .env file with your API keys before starting services"
        echo "   Run: nano .env"
    else
        echo "❌ .env.example not found. Please create .env manually."
    fi
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p backend/data/inbox
mkdir -p backend/data/results
mkdir -p backend/data/reports

# Set proper permissions
sudo chown -R $USER:$USER .

# Configure firewall rules
echo "🔥 Configuring firewall..."
echo "⚠️  You need to configure GCP firewall rules manually:"
echo "   1. Go to GCP Console > VPC Network > Firewall"
echo "   2. Create rule: Allow TCP ports 80, 443, 5001, 5173"
echo "   3. Source IP ranges: 0.0.0.0/0 (or restrict as needed)"

# Display next steps
echo ""
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit environment variables:"
echo "   nano .env"
echo ""
echo "2. Add your API keys (GROQ_API_KEY, YOUTUBE_API_KEY, etc.)"
echo ""
echo "3. Start the application:"
echo "   docker-compose up -d"
echo ""
echo "4. Check status:"
echo "   docker-compose ps"
echo "   docker-compose logs -f"
echo ""
echo "5. Access the application:"
echo "   Frontend: http://YOUR_VM_IP:5173"
echo "   Backend API: http://YOUR_VM_IP:5001"
echo "   Grafana: http://YOUR_VM_IP:3001"
echo ""
echo "6. To stop:"
echo "   docker-compose down"
echo ""
echo "========================================="
