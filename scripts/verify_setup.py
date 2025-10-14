#!/usr/bin/env python
"""
Verify that the environment and Supabase setup is correct.
Run this to test your configuration.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables from parent directory
parent_dir = Path(__file__).parent.parent
env_path = parent_dir / '.env'
env_local_path = parent_dir / '.env.local'

# Try .env.local first, then .env
if env_local_path.exists():
    print(f"Loading environment from: {env_local_path}")
    load_dotenv(env_local_path)
elif env_path.exists():
    print(f"Loading environment from: {env_path}")
    load_dotenv(env_path)
else:
    print(f"Warning: No .env or .env.local file found in {parent_dir}")
    print("Trying to load from current environment...")
print()

def check_env_variables():
    """Check if all required environment variables are set."""
    print("=" * 50)
    print("Checking Environment Variables")
    print("=" * 50)

    required_vars = {
        'SUPABASE_URL': 'Supabase project URL',
        'SUPABASE_ANON_KEY': 'Supabase anonymous/public key',
        'SUPABASE_SERVICE_KEY': 'Supabase service role key',
    }

    optional_vars = {
        'SECRET_KEY': 'Flask secret key (will use default if not set)',
        'DATABASE_URL': 'Direct PostgreSQL connection (optional)',
    }

    all_good = True

    # Check required variables
    print("\n✓ Required Variables:")
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Mask the value for security
            if 'KEY' in var:
                masked_value = value[:10] + '...' + value[-10:] if len(value) > 20 else '***'
            elif 'URL' in var:
                masked_value = value.split('.supabase.co')[0] + '.supabase.co' if '.supabase.co' in value else value
            else:
                masked_value = '***'
            print(f"  ✅ {var}: {masked_value}")
        else:
            print(f"  ❌ {var}: NOT SET - {description}")
            all_good = False

    # Check optional variables
    print("\n✓ Optional Variables:")
    for var, description in optional_vars.items():
        value = os.environ.get(var)
        if value:
            if var == 'SECRET_KEY':
                masked_value = '***' if value != 'dev-secret-key-change-in-production' else 'DEFAULT (change for production)'
            elif var == 'DATABASE_URL':
                # Mask the password in the database URL
                if '@' in value:
                    parts = value.split('@')
                    masked_value = parts[0].split('://')[0] + '://***@' + parts[1] if len(parts) > 1 else '***'
                else:
                    masked_value = '***'
            else:
                masked_value = '***'
            print(f"  ✅ {var}: {masked_value}")
        else:
            print(f"  ℹ️  {var}: Not set - {description}")

    return all_good

def test_supabase_connection():
    """Test connection to Supabase."""
    print("\n" + "=" * 50)
    print("Testing Supabase Connection")
    print("=" * 50)

    try:
        from supabase import create_client

        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_ANON_KEY')

        if not url or not key:
            print("  ❌ Cannot test connection - missing SUPABASE_URL or SUPABASE_ANON_KEY")
            return False

        print(f"\n  Connecting to: {url}")
        client = create_client(url, key)

        # Try to query the users table (it might be empty, that's ok)
        result = client.table('users').select('id').limit(1).execute()
        print("  ✅ Successfully connected to Supabase!")

        # Check if users table exists and has data
        if result.data:
            print(f"  ℹ️  Users table exists and has data")
        else:
            print(f"  ℹ️  Users table exists but is empty (run seed_users.py to add test users)")

        return True

    except Exception as e:
        error_msg = str(e)
        if 'users' in error_msg and 'does not exist' in error_msg:
            print("  ⚠️  Connected to Supabase but 'users' table doesn't exist")
            print("  ➡️  Please run the setup_supabase.sql script in your Supabase SQL Editor")
        elif 'Invalid API key' in error_msg:
            print("  ❌ Invalid Supabase API key - check your SUPABASE_ANON_KEY")
        elif 'Unable to find' in error_msg or 'getaddrinfo failed' in error_msg:
            print("  ❌ Cannot reach Supabase - check your SUPABASE_URL")
        else:
            print(f"  ❌ Connection failed: {error_msg}")
        return False

def test_service_key():
    """Test if service key works (needed for seeding users)."""
    print("\n" + "=" * 50)
    print("Testing Service Key")
    print("=" * 50)

    try:
        from supabase import create_client

        url = os.environ.get('SUPABASE_URL')
        service_key = os.environ.get('SUPABASE_SERVICE_KEY')

        if not url or not service_key:
            print("  ⚠️  Cannot test service key - missing SUPABASE_SERVICE_KEY")
            print("  ℹ️  Service key is needed for admin operations like seeding users")
            return False

        client = create_client(url, service_key)

        # Try a simple query with service key
        result = client.table('users').select('id').limit(1).execute()
        print("  ✅ Service key is valid and working!")

        return True

    except Exception as e:
        error_msg = str(e)
        if 'Invalid API key' in error_msg:
            print("  ❌ Invalid service key - check your SUPABASE_SERVICE_KEY")
        else:
            print(f"  ❌ Service key test failed: {error_msg}")
        return False

def check_tables():
    """Check if required database tables exist."""
    print("\n" + "=" * 50)
    print("Checking Database Tables")
    print("=" * 50)

    try:
        from supabase import create_client

        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_SERVICE_KEY') or os.environ.get('SUPABASE_ANON_KEY')

        if not url or not key:
            print("  ⚠️  Cannot check tables - missing credentials")
            return False

        client = create_client(url, key)

        tables_to_check = [
            'users',
            'categories',
            'tags',
            'content',
            'content_tags',
            'versions',
            'search_index'
        ]

        all_tables_exist = True

        for table in tables_to_check:
            try:
                result = client.table(table).select('*').limit(1).execute()
                count = len(result.data) if result.data else 0
                print(f"  ✅ Table '{table}' exists")
            except Exception as e:
                print(f"  ❌ Table '{table}' does not exist")
                all_tables_exist = False

        if not all_tables_exist:
            print("\n  ➡️  Please run the setup_supabase.sql script in your Supabase SQL Editor")

        return all_tables_exist

    except Exception as e:
        print(f"  ❌ Error checking tables: {e}")
        return False

def main():
    """Main verification function."""
    print("\n" + "=" * 50)
    print("🔍 Knowledge Base Setup Verification")
    print("=" * 50)

    # Check environment variables
    env_ok = check_env_variables()

    if not env_ok:
        print("\n❌ Missing required environment variables!")
        print("\nMake sure your .env or .env.local file contains:")
        print("  SUPABASE_URL=https://your-project.supabase.co")
        print("  SUPABASE_ANON_KEY=your-anon-key")
        print("  SUPABASE_SERVICE_KEY=your-service-key")
        print("\nYou can find these in your Supabase project settings:")
        print("  1. Go to https://app.supabase.com")
        print("  2. Select your project")
        print("  3. Go to Settings > API")
        print("  4. Copy the URL and keys")
        sys.exit(1)

    # Test Supabase connection
    connection_ok = test_supabase_connection()

    # Test service key
    service_key_ok = test_service_key()

    # Check tables if connected
    if connection_ok:
        tables_ok = check_tables()
    else:
        tables_ok = False

    # Summary
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)

    if env_ok and connection_ok and tables_ok:
        print("\n✅ Everything looks good! Your setup is correct.")
        print("\nNext steps:")
        print("  1. Run: python scripts/seed_users.py")
        print("  2. Run: python run.py")
        print("  3. Visit: http://localhost:5000")
        print("  4. Login with: admin@example.com / admin123")
    elif env_ok and connection_ok and not tables_ok:
        print("\n⚠️  Connected to Supabase but tables are missing.")
        print("\nNext steps:")
        print("  1. Copy the contents of scripts/setup_supabase.sql")
        print("  2. Go to your Supabase project SQL Editor")
        print("  3. Paste and run the SQL script")
        print("  4. Run this verification script again")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")

if __name__ == '__main__':
    main()