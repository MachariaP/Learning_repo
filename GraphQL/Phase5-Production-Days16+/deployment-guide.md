# GraphQL API Deployment Guide

This guide provides step-by-step instructions for deploying your GraphQL API to production.

---

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Tested all queries and mutations locally
- [ ] Set up environment variables
- [ ] Configured database connection
- [ ] Disabled introspection in production
- [ ] Disabled playground in production
- [ ] Implemented rate limiting
- [ ] Added error logging
- [ ] Created database backups
- [ ] Set up monitoring
- [ ] Configured CORS properly
- [ ] Added health check endpoint

---

## Option 1: Deploy to Heroku

### Step 1: Prepare Your Application

```bash
# Ensure package.json has start script
{
  "scripts": {
    "start": "node server.js"
  }
}

# Create Procfile
echo "web: node server.js" > Procfile

# Ensure Node version is specified in package.json
{
  "engines": {
    "node": "18.x"
  }
}
```

### Step 2: Create Heroku App

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create my-graphql-api

# Add MongoDB (if needed)
heroku addons:create mongolab:sandbox
```

### Step 3: Configure Environment

```bash
# Set environment variables
heroku config:set NODE_ENV=production
heroku config:set JWT_SECRET="your-secret-key"
heroku config:set ALLOWED_ORIGINS="https://your-frontend.com"
```

### Step 4: Deploy

```bash
# Push to Heroku
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open
```

---

## Option 2: Deploy to Railway

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
railway login
```

### Step 2: Initialize and Deploy

```bash
# Initialize Railway project
railway init

# Add environment variables
railway variables set NODE_ENV=production
railway variables set JWT_SECRET=your-secret-key

# Deploy
railway up

# View logs
railway logs
```

---

## Option 3: Deploy to AWS EC2

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Launch Instance (Ubuntu 22.04 LTS)
3. Configure security group:
   - HTTP (80)
   - HTTPS (443)
   - SSH (22)
   - Custom TCP (4000) - for GraphQL

### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install MongoDB (optional)
# Follow MongoDB installation guide

# Install PM2
sudo npm install -g pm2

# Install Git
sudo apt install git -y
```

### Step 3: Deploy Application

```bash
# Clone repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Install dependencies
npm install --production

# Create .env file
nano .env
# Add your environment variables

# Start with PM2
pm2 start server.js --name graphql-api

# Setup PM2 to start on boot
pm2 startup
pm2 save

# View logs
pm2 logs graphql-api
```

### Step 4: Setup Nginx (Optional)

```bash
# Install Nginx
sudo apt install nginx -y

# Configure Nginx
sudo nano /etc/nginx/sites-available/graphql

# Add configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/graphql /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Option 4: Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 4000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:4000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "server.js"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "4000:4000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET=${JWT_SECRET}
    restart: unless-stopped
    depends_on:
      - mongo
      - redis

  mongo:
    image: mongo:6
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  mongo-data:
```

### Step 3: Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Post-Deployment Tasks

### 1. Verify Deployment

```bash
# Test health endpoint
curl https://your-api.com/health

# Test GraphQL endpoint
curl -X POST https://your-api.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __typename }"}'
```

### 2. Set Up Monitoring

```bash
# Add health check monitoring
# Options: UptimeRobot, Pingdom, StatusCake

# Set up error tracking
# Options: Sentry, Rollbar, Bugsnag

# Set up performance monitoring
# Options: New Relic, DataDog, Apollo Studio
```

### 3. Configure SSL/TLS

```bash
# For Nginx with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo certbot renew --dry-run
```

### 4. Set Up Backups

```bash
# MongoDB backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mongodump --uri="your-connection-string" --out="/backups/backup_$TIMESTAMP"

# Add to crontab for daily backups
0 2 * * * /path/to/backup-script.sh
```

---

## Monitoring and Maintenance

### Health Check Endpoint

Add to your server:

```javascript
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});
```

### Logging

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Use in your code
logger.info('Server started');
logger.error('Error occurred', { error });
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Fails**
- Check DATABASE_URL is correctly set
- Verify firewall rules allow database connections
- Test database connectivity separately

**2. High Memory Usage**
- Check for memory leaks
- Implement connection pooling
- Use DataLoader for batching

**3. Slow Queries**
- Add database indexes
- Implement caching
- Use DataLoader

**4. Rate Limiting Issues**
- Adjust rate limit configuration
- Implement per-user limits
- Use Redis for distributed rate limiting

---

## Security Best Practices

1. **Use HTTPS** - Always use SSL/TLS in production
2. **Validate Input** - Sanitize all user inputs
3. **Rate Limiting** - Prevent abuse with rate limits
4. **Query Complexity** - Limit complex queries
5. **Authentication** - Use JWT or OAuth
6. **Secrets Management** - Use environment variables
7. **Regular Updates** - Keep dependencies updated
8. **CORS** - Configure properly for your frontend

---

## Scaling Strategies

### Horizontal Scaling

```bash
# Use a load balancer (Nginx, HAProxy, AWS ELB)
# Run multiple instances of your API
# Use Redis for shared session storage
```

### Vertical Scaling

```bash
# Increase server resources (RAM, CPU)
# Optimize database queries
# Implement caching
```

### Database Scaling

```bash
# Use read replicas
# Implement sharding
# Use connection pooling
```

---

## Rollback Plan

If deployment fails:

```bash
# Heroku
heroku releases
heroku rollback v123

# Railway
railway rollback

# Docker
docker-compose down
git checkout previous-version
docker-compose up -d

# AWS/Manual
pm2 stop graphql-api
git checkout previous-version
npm install
pm2 restart graphql-api
```

---

## Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "my-graphql-api"
        heroku_email: "your-email@example.com"
```

---

## Resources

- [Heroku Documentation](https://devcenter.heroku.com/)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PM2 Documentation](https://pm2.keymetrics.io/)

---

## Support

If you encounter issues:
1. Check application logs
2. Verify environment variables
3. Test database connectivity
4. Check server resources
5. Review error tracking (Sentry, etc.)

Good luck with your deployment! 🚀
