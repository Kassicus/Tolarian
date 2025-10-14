#!/usr/bin/env python
"""
Seed test users for development.
Run this after setting up the Supabase database tables.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import bcrypt
from supabase import create_client, Client
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

# Debug: Print what we loaded
print(f"SUPABASE_URL: {'Set' if os.environ.get('SUPABASE_URL') else 'Not found'}")
print(f"SUPABASE_SERVICE_KEY: {'Set' if os.environ.get('SUPABASE_SERVICE_KEY') else 'Not found'}")
print()

def get_supabase_client() -> Client:
    """Get Supabase client with service role key for admin operations."""
    url = os.environ.get('SUPABASE_URL')
    service_key = os.environ.get('SUPABASE_SERVICE_KEY')

    if not url or not service_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment")

    return create_client(url, service_key)

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def seed_users():
    """Create test users for development."""
    client = get_supabase_client()

    # Test users
    test_users = [
        {
            'email': 'admin@example.com',
            'username': 'admin',
            'password': 'admin123',  # Change this in production!
            'full_name': 'Admin User',
            'role': 'admin',
            'bio': 'System administrator',
            'is_active': True
        },
        {
            'email': 'editor@example.com',
            'username': 'editor',
            'password': 'editor123',  # Change this in production!
            'full_name': 'Editor User',
            'role': 'editor',
            'bio': 'Content editor',
            'is_active': True
        },
        {
            'email': 'viewer@example.com',
            'username': 'viewer',
            'password': 'viewer123',  # Change this in production!
            'full_name': 'Viewer User',
            'role': 'viewer',
            'bio': 'Read-only user',
            'is_active': True
        },
        {
            'email': 'john.doe@example.com',
            'username': 'johndoe',
            'password': 'password123',  # Change this in production!
            'full_name': 'John Doe',
            'role': 'editor',
            'bio': 'Software developer',
            'location': 'New York, NY',
            'website': 'https://johndoe.example.com',
            'is_active': True
        },
        {
            'email': 'jane.smith@example.com',
            'username': 'janesmith',
            'password': 'password123',  # Change this in production!
            'full_name': 'Jane Smith',
            'role': 'editor',
            'bio': 'Technical writer',
            'location': 'San Francisco, CA',
            'is_active': True
        }
    ]

    print("Creating test users...")

    for user_data in test_users:
        # Extract password and hash it
        password = user_data.pop('password')
        password_hash = hash_password(password)

        # Check if user already exists
        existing = client.table('users').select('id').eq('email', user_data['email']).execute()

        if existing.data:
            print(f"  User {user_data['email']} already exists, skipping...")
            continue

        # Create user with hashed password
        user_data['password_hash'] = password_hash
        user_data['created_at'] = datetime.utcnow().isoformat()
        user_data['updated_at'] = datetime.utcnow().isoformat()

        try:
            result = client.table('users').insert(user_data).execute()
            print(f"  ✓ Created user: {user_data['email']} (password: {password})")
        except Exception as e:
            print(f"  ✗ Failed to create user {user_data['email']}: {e}")

    print("\nTest users created successfully!")
    print("\nYou can now login with:")
    print("  Admin:   admin@example.com / admin123")
    print("  Editor:  editor@example.com / editor123")
    print("  Viewer:  viewer@example.com / viewer123")

def main():
    """Main function."""
    print("=" * 50)
    print("Knowledge Base - Seed Test Users")
    print("=" * 50)

    try:
        seed_users()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have:")
        print("1. Set up your Supabase project")
        print("2. Run the setup_supabase.sql script in Supabase SQL Editor")
        print("3. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in your .env file")
        sys.exit(1)

if __name__ == '__main__':
    main()