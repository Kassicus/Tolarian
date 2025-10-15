# Deployment Guide for Tolarian Knowledge Base

This application consists of a Flask API backend and a Next.js frontend, deployed as a monorepo on Vercel.

## Architecture Overview

- **Backend**: Flask API served via Vercel Serverless Functions (Python)
- **Frontend**: Next.js application
- **Database**: PostgreSQL (external, e.g., Supabase, Neon, or Vercel Postgres)

## Deployment Steps

### 1. Prerequisites

- Vercel account
- GitHub repository connected to Vercel
- PostgreSQL database (Supabase, Neon, or Vercel Postgres)

### 2. Project Configuration

The project is configured with the following files:
- `vercel.json` - Main Vercel configuration
- `frontend/vercel.json` - Frontend-specific configuration
- `api/vercel_app.py` - Flask API serverless handler

### 3. Environment Variables

Set the following environment variables in your Vercel project settings:

#### Required Variables

```bash
# Flask/Python Backend
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=<generate-secure-key>
PYTHONPATH=/var/task

# Database
DATABASE_URL=<your-database-url>

# Supabase (if using)
SUPABASE_URL=<your-supabase-url>
SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_SERVICE_KEY=<your-service-key>
```

#### Optional Variables

```bash
# Frontend (if different from deployment URL)
NEXT_PUBLIC_API_URL=<your-api-url>
```

### 4. Deploy to Vercel

#### Option A: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Option B: Deploy via GitHub

1. Connect your GitHub repository to Vercel
2. Configure environment variables in Vercel dashboard
3. Push to main branch to trigger deployment

### 5. Post-Deployment

After deployment:

1. **Test API Endpoints**: Visit `https://your-domain.vercel.app/api/v1/health` to verify API is working
2. **Check Frontend**: Visit `https://your-domain.vercel.app` to see the Next.js app
3. **Monitor Logs**: Check Vercel Functions logs for any API errors

## Project Structure

```
/
├── api/                  # Vercel serverless functions
│   └── vercel_app.py    # Flask API handler
├── app/                  # Flask application
│   ├── api/             # API routes
│   ├── models/          # Database models
│   └── __init__.py      # Flask app factory
├── frontend/            # Next.js application
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   └── package.json    # Frontend dependencies
├── vercel.json          # Main Vercel configuration
└── requirements.txt     # Python dependencies
```

## API Routes

The Flask API is accessible at `/api/v1/*` and includes:
- Authentication endpoints
- Content management
- User management
- Search functionality

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure `PYTHONPATH=/var/task` is set
   - Check that all dependencies are in `requirements.txt`

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is correctly set
   - Check database is accessible from Vercel's network

3. **CORS Errors**
   - API and frontend are on same domain in production
   - CORS should be handled automatically

4. **Build Failures**
   - Check Node.js and Python versions match Vercel's defaults
   - Review build logs in Vercel dashboard

### Debug Mode

To enable debug mode for troubleshooting:
1. Set `FLASK_DEBUG=true` in Vercel environment variables (development only!)
2. Check Function logs in Vercel dashboard

## Performance Optimization

- Frontend uses Next.js SSG/ISR for optimal performance
- API functions have 30-second timeout limit
- Static assets are served from Vercel's CDN

## Security Considerations

- Never commit `.env` files
- Use strong `SECRET_KEY` values
- Keep `SUPABASE_SERVICE_KEY` secure
- Enable Vercel's DDoS protection

## Support

For issues or questions:
1. Check Vercel deployment logs
2. Review Flask API logs in Functions tab
3. Test API endpoints directly using tools like Postman