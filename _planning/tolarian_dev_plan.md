# Developer Knowledge Base - Development Plan

## Project Overview

A comprehensive knowledge base system for development teams featuring markdown documentation, syntax highlighting, courses, project templates, and rapid search capabilities.

**Tech Stack:**
- **Backend:** Blazor (.NET 9 or .NET 8 LTS)
- **Frontend:** Next.js 15.x with App Router (Next.js 16 beta available but use stable 15.x)
- **Database:** PostgreSQL 17 or 18 with Full-Text Search
- **Storage:** Azure Blob Storage or AWS S3 (for images/files)
- **Search:** PostgreSQL Full-Text Search or Elasticsearch (optional enhancement)
- **UI Library:** React 19.2

## Current Software Versions (as of October 2025)

**Verified Current Versions:**
- **Next.js:** 15.5.6 (stable) | 16.0 (beta, use stable for production)
- **.NET:** 9.0 (current) | 8.0 (LTS, supported until November 2026)
- **React:** 19.2.0
- **react-markdown:** 10.1.0
- **TanStack Query:** 5.90.5
- **PostgreSQL:** 18.0 (latest) | 17.6 (stable)
- **Node.js:** 20.x or 22.x LTS

---

## System Architecture

### Backend (Blazor/ASP.NET Core)
```
DevKnowledgeBase.API/
├── Controllers/
│   ├── ArticlesController.cs
│   ├── TagsController.cs
│   ├── CategoriesController.cs
│   ├── CoursesController.cs
│   ├── TemplatesController.cs
│   ├── SearchController.cs
│   └── MediaController.cs
├── Models/
│   ├── Article.cs
│   ├── Tag.cs
│   ├── Category.cs
│   ├── Course.cs
│   ├── CourseItem.cs
│   ├── Template.cs
│   ├── TemplateFile.cs
│   └── MediaFile.cs
├── Services/
│   ├── ArticleService.cs
│   ├── SearchService.cs
│   ├── StorageService.cs
│   └── TemplateService.cs
├── Data/
│   ├── ApplicationDbContext.cs
│   └── Migrations/
└── Program.cs
```

### Frontend (Next.js)
```
knowledge-base-ui/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── articles/
│   │   │   ├── page.tsx
│   │   │   ├── [id]/page.tsx
│   │   │   └── create/page.tsx
│   │   ├── courses/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── templates/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   └── search/
│   │       └── page.tsx
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── markdown/
│   │   │   ├── MarkdownEditor.tsx
│   │   │   ├── MarkdownViewer.tsx
│   │   │   └── CodeBlock.tsx
│   │   ├── search/
│   │   │   ├── SearchBar.tsx
│   │   │   └── SearchResults.tsx
│   │   ├── articles/
│   │   │   ├── ArticleCard.tsx
│   │   │   ├── ArticleList.tsx
│   │   │   └── TagFilter.tsx
│   │   ├── courses/
│   │   │   ├── CourseCard.tsx
│   │   │   ├── CourseBuilder.tsx
│   │   │   └── CourseProgress.tsx
│   │   └── templates/
│   │       ├── TemplateCard.tsx
│   │       └── TemplateExplorer.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── utils.ts
│   └── types/
│       └── index.ts
├── public/
└── package.json
```

---

## Database Schema

### Core Tables

**Articles**
```sql
CREATE TABLE Articles (
    Id UUID PRIMARY KEY,
    Title VARCHAR(500) NOT NULL,
    Slug VARCHAR(500) UNIQUE NOT NULL,
    Content TEXT NOT NULL,
    CategoryId UUID REFERENCES Categories(Id),
    CreatedAt TIMESTAMP DEFAULT NOW(),
    UpdatedAt TIMESTAMP DEFAULT NOW(),
    CreatedBy VARCHAR(100),
    SearchVector TSVECTOR
);

CREATE INDEX idx_articles_search ON Articles USING GIN(SearchVector);
CREATE INDEX idx_articles_category ON Articles(CategoryId);
```

**Tags**
```sql
CREATE TABLE Tags (
    Id UUID PRIMARY KEY,
    Name VARCHAR(100) UNIQUE NOT NULL,
    Slug VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE ArticleTags (
    ArticleId UUID REFERENCES Articles(Id) ON DELETE CASCADE,
    TagId UUID REFERENCES Tags(Id) ON DELETE CASCADE,
    PRIMARY KEY (ArticleId, TagId)
);
```

**Categories**
```sql
CREATE TABLE Categories (
    Id UUID PRIMARY KEY,
    Name VARCHAR(200) NOT NULL,
    Slug VARCHAR(200) UNIQUE NOT NULL,
    ParentId UUID REFERENCES Categories(Id),
    Description TEXT
);
```

**Courses**
```sql
CREATE TABLE Courses (
    Id UUID PRIMARY KEY,
    Title VARCHAR(500) NOT NULL,
    Slug VARCHAR(500) UNIQUE NOT NULL,
    Description TEXT,
    CreatedAt TIMESTAMP DEFAULT NOW()
);

CREATE TABLE CourseItems (
    Id UUID PRIMARY KEY,
    CourseId UUID REFERENCES Courses(Id) ON DELETE CASCADE,
    ArticleId UUID REFERENCES Articles(Id) ON DELETE CASCADE,
    OrderIndex INT NOT NULL,
    UNIQUE(CourseId, OrderIndex)
);
```

**Templates**
```sql
CREATE TABLE Templates (
    Id UUID PRIMARY KEY,
    Name VARCHAR(200) NOT NULL,
    Description TEXT,
    CreatedAt TIMESTAMP DEFAULT NOW()
);

CREATE TABLE TemplateFiles (
    Id UUID PRIMARY KEY,
    TemplateId UUID REFERENCES Templates(Id) ON DELETE CASCADE,
    Path VARCHAR(500) NOT NULL,
    Content TEXT,
    IsDirectory BOOLEAN DEFAULT FALSE
);
```

**Media**
```sql
CREATE TABLE MediaFiles (
    Id UUID PRIMARY KEY,
    FileName VARCHAR(500) NOT NULL,
    StoragePath VARCHAR(1000) NOT NULL,
    ContentType VARCHAR(100),
    SizeBytes BIGINT,
    UploadedAt TIMESTAMP DEFAULT NOW()
);
```

---

## Development Phases

### Phase 1: Foundation (Week 1-2)

**Backend Tasks:**
1. Set up Blazor Web API project
2. Configure PostgreSQL connection
3. Set up Entity Framework Core
4. Create database models and migrations
5. Implement basic CRUD for Articles
6. Set up CORS for Next.js frontend
7. Implement authentication/authorization (JWT)

**Frontend Tasks:**
1. Initialize Next.js 14 project with TypeScript
2. Set up Tailwind CSS
3. Create base layout components (Navbar, Sidebar)
4. Set up API client with axios/fetch
5. Create basic routing structure
6. Implement environment configuration

**Deliverables:**
- Running backend API
- Basic Next.js frontend with navigation
- Database initialized with migrations

### Phase 2: Markdown & Content Management (Week 3-4)

**Backend Tasks:**
1. Complete Articles CRUD API endpoints
2. Implement Tags and Categories endpoints
3. Add tag/category association logic
4. Implement filtering and pagination

**Frontend Tasks:**
1. Install markdown dependencies (latest versions):
   - `react-markdown@10.1.0` or `@uiw/react-md-editor@latest`
   - `react-syntax-highlighter@latest`
   - `rehype-highlight@latest` and `remark-gfm@latest`
2. Build MarkdownEditor component with live preview
3. Build MarkdownViewer component with syntax highlighting
4. Create Article creation/edit pages
5. Implement tag and category selection UI
6. Build ArticleList with filters

**Key Components to Build:**

**MarkdownEditor.tsx**
```typescript
// Features:
- Split-pane editor/preview
- Toolbar for common markdown actions
- Auto-save functionality
- Image paste support
- Code block language selection
```

**MarkdownViewer.tsx**
```typescript
// Features:
- Syntax highlighting (support 20+ languages)
- Copy code button
- Line numbers
- Theme support (light/dark)
- Table of contents generation
```

**Deliverables:**
- Full markdown editing experience
- Syntax-highlighted code display
- Tag/category management

### Phase 3: Search Implementation (Week 5)

**Backend Tasks:**
1. Implement PostgreSQL Full-Text Search
2. Create search indexes on Articles table
3. Build SearchController with multiple search modes:
   - By title
   - By content
   - By tags
   - By category
4. Implement search result ranking
5. Add autocomplete endpoint

**Frontend Tasks:**
1. Build SearchBar component with autocomplete
2. Create search results page
3. Implement instant search (debounced)
4. Add search filters (tags, categories, date)
5. Highlight search terms in results

**Search Query Example:**
```csharp
// Backend search implementation
public async Task<List<Article>> SearchArticles(string query)
{
    return await _context.Articles
        .Where(a => a.SearchVector.Matches(EF.Functions.ToTsQuery("english", query)))
        .OrderByDescending(a => 
            a.SearchVector.Rank(EF.Functions.ToTsQuery("english", query)))
        .Take(50)
        .ToListAsync();
}
```

**Deliverables:**
- Fast, accurate search functionality
- Search with multiple filter options
- Autocomplete suggestions

### Phase 4: Media & Storage (Week 6)

**Backend Tasks:**
1. Set up blob storage (Azure/AWS)
2. Implement MediaController for uploads
3. Add image optimization/resizing
4. Create secure upload endpoints
5. Implement file validation and limits

**Frontend Tasks:**
1. Build image upload component
2. Add drag-and-drop support
3. Show upload progress
4. Integrate image picker in MarkdownEditor
5. Generate markdown image syntax automatically

**Deliverables:**
- Image upload functionality
- Integrated image insertion in editor
- Secure file storage

### Phase 5: Courses Feature (Week 7)

**Backend Tasks:**
1. Implement Courses CRUD endpoints
2. Create CourseItems management
3. Add reordering functionality
4. Build course enrollment tracking (optional)

**Frontend Tasks:**
1. Build Course list and detail pages
2. Create CourseBuilder component (drag-and-drop reordering)
3. Implement course navigation (previous/next)
4. Add progress tracking UI
5. Build CourseCard component

**CourseBuilder Features:**
- Drag-and-drop article ordering
- Search and add articles to course
- Preview course structure
- Publish/unpublish courses

**Deliverables:**
- Complete course creation system
- Course viewing with navigation
- Progress tracking

### Phase 6: Project Templates (Week 8)

**Backend Tasks:**
1. Implement Templates CRUD
2. Build template file structure management
3. Create ZIP generation for downloads
4. Add template metadata (language, framework, etc.)

**Frontend Tasks:**
1. Build Template creation interface
2. Create file tree component
3. Implement template browser/preview
4. Add download functionality
5. Build template search/filter

**Template Features:**
- Visual folder structure builder
- File content editor
- Template variables (optional)
- One-click download as ZIP

**Deliverables:**
- Template creation system
- Template browser and download
- Folder structure visualization

### Phase 7: Polish & Optimization (Week 9-10)

**Backend Tasks:**
1. Add caching (Redis/Memory Cache)
2. Implement rate limiting
3. Add logging and monitoring
4. Write unit tests
5. Optimize database queries
6. Add API documentation (Swagger)

**Frontend Tasks:**
1. Implement error boundaries
2. Add loading states
3. Optimize bundle size
4. Add PWA support (optional)
5. Implement dark mode
6. Add keyboard shortcuts
7. Write component tests

**Performance Optimizations:**
- Implement Next.js ISR for articles
- Add React Query for caching
- Lazy load heavy components
- Optimize images with Next.js Image
- Implement virtual scrolling for large lists

**Deliverables:**
- Production-ready application
- Comprehensive test coverage
- Performance optimizations

---

## Key Technical Decisions

### Markdown Libraries
**Recommended:** `@uiw/react-md-editor@latest` + `react-markdown@10.1.0` + `react-syntax-highlighter@latest`

**Reasoning:**
- Split-pane editing experience
- Excellent syntax highlighting (20+ languages)
- GitHub Flavored Markdown support
- Active maintenance and React 19 compatible
- TypeScript support out of the box

### Search Implementation
**Recommended:** PostgreSQL Full-Text Search (Phase 1), Elasticsearch (optional Phase 2)

**Reasoning:**
- PostgreSQL FTS is sufficient for <100k articles
- No additional infrastructure needed
- Easy to implement with EF Core
- Upgrade path to Elasticsearch if needed

### State Management
**Recommended:** TanStack Query v5 (React Query) + Zustand (for UI state)

**Reasoning:**
- TanStack Query v5.90+ handles server state perfectly
- Automatic caching and refetching
- Zustand for lightweight client state
- Minimal boilerplate

### Styling
**Recommended:** Tailwind CSS + shadcn/ui components

**Reasoning:**
- Rapid development
- Consistent design system
- Pre-built accessible components
- Easy theming

---

## API Endpoints Reference

### Articles
```
GET    /api/articles                  # List with filters
GET    /api/articles/{id}             # Get single
POST   /api/articles                  # Create
PUT    /api/articles/{id}             # Update
DELETE /api/articles/{id}             # Delete
GET    /api/articles/slug/{slug}      # Get by slug
GET    /api/articles/{id}/tags        # Get article tags
POST   /api/articles/{id}/tags        # Add tags
```

### Search
```
GET    /api/search?q={query}          # Full search
GET    /api/search/autocomplete?q={}  # Autocomplete
GET    /api/search/by-tag/{tagId}     # Search by tag
GET    /api/search/by-category/{id}   # Search by category
```

### Courses
```
GET    /api/courses                   # List courses
GET    /api/courses/{id}              # Get course
POST   /api/courses                   # Create
PUT    /api/courses/{id}              # Update
POST   /api/courses/{id}/items        # Add article to course
PUT    /api/courses/{id}/items/order  # Reorder items
```

### Templates
```
GET    /api/templates                 # List templates
GET    /api/templates/{id}            # Get template
POST   /api/templates                 # Create
GET    /api/templates/{id}/download   # Download as ZIP
GET    /api/templates/{id}/files      # Get file structure
```

### Media
```
POST   /api/media/upload              # Upload file
GET    /api/media/{id}                # Get file info
DELETE /api/media/{id}                # Delete file
```

---

## Environment Setup

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/devkb
JWT_SECRET=your-secret-key
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_STORAGE_URL=https://your-storage.blob.core.windows.net
```

---

## Getting Started Commands

### Backend
```bash
# Ensure you have .NET 9 SDK installed (or .NET 8 LTS)
dotnet --version  # Should show 9.0.x or 8.0.x

dotnet new webapi -n DevKnowledgeBase.API
cd DevKnowledgeBase.API
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package Azure.Storage.Blobs
dotnet ef migrations add InitialCreate
dotnet ef database update
dotnet run
```

### Frontend
```bash
# Next.js 15 with latest features
npx create-next-app@latest knowledge-base-ui --typescript --tailwind --app
cd knowledge-base-ui

# Core markdown libraries (latest versions)
npm install @uiw/react-md-editor react-markdown@10.1.0 react-syntax-highlighter
npm install @tanstack/react-query@latest axios
npm install rehype-highlight remark-gfm
npm install -D @types/react-syntax-highlighter

npm run dev
```

---

## Success Metrics

### Performance Targets
- Search response time: <200ms
- Page load time: <2s
- Markdown preview latency: <100ms
- Image upload: <5s for 5MB file

### Functionality Checklist
- ✅ Create/edit/delete articles
- ✅ Live markdown preview
- ✅ Syntax highlighting (20+ languages)
- ✅ Tag and categorize articles
- ✅ Sub-200ms search
- ✅ Image upload and insertion
- ✅ Create courses with ordered content
- ✅ Create downloadable project templates
- ✅ Folder structure management

---

## Next Steps

1. **Initialize repositories**
   ```bash
   git init DevKnowledgeBase.API
   git init knowledge-base-ui
   ```

2. **Set up development environment**
   - Install PostgreSQL 17 or 18
   - Install .NET 9 SDK (or .NET 8 LTS)
   - Install Node.js 20+
   - Set up Azure/AWS account for storage

3. **Start with Phase 1**
   - Follow the Backend Tasks first
   - Set up database
   - Create basic API structure
   - Then move to Frontend setup

4. **Iterate rapidly**
   - Deploy early and often
   - Get team feedback after Phase 2
   - Adjust priorities based on usage

5. **Documentation**
   - API documentation with Swagger
   - Component storybook (optional)
   - User guide as first article in KB

---

## Future Enhancements (Post-Launch)

- Version control for articles
- Collaborative editing
- Comments and discussions
- Article analytics
- API documentation generator integration
- Webhook integrations
- Mobile app
- Export to PDF
- AI-powered search improvements
- Automatic tag suggestions
- Code snippet execution (sandboxed)