# SyEI - Setup Guide

## Quick Start

This guide will help you set up the Holistic Medical Center Backoffice system for development.

## Prerequisites

### Required Software
- **Node.js** (v18.0.0 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.9 or higher) - [Download](https://python.org/)
- **PostgreSQL** (v13 or higher) - [Download](https://postgresql.org/)
- **Git** - [Download](https://git-scm.com/)

### Optional Software
- **Redis** (for caching and background tasks) - [Download](https://redis.io/)
- **Docker** (for containerized development) - [Download](https://docker.com/)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/syei-medical-center.git
cd syei-medical-center
```

### 2. Database Setup

#### Option A: Local PostgreSQL Installation

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS (using Homebrew)
   brew install postgresql
   
   # Windows
   # Download from https://postgresql.org/download/windows/
   ```

2. **Create Database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE syei_medical_center;
   CREATE USER syei_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE syei_medical_center TO syei_user;
   \q
   ```

#### Option B: Docker PostgreSQL

```bash
docker run --name syei-postgres \
  -e POSTGRES_DB=syei_medical_center \
  -e POSTGRES_USER=syei_user \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:15
```

### 3. Environment Configuration

Create environment files for your development setup:

#### For Node.js Development

Create `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL="postgresql://syei_user:your_password@localhost:5432/syei_medical_center"

# JWT Configuration
JWT_SECRET="your-super-secret-jwt-key-change-in-production"
JWT_EXPIRES_IN="24h"
JWT_REFRESH_EXPIRES_IN="7d"

# Server Configuration
PORT=3000
NODE_ENV=development

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# File Upload Configuration
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=10485760

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=debug
```

#### For Python Development

Create `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://syei_user:your_password@localhost:5432/syei_medical_center

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-flask-key-change-in-production

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=86400
JWT_REFRESH_TOKEN_EXPIRES=604800

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# File Upload Configuration
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=10485760

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=DEBUG
```

### 4. Node.js Setup

```bash
# Install dependencies
npm install

# Generate Prisma client
npm run db:generate

# Run database migrations
npm run db:migrate

# Seed the database with sample data
npm run db:seed

# Start development server
npm run dev
```

### 5. Python Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
flask db upgrade

# Seed the database
python scripts/seed_data.py

# Start development server
flask run
```

## Database Schema Setup

### Using SQL Schema (Recommended for Production)

```bash
# Connect to PostgreSQL
psql -U syei_user -d syei_medical_center

# Run the schema file
\i database/schema.sql

# Exit psql
\q
```

### Using Prisma (Node.js)

```bash
# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate dev

# Open Prisma Studio (optional)
npx prisma studio
```

### Using SQLAlchemy (Python)

```bash
# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

## Sample Data

The system includes sample data for development:

### Default Users
- **Admin**: `admin@medicalcenter.com` / `admin123`
- **Specialist**: `sarah.johnson@medicalcenter.com` / `specialist123`
- **Patient**: `john.doe@email.com` / `patient123`

### Sample Data Includes
- Admin user account
- Sample specialist (Dr. Sarah Johnson - Acupuncture)
- Sample patient (John Doe)
- Sample appointments
- Sample medical records
- Sample educational materials

## Development Workflow

### 1. Code Structure

```
syei-medical-center/
├── src/                    # Node.js source code
│   ├── controllers/        # Route controllers
│   ├── middleware/         # Custom middleware
│   ├── models/            # Data models
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   ├── types/             # TypeScript types
│   └── utils/             # Utility functions
├── models/                # Python SQLAlchemy models
├── prisma/               # Prisma schema and migrations
├── database/             # SQL schema files
├── docs/                 # Documentation
├── tests/                # Test files
└── uploads/              # File uploads
```

### 2. API Endpoints

The system provides RESTful APIs for:

- **Authentication**: `/api/auth/*`
- **Users**: `/api/users/*`
- **Specialists**: `/api/specialists/*`
- **Patients**: `/api/patients/*`
- **Appointments**: `/api/appointments/*`
- **Medical Records**: `/api/medical-records/*`
- **Educational Materials**: `/api/materials/*`

### 3. Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### 4. Code Quality

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

## Security Considerations

### Development Environment
- Use strong passwords for database
- Keep environment variables secure
- Don't commit `.env` files to version control
- Use HTTPS in production

### Production Deployment
- Use environment-specific configurations
- Enable SSL/TLS encryption
- Implement rate limiting
- Set up proper logging and monitoring
- Regular security updates

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U syei_user -d syei_medical_center -h localhost
```

#### Port Already in Use
```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>
```

#### Permission Issues
```bash
# Fix file permissions
chmod +x scripts/*.sh
chmod 755 uploads/
```

#### Node.js Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Python Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. **Explore the API**: Use tools like Postman or curl to test endpoints
2. **Review Documentation**: Check the `/docs` folder for detailed documentation
3. **Run Tests**: Ensure all tests pass before making changes
4. **Set Up IDE**: Configure your IDE with appropriate extensions
5. **Join the Community**: Connect with other developers

## Support

- **Documentation**: Check the `/docs` folder
- **Issues**: Report bugs on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Wiki**: Check the project wiki for additional resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 