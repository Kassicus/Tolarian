#!/usr/bin/env python
"""Debug script to verify environment variables are loaded correctly."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env.local or .env file
base_dir = Path(__file__).parent
env_file = base_dir / '.env.local' if (base_dir / '.env.local').exists() else base_dir / '.env'

print(f"Loading environment from: {env_file}")
load_dotenv(env_file)

# Check critical environment variables
env_vars = {
    'SUPABASE_URL': os.environ.get('SUPABASE_URL'),
    'SUPABASE_ANON_KEY': os.environ.get('SUPABASE_ANON_KEY'),
    'SUPABASE_SERVICE_KEY': os.environ.get('SUPABASE_SERVICE_KEY'),
}

print("\nEnvironment Variables Status:")
print("=" * 50)

for var, value in env_vars.items():
    if value:
        # Mask sensitive values
        if 'KEY' in var:
            masked = value[:10] + '...' if len(value) > 10 else '***'
        else:
            masked = value
        print(f"✅ {var}: {masked}")
    else:
        print(f"❌ {var}: NOT SET")

# Now test Flask app config loading
print("\nFlask App Config Loading:")
print("=" * 50)

from app import create_app
app = create_app('development')

with app.app_context():
    print(f"SUPABASE_URL: {app.config.get('SUPABASE_URL', 'NOT SET')}")
    print(f"SUPABASE_ANON_KEY: {'SET' if app.config.get('SUPABASE_ANON_KEY') else 'NOT SET'}")
    print(f"SUPABASE_SERVICE_KEY: {'SET' if app.config.get('SUPABASE_SERVICE_KEY') else 'NOT SET'}")