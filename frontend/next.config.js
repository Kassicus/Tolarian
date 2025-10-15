/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,

  // API Proxy Configuration
  async rewrites() {
    // In production on Vercel, the API is at the same origin
    // In development, proxy to local Flask server
    const isProduction = process.env.NODE_ENV === 'production';

    if (!isProduction) {
      return [
        {
          source: '/api/v1/:path*',
          destination: 'http://localhost:5000/api/v1/:path*', // Flask backend in dev
        },
      ]
    }

    // In production, API routes are handled by Vercel's rewrites in vercel.json
    return []
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ||
      (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:5000'),
    NEXT_PUBLIC_APP_NAME: 'Tolarian Knowledge Base',
  },

  // Image optimization
  images: {
    domains: ['localhost'],
  },
}

module.exports = nextConfig