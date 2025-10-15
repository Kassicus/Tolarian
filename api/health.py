"""
Simple health check endpoint for debugging.
"""

def handler(request):
    """Vercel serverless function handler."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': {
            'status': 'healthy',
            'message': 'API is running',
            'path': request.path if hasattr(request, 'path') else 'unknown'
        }
    }