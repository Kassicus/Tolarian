# Knowledge Base Application Project Plan

## Project Overview

A centralized, searchable knowledge base application built with Python/Flask/Jinja2 to organize development team resources, including project templates, documentation, guides, and external links.

### Vision Statement
Transform a disorganized development team into a well-structured, efficient organization by providing a single source of truth for all technical knowledge and resources.

### Success Metrics
- [ ] 80% of team actively using the platform within 3 months
- [ ] 50% reduction in time spent searching for documentation
- [ ] 100% of project templates standardized and accessible
- [ ] Average search query returns relevant results in <500ms

---

## Phase 1: Planning & Architecture

### Core Features

#### Must-Have (MVP)
- [ ] Full-text search across all content types
- [ ] Content categorization (templates, documents, guides, links)
- [ ] User authentication and authorization
- [ ] Markdown support for content creation
- [ ] File upload/download capabilities
- [ ] Tagging system for content organization
- [ ] Responsive web interface

#### Nice-to-Have (Post-MVP)
- [ ] Version control for documents
- [ ] API for external integrations
- [ ] Real-time collaborative editing
- [ ] AI-powered content recommendations
- [ ] Advanced analytics dashboard
- [ ] Mobile application

### Technical Architecture

#### Technology Stack
| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Backend Framework** | Flask 3.0+ | Lightweight, flexible, excellent documentation |
| **Hosting Platform** | Vercel | Serverless, auto-scaling, great Flask support |
| **Database** | Supabase (PostgreSQL) | Managed PostgreSQL with built-in auth, real-time, and storage |
| **ORM** | SQLAlchemy 2.0+ | Powerful, flexible, great Flask integration |
| **Search Engine** | Supabase PostgreSQL FTS | Leverages Supabase's built-in full-text search |
| **Authentication** | Supabase Auth + Flask-Login | Managed auth with social logins, JWT tokens |
| **Forms** | Flask-WTF | CSRF protection, validation |
| **Migrations** | Flask-Migrate (Alembic) | Reliable schema management |
| **Frontend** | Jinja2 + Bootstrap 5 + Alpine.js | Simple, responsive, minimal JS |
| **Markdown** | Python-Markdown | Extensible, well-maintained |
| **File Storage** | Supabase Storage | Built-in S3-compatible storage with CDN |
| **Cache** | Vercel Edge Cache + KV Storage | Edge caching and serverless Redis alternative |
| **Task Queue** | Vercel Cron Jobs | Serverless scheduled functions |

#### Database Schema

```sql
-- Core Tables Structure
Users
├── id (UUID, PK)
├── email (unique)
├── password_hash
├── role (enum: admin, editor, viewer)
├── created_at
└── updated_at

Categories
├── id (UUID, PK)
├── name
├── slug
├── parent_id (self-reference)
├── icon
└── order_index

Content
├── id (UUID, PK)
├── title
├── slug
├── content_type (enum: document, template, guide, link)
├── body (text/markdown)
├── metadata (JSONB)
├── category_id (FK)
├── author_id (FK)
├── status (enum: draft, published, archived)
├── created_at
├── updated_at
└── search_vector (tsvector)

Tags
├── id (UUID, PK)
├── name
├── slug
└── color

ContentTags (M2M)
├── content_id (FK)
└── tag_id (FK)

Versions
├── id (UUID, PK)
├── content_id (FK)
├── version_number
├── changes (JSONB)
├── author_id (FK)
└── created_at

SearchIndex
├── id (UUID, PK)
├── content_id (FK)
├── search_vector (tsvector)
├── rank
└── updated_at
```

### Project Structure

```
knowledge-base/
├── api/                         # Vercel serverless functions
│   ├── index.py                 # Main Flask application
│   ├── auth.py                  # Auth endpoints
│   ├── search.py                # Search endpoints
│   └── cron/                    # Vercel cron jobs
│       ├── reindex.py           # Search reindexing
│       └── cleanup.py           # Storage cleanup
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration classes
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model (Supabase Auth integrated)
│   │   ├── content.py           # Content models
│   │   ├── search.py            # Search-related models
│   │   └── mixins.py            # Common model mixins
│   ├── blueprints/
│   │   ├── auth/                # Authentication routes
│   │   ├── main/                # Main application routes
│   │   ├── admin/               # Admin panel
│   │   ├── api/                 # RESTful API
│   │   ├── search/              # Search functionality
│   │   └── content/             # Content management
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── macros/              # Reusable Jinja2 macros
│   │   ├── auth/                # Auth templates
│   │   ├── content/             # Content templates
│   │   ├── admin/               # Admin templates
│   │   └── errors/              # Error pages
│   ├── static/                  # Static files (served via Vercel CDN)
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   └── components/
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   └── modules/
│   │   └── img/
│   ├── utils/
│   │   ├── supabase.py          # Supabase client initialization
│   │   ├── search.py            # Search utilities
│   │   ├── markdown.py          # Markdown processing
│   │   ├── validators.py        # Custom validators
│   │   └── decorators.py        # Custom decorators
│   └── services/
│       ├── content_service.py   # Business logic
│       ├── search_service.py
│       ├── storage_service.py   # Supabase storage handling
│       └── export_service.py
├── migrations/                   # Alembic migrations (run against Supabase)
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   ├── import_data.py           # Data migration scripts
│   └── setup_supabase.py        # Supabase initialization
├── public/                      # Vercel public directory
├── requirements.txt             # Python dependencies
├── vercel.json                  # Vercel configuration
├── .env.example                 # Environment variables template
├── .env.local                   # Local development env
├── .gitignore
├── README.md
└── run.py                       # Local development entry point
```

---

## Phase 2: Development Roadmap

### Sprint Overview (7-Week Timeline)

| Sprint | Focus Area | Duration | Deliverables |
|--------|-----------|----------|--------------|
| 1 | Foundation | Week 1-2 | Basic Flask app, database, migrations |
| 2 | Authentication | Week 2-3 | User system, roles, permissions |
| 3 | Content Management | Week 3-4 | CRUD, Markdown, file handling |
| 4 | Search | Week 4-5 | Full-text search, filters, indexing |
| 5 | Organization | Week 5-6 | Categories, tags, navigation |
| 6 | Polish & Deploy | Week 6-7 | UI/UX, optimization, deployment |

### Sprint 1: Foundation Setup (Week 1-2)

#### Goals
- [ ] Initialize Flask application for Vercel deployment
- [ ] Set up Supabase project and database
- [ ] Configure SQLAlchemy with Supabase PostgreSQL
- [ ] Implement Flask-Migrate with Supabase
- [ ] Create base templates
- [ ] Configure Vercel deployment

#### Tasks
```python
# Key files to create
- api/index.py             # Main Vercel function entry
- app/__init__.py          # Application factory
- app/config.py            # Configuration for Supabase
- app/utils/supabase.py    # Supabase client setup
- vercel.json              # Vercel configuration
- requirements.txt         # Python dependencies
```

#### Acceptance Criteria
- [ ] Application runs locally with `flask run`
- [ ] Successful connection to Supabase database
- [ ] Database migrations work with Supabase
- [ ] Base template renders with Bootstrap styling
- [ ] Successful deployment to Vercel
- [ ] Environment variables configured in Vercel dashboard

### Sprint 2: Authentication & Authorization (Week 2-3)

#### Goals
- [ ] Integrate Supabase Auth with Flask-Login
- [ ] Configure social logins (Google, GitHub)
- [ ] Add role-based access control using Supabase RLS
- [ ] Create user profile management
- [ ] Implement magic link authentication
- [ ] Set up JWT session management

#### Tasks
```python
# Components to build
- Supabase Auth integration
- User model synchronized with Supabase
- Social OAuth configuration
- Magic link email flow
- Row Level Security policies
- User profile pages with Supabase Storage avatars
```

#### Acceptance Criteria
- [ ] Users can sign up/login via Supabase Auth
- [ ] Social logins work (Google/GitHub)
- [ ] Magic link authentication sends emails
- [ ] RLS policies enforce access control
- [ ] JWT tokens properly validated
- [ ] User avatars upload to Supabase Storage

### Sprint 3: Content Management System (Week 3-4)

#### Goals
- [ ] Build CRUD operations for all content types
- [ ] Implement Markdown editor with live preview
- [ ] Integrate Supabase Storage for file handling
- [ ] Create version control using Supabase triggers
- [ ] Build tagging system with PostgreSQL arrays

#### Tasks
```python
# Features to implement
- Content model with Supabase tables
- Markdown editor integration
- Supabase Storage bucket setup
- Database triggers for versioning
- Tag management with PostgreSQL arrays
- Supabase Storage policies for access control
```

#### Acceptance Criteria
- [ ] Create/edit/delete content with Supabase
- [ ] Markdown preview updates in real-time
- [ ] Files upload to Supabase Storage with policies
- [ ] Version history tracked via database triggers
- [ ] Tags stored as PostgreSQL arrays with indexing
- [ ] Storage URLs properly signed and cached

### Sprint 4: Search Implementation (Week 4-5)

#### Goals
- [ ] Implement Supabase PostgreSQL full-text search
- [ ] Add search filters using Supabase views
- [ ] Create search result ranking with ts_rank
- [ ] Add search suggestions using Supabase RPC
- [ ] Implement search indexing via Vercel cron jobs

#### Tasks
```python
# Search components
- Supabase database functions for FTS
- Search vector columns with GIN indexes
- Supabase RPC functions for complex queries
- Filter UI with Supabase views
- Vercel cron job for reindexing
- Edge caching for search results
```

#### Acceptance Criteria
- [ ] Search uses Supabase FTS capabilities
- [ ] Filters work via Supabase views
- [ ] Search suggestions via RPC functions
- [ ] Results ranked by relevance
- [ ] Vercel cron job reindexes nightly
- [ ] Search results cached at edge

### Sprint 5: Organization Features (Week 5-6)

#### Goals
- [ ] Build hierarchical category system
- [ ] Create template library
- [ ] Add link management with validation
- [ ] Implement related content
- [ ] Add navigation breadcrumbs

#### Tasks
```python
# Organization features
- Category tree management
- Template preview system
- Link checker service
- Related content algorithm
- Breadcrumb generator
- Navigation menu builder
```

#### Acceptance Criteria
- [ ] Categories support nesting 3 levels deep
- [ ] Templates show preview before use
- [ ] External links validated periodically
- [ ] Related content appears on detail pages
- [ ] Breadcrumbs show current location

### Sprint 6: Polish & Deployment (Week 6-7)

#### Goals
- [ ] Configure Supabase analytics views
- [ ] Implement Vercel Edge caching
- [ ] Add export functionality with edge functions
- [ ] Optimize Vercel production deployment
- [ ] Set up Supabase backup policies

#### Tasks
```python
# Final touches
- Supabase analytics dashboard views
- Vercel Edge cache configuration
- PDF export via Vercel functions
- Production environment setup
- Supabase Point-in-Time recovery
- Monitoring with Vercel Analytics
```

#### Acceptance Criteria
- [ ] Analytics available via Supabase dashboard
- [ ] Page load time <1 second with edge caching
- [ ] Exports generate via serverless functions
- [ ] Production deployment on Vercel
- [ ] Supabase backups configured
- [ ] Vercel Analytics tracking enabled

---

## Phase 3: Implementation Details

### Search System Architecture

#### Supabase PostgreSQL Full-Text Search Setup
```sql
-- Enable full-text search in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Add search vector column to content table
ALTER TABLE content ADD COLUMN search_vector tsvector 
  GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(body, '')), 'B')
  ) STORED;

-- Create GIN index for fast searches
CREATE INDEX content_search_idx ON content USING GIN(search_vector);

-- Create search function as Supabase RPC
CREATE OR REPLACE FUNCTION search_content(
  search_query TEXT,
  result_limit INT DEFAULT 10,
  result_offset INT DEFAULT 0
)
RETURNS TABLE(
  id UUID,
  title TEXT,
  content_type TEXT,
  body TEXT,
  rank REAL,
  highlight_title TEXT,
  highlight_body TEXT
)
LANGUAGE plpgsql
AS $
BEGIN
  RETURN QUERY
  SELECT 
    c.id,
    c.title,
    c.content_type,
    c.body,
    ts_rank(c.search_vector, websearch_to_tsquery('english', search_query)) AS rank,
    ts_headline('english', c.title, websearch_to_tsquery('english', search_query)) AS highlight_title,
    ts_headline('english', c.body, websearch_to_tsquery('english', search_query), 
      'MaxWords=50, MinWords=25, StartSel=<mark>, StopSel=</mark>') AS highlight_body
  FROM content c
  WHERE c.search_vector @@ websearch_to_tsquery('english', search_query)
    AND c.status = 'published'
  ORDER BY rank DESC
  LIMIT result_limit
  OFFSET result_offset;
END;
$;

-- Create search suggestions function
CREATE OR REPLACE FUNCTION search_suggestions(
  partial_query TEXT,
  suggestion_limit INT DEFAULT 5
)
RETURNS TABLE(suggestion TEXT)
LANGUAGE plpgsql
AS $
BEGIN
  RETURN QUERY
  SELECT DISTINCT title AS suggestion
  FROM content
  WHERE title ILIKE partial_query || '%'
    AND status = 'published'
  ORDER BY title
  LIMIT suggestion_limit;
END;
$;

-- Enable Row Level Security
ALTER TABLE content ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Public content readable by all" ON content
  FOR SELECT USING (status = 'published');

CREATE POLICY "Authors can edit own content" ON content
  FOR ALL USING (auth.uid() = author_id);

CREATE POLICY "Admins can edit all content" ON content
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.role = 'admin'
    )
  );
```

### Supabase Storage Configuration

#### Storage Buckets Setup
```javascript
// Initialize Supabase Storage buckets via script
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
)

// Create storage buckets
async function setupStorage() {
  // Documents bucket
  await supabase.storage.createBucket('documents', {
    public: false,
    fileSizeLimit: 10485760, // 10MB
    allowedMimeTypes: ['application/pdf', 'application/msword', 
                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  })
  
  // Images bucket
  await supabase.storage.createBucket('images', {
    public: true,
    fileSizeLimit: 5242880, // 5MB
    allowedMimeTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  })
  
  // Templates bucket
  await supabase.storage.createBucket('templates', {
    public: false,
    fileSizeLimit: 1048576, // 1MB
    allowedMimeTypes: ['application/json', 'application/yaml', 'text/plain']
  })
  
  // User avatars bucket
  await supabase.storage.createBucket('avatars', {
    public: true,
    fileSizeLimit: 2097152, // 2MB
    allowedMimeTypes: ['image/jpeg', 'image/png'],
    transformations: {
      resize: 'cover',
      width: 200,
      height: 200
    }
  })
}
```

### Vercel Configuration

#### vercel.json
```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "FLASK_APP": "app",
    "FLASK_ENV": "production"
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 10
    },
    "api/cron/*.py": {
      "maxDuration": 60
    }
  },
  "crons": [
    {
      "path": "/api/cron/reindex",
      "schedule": "0 2 * * *"
    },
    {
      "path": "/api/cron/cleanup",
      "schedule": "0 3 * * 0"
    }
  ]
}

### Content Organization Strategy

#### Hierarchical Structure
```
Knowledge Base
├── Development
│   ├── Backend
│   │   ├── Python
│   │   ├── Node.js
│   │   └── APIs
│   ├── Frontend
│   │   ├── React
│   │   ├── Vue
│   │   └── CSS
│   └── DevOps
│       ├── Docker
│       ├── CI/CD
│       └── Monitoring
├── Project Templates
│   ├── Microservices
│   ├── Web Applications
│   └── Mobile Apps
├── Best Practices
│   ├── Code Review
│   ├── Testing
│   └── Documentation
└── External Resources
    ├── Documentation
    ├── Tools
    └── Learning
```

#### Tagging Taxonomy
```yaml
Technical Tags:
  - python
  - javascript
  - docker
  - kubernetes
  - postgresql

Project Tags:
  - frontend
  - backend
  - fullstack
  - infrastructure
  - mobile

Document Type Tags:
  - tutorial
  - reference
  - howto
  - troubleshooting
  - template

Difficulty Tags:
  - beginner
  - intermediate
  - advanced
  - expert
```

### Security Considerations

#### Authentication Security
- [ ] Passwords hashed with bcrypt (min 12 rounds)
- [ ] Session cookies httponly and secure
- [ ] CSRF protection on all forms
- [ ] Rate limiting on login attempts
- [ ] Two-factor authentication (optional)

#### Content Security
- [ ] Input sanitization for XSS prevention
- [ ] File upload restrictions (type, size)
- [ ] SQL injection prevention via ORM
- [ ] Proper authorization checks
- [ ] Audit logging for sensitive actions

#### Deployment Security
- [ ] HTTPS only with SSL certificate
- [ ] Security headers (CSP, HSTS, etc.)
- [ ] Regular dependency updates
- [ ] Database connection encryption
- [ ] Secrets in environment variables

---

## Phase 4: Testing Strategy

### Test Coverage Goals
- Unit Tests: 80% coverage
- Integration Tests: Critical paths
- E2E Tests: User workflows
- Performance Tests: Search and load

### Testing Pyramid

```
         /\
        /E2E\        5% - Critical user journeys
       /----\
      / Integ \      15% - API and database
     /--------\
    /   Unit   \     80% - Business logic
   /____________\
```

### Test Categories

#### Unit Tests
```python
# Example test structure
tests/unit/
├── test_models.py
├── test_services.py
├── test_utils.py
└── test_validators.py
```

#### Integration Tests
```python
# Key integration points
- Database operations
- Search functionality
- File upload/download
- Email sending
- Cache operations
```

#### End-to-End Tests
```python
# Critical workflows
- User registration and login
- Create and publish content
- Search and filter results
- Export documentation
- Admin management tasks
```

### Performance Benchmarks
| Operation | Target | Maximum |
|-----------|--------|---------|
| Page Load | <1s | 2s |
| Search Query | <500ms | 1s |
| File Upload (10MB) | <5s | 10s |
| Export (PDF) | <3s | 5s |
| Concurrent Users | 100 | 500 |

---

## Phase 5: Deployment & Operations

### Deployment Strategy

#### Local Development Environment
```bash
# Install Supabase CLI for local development
npm install -g supabase

# Initialize local Supabase instance
supabase init
supabase start

# Set up environment variables
cp .env.example .env.local
# Add your Supabase project URL and keys

# Install Python dependencies
pip install -r requirements.txt

# Run Flask locally
flask run

# Or use Vercel CLI for local testing
npm install -g vercel
vercel dev
```

#### Vercel Deployment Configuration
```python
# api/index.py - Main entry point for Vercel
from flask import Flask
from app import create_app
import os

# Create Flask app instance
app = create_app()

# Vercel expects a variable named 'app'
# This will be the entry point for serverless functions

# Configure for Vercel environment
if os.environ.get('VERCEL_ENV'):
    app.config['SERVER_NAME'] = os.environ.get('VERCEL_URL')
```

#### Supabase Project Setup
```bash
# Create new Supabase project via dashboard
# https://app.supabase.com

# Configure environment variables in Vercel
SUPABASE_URL=your-project-url.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key  # For admin operations
DATABASE_URL=postgresql://...  # Direct connection for migrations

# Set up database schema
flask db upgrade

# Or run migrations directly in Supabase SQL editor
```

#### Environment Variables (Vercel Dashboard)
```bash
# Production Environment Variables
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=your-secret-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
DATABASE_URL=your-direct-db-url

# Optional: Email configuration for magic links
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your-sendgrid-api-key
```

### Monitoring & Maintenance

#### Key Metrics to Track
- [ ] Vercel Analytics (Core Web Vitals)
- [ ] Supabase Dashboard metrics
- [ ] API response times via Vercel Functions
- [ ] Storage usage in Supabase
- [ ] Database connections and query performance

#### Backup Strategy
```python
# Supabase handles automatic backups
# Point-in-Time Recovery available on Pro plan
# Daily backups retained for 7-30 days depending on plan

# Export data via Supabase CLI
supabase db dump -f backup.sql

# Or use pg_dump directly
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

#### Maintenance Tasks
- [ ] Monitor Vercel function logs
- [ ] Review Supabase query performance
- [ ] Check storage bucket usage
- [ ] Update edge cache rules
- [ ] Review RLS policies

---

## Phase 6: Team Adoption

### Rollout Strategy

#### Phase 1: Pilot (Week 1-2)
- Select 3-5 power users
- Daily feedback sessions
- Quick iteration on issues
- Document pain points

#### Phase 2: Department (Week 3-4)
- Expand to full development team
- Training sessions
- Create video tutorials
- Assign content champions

#### Phase 3: Organization (Week 5+)
- Company-wide rollout
- Self-service onboarding
- Regular training workshops
- Feedback surveys

### Training Materials

#### User Guides
- [ ] Getting Started (5 min)
- [ ] Searching Effectively (10 min)
- [ ] Creating Content (15 min)
- [ ] Managing Projects (20 min)
- [ ] Admin Features (30 min)

#### Video Tutorials
- [ ] Platform Overview
- [ ] Search Tips & Tricks
- [ ] Markdown Basics
- [ ] Template Usage
- [ ] Best Practices

### Success Metrics

#### Adoption Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| User Activation | 80% | Users who create content |
| Weekly Active Users | 70% | Login at least once/week |
| Content Creation | 50+ docs/month | New documents added |
| Search Usage | 100+ queries/day | Search analytics |
| User Satisfaction | 4.0/5.0 | Quarterly survey |

---

## Phase 7: Future Enhancements

### Roadmap (Post-MVP)

#### Quarter 1
- [ ] REST API for integrations
- [ ] Webhook notifications
- [ ] Advanced markdown features
- [ ] Bulk import/export

#### Quarter 2
- [ ] Elasticsearch integration
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)
- [ ] SSO integration

#### Quarter 3
- [ ] AI-powered search
- [ ] Content recommendations
- [ ] Automated tagging
- [ ] Translation support

#### Quarter 4
- [ ] GraphQL API
- [ ] Plugin system
- [ ] Custom workflows
- [ ] Advanced analytics

### Innovation Opportunities

#### AI Integration
- Semantic search
- Auto-summarization
- Content generation
- Smart categorization
- Duplicate detection

#### Collaboration Features
- Real-time editing
- Comments system
- Review workflows
- Team spaces
- Activity feeds

#### Integration Ecosystem
- Slack notifications
- JIRA integration
- GitHub sync
- IDE plugins
- CLI tools

---

## Appendix A: Quick Start Commands

### Development Setup
```bash
# Clone repository
git clone https://github.com/company/knowledge-base.git
cd knowledge-base

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Supabase locally (optional)
npm install -g supabase
supabase init
supabase start

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your Supabase credentials

# Initialize database schema in Supabase
# Option 1: Run migrations
export DATABASE_URL=your-supabase-direct-url
flask db upgrade

# Option 2: Execute SQL in Supabase Dashboard
# Copy migration files to SQL editor

# Run development server
flask run --debug

# Or test with Vercel CLI
npm install -g vercel
vercel dev
```

### Vercel Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to Vercel (first time)
vercel

# Deploy to production
vercel --prod

# Set environment variables
vercel env add SUPABASE_URL
vercel env add SUPABASE_ANON_KEY
vercel env add SUPABASE_SERVICE_KEY
vercel env add SECRET_KEY

# View deployment logs
vercel logs
```

### Supabase Setup
```bash
# Create tables in Supabase SQL editor
# Navigate to: https://app.supabase.com/project/YOUR_PROJECT/sql

# Run schema creation scripts
# Enable RLS policies
# Create storage buckets
# Set up Edge Functions (if needed)

# Test connection
python -c "from app.utils.supabase import get_client; client = get_client(); print('Connected!')"
```

### Testing Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Test Vercel functions locally
vercel dev

# Test Supabase functions
supabase functions serve
```

---

## Appendix B: Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check Supabase connection
curl https://YOUR-PROJECT.supabase.co/rest/v1/ \
  -H "apikey: YOUR-ANON-KEY" \
  -H "Authorization: Bearer YOUR-ANON-KEY"

# Test database URL
psql $DATABASE_URL -c "SELECT 1"

# Check Supabase status
# Visit: https://status.supabase.com

# Reset local Supabase
supabase stop
supabase start
supabase db reset
```

#### Search Not Working
```sql
-- Check if search vector is populated (in Supabase SQL editor)
SELECT id, title, search_vector FROM content LIMIT 5;

-- Manually rebuild search index
UPDATE content SET updated_at = now();

-- Verify GIN index exists
SELECT indexname FROM pg_indexes 
WHERE tablename = 'content' AND indexname LIKE '%search%';

-- Test search function
SELECT * FROM search_content('test query');
```

#### File Upload Issues
```python
# Check Supabase Storage bucket configuration
from app.utils.supabase import get_client
client = get_client()

# List buckets
buckets = client.storage.list_buckets()
print(buckets)

# Check bucket policies
# Visit Supabase Dashboard > Storage > Policies

# Test upload
file = open('test.pdf', 'rb')
client.storage.from_('documents').upload('test.pdf', file)
```

#### Vercel Deployment Issues
```bash
# Check Vercel logs
vercel logs --follow

# Verify environment variables
vercel env ls

# Redeploy with clean build
vercel --force

# Check function size (must be under 50MB)
du -sh api/

# Test function locally
vercel dev --debug
```

---

## Appendix C: Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes/python)
- [Supabase Documentation](https://supabase.com/docs)
- [SQLAlchemy with Supabase](https://supabase.com/docs/guides/integrations/sqlalchemy)
- [Supabase Full-Text Search](https://supabase.com/docs/guides/database/full-text-search)
- [Bootstrap 5 Components](https://getbootstrap.com/docs/5.0/)
- [Alpine.js Guide](https://alpinejs.dev/)

### Tools
- [Supabase Dashboard](https://app.supabase.com/) - Database & Storage management
- [Vercel Dashboard](https://vercel.com/dashboard) - Deployment & Analytics
- [TablePlus](https://tableplus.com/) - Database GUI with Supabase support
- [Postman](https://www.postman.com/) - API testing
- [Supabase CLI](https://supabase.com/docs/guides/cli) - Local development
- [Vercel CLI](https://vercel.com/cli) - Deployment management

### Community
- Project Slack: #knowledge-base
- Weekly Standup: Mondays 10am
- Code Review: PR required for main
- Issues: GitHub Issues
- Wiki: Confluence/Internal

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2024-01-15 | Team | Initial project plan |
| 1.1.0 | 2024-02-01 | Team | Added testing strategy |
| 1.2.0 | 2024-02-15 | Team | Updated deployment section |
| 1.3.0 | 2024-03-01 | Team | Added future enhancements |

---

## Sign-off

### Stakeholder Approval

- [ ] **Product Owner**: ___________________ Date: ___________
- [ ] **Tech Lead**: _____________________ Date: ___________
- [ ] **DevOps Lead**: ___________________ Date: ___________
- [ ] **Security Team**: _________________ Date: ___________
- [ ] **QA Lead**: _______________________ Date: ___________

---

**Last Updated**: [Current Date]  
**Status**: In Planning  
**Next Review**: [Date + 2 weeks]