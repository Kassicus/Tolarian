-- Supabase SQL Setup Script for Knowledge Base Application
-- Run this in your Supabase SQL Editor

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE user_role AS ENUM ('viewer', 'editor', 'admin');
CREATE TYPE content_type AS ENUM ('document', 'template', 'guide', 'link');
CREATE TYPE content_status AS ENUM ('draft', 'published', 'archived');

-- Users table (for local development authentication)
-- In production, this will integrate with AD
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- For local dev only
    full_name VARCHAR(255),
    role user_role DEFAULT 'viewer' NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    avatar_url VARCHAR(500),
    bio VARCHAR(500),
    location VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    last_login_at TIMESTAMP WITH TIME ZONE
);

-- Create index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    parent_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent ON categories(parent_id);

-- Tags table
CREATE TABLE IF NOT EXISTS tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#6c757d',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

CREATE INDEX idx_tags_slug ON tags(slug);

-- Content table
CREATE TABLE IF NOT EXISTS content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content_type content_type NOT NULL,
    body TEXT,
    content_metadata JSONB,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    author_id UUID REFERENCES users(id) NOT NULL,
    status content_status DEFAULT 'draft' NOT NULL,
    is_featured BOOLEAN DEFAULT false,
    view_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    published_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_content_slug ON content(slug);
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_content_type ON content(content_type);
CREATE INDEX idx_content_author ON content(author_id);
CREATE INDEX idx_content_category ON content(category_id);

-- Content-Tags junction table (many-to-many)
CREATE TABLE IF NOT EXISTS content_tags (
    content_id UUID REFERENCES content(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (content_id, tag_id)
);

-- Versions table for content version control
CREATE TABLE IF NOT EXISTS versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID REFERENCES content(id) ON DELETE CASCADE NOT NULL,
    version_number INTEGER NOT NULL,
    changes JSONB,
    commit_message VARCHAR(255),
    author_id UUID REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    UNIQUE(content_id, version_number)
);

CREATE INDEX idx_versions_content ON versions(content_id, version_number);

-- Search index table (optional, for caching search vectors)
CREATE TABLE IF NOT EXISTS search_index (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID REFERENCES content(id) ON DELETE CASCADE NOT NULL UNIQUE,
    search_vector tsvector,
    rank REAL DEFAULT 0.0,
    keywords TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Add full-text search to content
ALTER TABLE content ADD COLUMN IF NOT EXISTS search_vector tsvector
    GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(body, '')), 'B')
    ) STORED;

CREATE INDEX IF NOT EXISTS idx_content_search ON content USING GIN(search_vector);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_content_updated_at BEFORE UPDATE ON content
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE content ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE tags ENABLE ROW LEVEL SECURITY;

-- Create RLS policies (basic policies for development)
-- In production, these would be more sophisticated

-- Users table policies
CREATE POLICY "Users are viewable by everyone" ON users
    FOR SELECT USING (true);

CREATE POLICY "Users can update their own record" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Content table policies
CREATE POLICY "Published content is viewable by everyone" ON content
    FOR SELECT USING (status = 'published' OR author_id = auth.uid()::uuid);

CREATE POLICY "Users can create content" ON content
    FOR INSERT WITH CHECK (auth.uid()::uuid = author_id);

CREATE POLICY "Users can update their own content" ON content
    FOR UPDATE USING (auth.uid()::uuid = author_id);

CREATE POLICY "Users can delete their own content" ON content
    FOR DELETE USING (auth.uid()::uuid = author_id);

-- Categories and tags are publicly readable
CREATE POLICY "Categories are viewable by everyone" ON categories
    FOR SELECT USING (true);

CREATE POLICY "Tags are viewable by everyone" ON tags
    FOR SELECT USING (true);

-- Create search function
CREATE OR REPLACE FUNCTION search_content(
    search_query TEXT,
    result_limit INT DEFAULT 10,
    result_offset INT DEFAULT 0
)
RETURNS TABLE(
    id UUID,
    title TEXT,
    content_type content_type,
    body TEXT,
    rank REAL,
    highlight_title TEXT,
    highlight_body TEXT
)
LANGUAGE plpgsql
AS $$
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
$$;

-- Insert some default categories
INSERT INTO categories (name, slug, description, icon, order_index) VALUES
    ('Development', 'development', 'Code standards, best practices, and development guides', 'bi-code-slash', 1),
    ('Templates', 'templates', 'Ready-to-use project templates and boilerplates', 'bi-file-earmark-text', 2),
    ('Guides', 'guides', 'Step-by-step tutorials and how-to guides', 'bi-book', 3),
    ('Tools', 'tools', 'Development tools and utilities', 'bi-tools', 4),
    ('Resources', 'resources', 'External links and references', 'bi-link-45deg', 5)
ON CONFLICT (slug) DO NOTHING;

-- Insert some default tags
INSERT INTO tags (name, slug, color) VALUES
    ('Python', 'python', '#3776AB'),
    ('JavaScript', 'javascript', '#F7DF1E'),
    ('Docker', 'docker', '#2496ED'),
    ('Database', 'database', '#336791'),
    ('API', 'api', '#6BA644'),
    ('Security', 'security', '#FFA500'),
    ('Performance', 'performance', '#DC382D'),
    ('Testing', 'testing', '#00C853')
ON CONFLICT (slug) DO NOTHING;