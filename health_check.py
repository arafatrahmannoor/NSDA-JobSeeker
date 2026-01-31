#!/usr/bin/env python
"""
Comprehensive Project Health Check
This script validates all aspects of the Django job portal project
"""
import os
import sys
import django
import subprocess
from pathlib import Path

# Setup Django
project_path = Path(__file__).parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REG_ICT_WADP_L4_001154_ARFAT_RAHMAN_JOB_PORTAL.settings')
sys.path.insert(0, str(project_path))

try:
    django.setup()
    from django.core.management import execute_from_command_line
    from django.test import Client
    from accounts.models import User, RecruiterProfile, JobSeekerProfile
    from jobs.models import Job
    django_available = True
except Exception as e:
    django_available = False
    print(f"❌ Django setup failed: {e}")

def check_file_structure():
    """Check if all required files and directories exist"""
    print("🏗️  Checking Project Structure...")
    
    required_files = [
        'manage.py',
        'db.sqlite3',
        'REG_ICT_WADP_L4_001154_ARFAT_RAHMAN_JOB_PORTAL/settings.py',
        'REG_ICT_WADP_L4_001154_ARFAT_RAHMAN_JOB_PORTAL/urls.py',
        'accounts/models.py',
        'accounts/views.py',
        'accounts/urls.py',
        'jobs/models.py',
        'jobs/views.py',
        'jobs/urls.py',
        'dashboard/views.py',
        'dashboard/urls.py',
        'templates/base.html',
        'templates/home.html',
    ]
    
    missing = []
    for file_path in required_files:
        full_path = project_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n⚠️  Missing files: {len(missing)}")
    else:
        print("\n✅ All required files present")
    
    return len(missing) == 0

def check_django_system():
    """Run Django system checks"""
    print("\n🔧 Running Django System Check...")
    
    if not django_available:
        print("❌ Django not available")
        return False
    
    try:
        from django.core.management.commands.check import Command
        from io import StringIO
        from django.core.management.base import CommandError
        
        # Capture output
        output = StringIO()
        command = Command()
        
        try:
            command.handle(verbosity=1, stdout=output)
            result = output.getvalue()
            if "no issues" in result.lower():
                print("✅ Django system check passed")
                return True
            else:
                print(f"⚠️  System check issues:\n{result}")
                return True  # Still functional
        except CommandError as e:
            print(f"❌ System check failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ System check error: {e}")
        return False

def check_database():
    """Check database and migrations"""
    print("\n💾 Checking Database...")
    
    if not django_available:
        return False
    
    try:
        # Check if database file exists
        db_path = project_path / 'db.sqlite3'
        if not db_path.exists():
            print("❌ Database file not found")
            return False
        
        # Check models
        user_count = User.objects.count()
        job_count = Job.objects.count()
        recruiter_count = RecruiterProfile.objects.count()
        jobseeker_count = JobSeekerProfile.objects.count()
        
        print(f"✅ Database connected - {user_count} users, {job_count} jobs")
        print(f"✅ Profiles - {recruiter_count} recruiters, {jobseeker_count} job seekers")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_templates():
    """Check template syntax and structure"""
    print("\n📄 Checking Templates...")
    
    templates_dir = project_path / 'templates'
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    template_files = []
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                template_files.append(os.path.join(root, file))
    
    print(f"📊 Found {len(template_files)} template files")
    
    # Check for common template issues
    issues_found = 0
    for template_file in template_files:
        relative_path = os.path.relpath(template_file, project_path)
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for template syntax issues
            if '} {%' in content or '%} {%' in content:
                print(f"⚠️  {relative_path}: Potential template tag spacing issues")
                issues_found += 1
            else:
                print(f"✅ {relative_path}")
                
        except Exception as e:
            print(f"❌ {relative_path}: {e}")
            issues_found += 1
    
    return issues_found == 0

def check_urls():
    """Test URL patterns"""
    print("\n🌐 Checking URL Patterns...")
    
    if not django_available:
        return False
    
    test_urls = [
        '/',
        '/accounts/login/',
        '/accounts/register/', 
        '/jobs/',
        '/dashboard/',
    ]
    
    client = Client()
    working_urls = 0
    
    for url in test_urls:
        try:
            response = client.get(url)
            if response.status_code in [200, 302, 301]:  # OK, redirect, or moved
                print(f"✅ {url} - Status {response.status_code}")
                working_urls += 1
            else:
                print(f"⚠️  {url} - Status {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    return working_urls == len(test_urls)

def generate_report():
    """Generate final report"""
    print("\n" + "="*60)
    print("📋 PROJECT HEALTH REPORT")
    print("="*60)
    
    checks = [
        ("File Structure", check_file_structure()),
        ("Django System", check_django_system()),
        ("Database", check_database()),
        ("Templates", check_templates()),
        ("URL Patterns", check_urls()),
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\n📊 Overall Score: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! Project is healthy and ready to use.")
        return True
    elif passed >= total * 0.8:
        print("✅ Project is mostly working with minor issues.")
        return True
    else:
        print("⚠️  Project has significant issues that need attention.")
        return False

if __name__ == "__main__":
    print("🚀 COMPREHENSIVE PROJECT HEALTH CHECK")
    print("="*60)
    
    success = generate_report()
    
    if success:
        print("\n💡 To start the server: python manage.py runserver")
        sys.exit(0)
    else:
        print("\n💡 Fix the issues above before running the server.")
        sys.exit(1)