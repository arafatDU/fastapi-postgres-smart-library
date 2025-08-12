# Docker Commands for FastAPI Smart Library

## 🏗️ Architecture
```
nginx (Port 80) → Reverse Proxy
├── /api/users  → user-service:8081
├── /api/books  → book-service:8082
└── /api/loans  → loan-service:8083
```

## 🚀 Essential Commands

### Start All Services
```bash
docker-compose up -d
```

### Start with Build (rebuild images)
```bash
docker-compose up -d --build
```

### Stop All Services
```bash
docker-compose down
```

### Clean Reset (remove volumes)
```bash
docker-compose down -v
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Specific Services
```bash
docker-compose restart user-service
docker-compose restart book-service  
docker-compose restart loan-service
docker-compose restart nginx
```

## 🌐 Access Points
- **Main Gateway:** http://localhost/
- **User Service:** http://localhost/api/users
- **Book Service:** http://localhost/api/books
- **Loan Service:** http://localhost/api/loans
- **Health Check:** http://localhost/health
