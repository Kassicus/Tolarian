# Knowledge Base Application

A centralized, searchable knowledge base application built with Python/Flask/Jinja2 to organize development team resources, including project templates, documentation, guides, and external links.

## Features

- 🔍 **Full-text search** across all content types
- 📝 **Markdown support** for rich content creation
- 🏷️ **Tagging system** for content organization
- 📁 **Hierarchical categories** for structured navigation
- 🔐 **User authentication** with role-based access control
- 📊 **Version control** for document history
- ☁️ **Cloud-native** deployment on Vercel with Supabase
- 📱 **Responsive design** with Bootstrap 5

## Tech Stack

- **Backend**: Flask 3.0+ (Python)
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Authentication**: Supabase Auth
- **Hosting**: Vercel (Serverless)
- **Frontend**: Jinja2, Bootstrap 5, Alpine.js
- **Search**: PostgreSQL Full-Text Search

## Project Structure

```
Tolarian/
├── api/                    # Vercel serverless functions
│   └── index.py           # Main Flask entry point
├── app/                   # Application code
│   ├── __init__.py       # Application factory
│   ├── config.py         # Configuration settings
│   ├── models/           # Database models
│   ├── blueprints/       # Flask blueprints
│   ├── templates/        # Jinja2 templates
│   ├── static/           # CSS, JS, images
│   ├── utils/            # Utility functions
│   └── services/         # Business logic
├── migrations/           # Database migrations
├── tests/               # Test suite
├── scripts/             # Utility scripts
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
├── .env.example        # Environment variables template
└── run.py              # Local development server
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+ (for Vercel CLI)
- Supabase account
- Vercel account (for deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Tolarian.git
   cd Tolarian
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   Edit `.env.local` with your Supabase credentials:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_ANON_KEY`: Your Supabase anonymous key
   - `SUPABASE_SERVICE_KEY`: Your Supabase service key
   - `DATABASE_URL`: Direct PostgreSQL connection string
   - `SECRET_KEY`: A secure secret key for Flask

5. **Set up Supabase**
   - Create a new Supabase project
   - Run the database setup scripts (see `scripts/setup_supabase.py`)
   - Configure authentication providers if needed

6. **Run the application**
   ```bash
   python run.py
   ```
   The app will be available at `http://localhost:5000`

### Using Supabase Local Development

For local Supabase development:

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize local Supabase
supabase init
supabase start

# Set LOCAL_SUPABASE=true in your .env.local
```

## Deployment

### Deploy to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Configure environment variables in Vercel**
   ```bash
   vercel env add SUPABASE_URL
   vercel env add SUPABASE_ANON_KEY
   vercel env add SUPABASE_SERVICE_KEY
   vercel env add DATABASE_URL
   vercel env add SECRET_KEY
   ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

## Development Workflow

### Sprint 1: Foundation (Completed ✅)
- [x] Flask application setup
- [x] Supabase configuration
- [x] Basic templates with Bootstrap
- [x] SQLAlchemy models
- [x] Vercel deployment configuration

### Sprint 2: Authentication (Next)
- [ ] Supabase Auth integration
- [ ] User registration/login
- [ ] Social OAuth (Google, GitHub)
- [ ] Role-based access control
- [ ] Magic link authentication

### Sprint 3: Content Management
- [ ] CRUD operations for content
- [ ] Markdown editor with preview
- [ ] File upload to Supabase Storage
- [ ] Version control system
- [ ] Tagging functionality

### Sprint 4: Search Implementation
- [ ] PostgreSQL full-text search
- [ ] Search filters and facets
- [ ] Search suggestions
- [ ] Result ranking

### Sprint 5: Organization Features
- [ ] Category management
- [ ] Template library
- [ ] Link validation
- [ ] Related content
- [ ] Navigation breadcrumbs

### Sprint 6: Polish & Optimization
- [ ] Performance optimization
- [ ] Edge caching
- [ ] Export functionality
- [ ] Analytics dashboard
- [ ] Production deployment

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

## API Documentation

The API documentation will be available at `/api/v1/docs` once implemented.

### Key Endpoints (Planned)

- `GET /api/v1/content` - List content
- `POST /api/v1/content` - Create content
- `GET /api/v1/search` - Search content
- `GET /api/v1/categories` - List categories
- `GET /api/v1/tags` - List tags

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_ANON_KEY` | Supabase anonymous key | Yes |
| `SUPABASE_SERVICE_KEY` | Supabase service key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `FLASK_ENV` | Flask environment (development/production) | No |
| `LOCAL_SUPABASE` | Use local Supabase instance | No |

## Security

- All passwords are hashed using bcrypt
- CSRF protection enabled on all forms
- SQL injection prevention via SQLAlchemy ORM
- XSS protection through content sanitization
- Row Level Security (RLS) in Supabase
- Secure session management

## License

This project is proprietary and confidential.

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Contact the development team via Slack (#knowledge-base)

## Acknowledgments

- Flask community for the excellent framework
- Supabase team for the amazing backend platform
- Vercel for serverless hosting
- Bootstrap team for the UI framework

---

**Version**: 1.0.0
**Status**: Sprint 1 Complete - Foundation Setup ✅
**Next**: Sprint 2 - Authentication & Authorization
