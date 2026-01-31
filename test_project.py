#!/usr/bin/env python
"""
Comprehensive test script to verify all functionality works
"""
import os
import django
import sys

# Add the project directory to Python path
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REG_ICT_WADP_L4_001154_ARFAT_RAHMAN_JOB_PORTAL.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.models import RecruiterProfile, JobSeekerProfile
from jobs.models import Job

User = get_user_model()

def test_basic_functionality():
    """Test basic project functionality"""
    client = Client()
    
    print("🧪 Testing Project Functionality...")
    
    # Test 1: Home page loads
    try:
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home page loads successfully")
        else:
            print(f"❌ Home page failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Home page error: {e}")
    
    # Test 2: Registration page loads
    try:
        response = client.get('/accounts/register/')
        if response.status_code == 200:
            print("✅ Registration page loads successfully")
        else:
            print(f"❌ Registration page failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Registration page error: {e}")
    
    # Test 3: Login page loads
    try:
        response = client.get('/accounts/login/')
        if response.status_code == 200:
            print("✅ Login page loads successfully")
        else:
            print(f"❌ Login page failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Login page error: {e}")
    
    # Test 4: Job list loads
    try:
        response = client.get('/jobs/')
        if response.status_code == 200:
            print("✅ Job list page loads successfully")
        else:
            print(f"❌ Job list page failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Job list page error: {e}")

def test_models():
    """Test model functionality"""
    print("\n🏗️  Testing Models...")
    
    try:
        # Test User model
        user_count = User.objects.count()
        print(f"✅ User model working - {user_count} users in database")
        
        # Test profile models
        recruiter_count = RecruiterProfile.objects.count()
        jobseeker_count = JobSeekerProfile.objects.count()
        print(f"✅ Profile models working - {recruiter_count} recruiters, {jobseeker_count} job seekers")
        
        # Test job model
        try:
            job_count = Job.objects.count()
            print(f"✅ Job model working - {job_count} jobs in database")
        except Exception as e:
            print(f"⚠️  Job model issue: {e}")
            
    except Exception as e:
        print(f"❌ Model error: {e}")

def check_template_syntax():
    """Check for common template issues"""
    print("\n📄 Checking Template Syntax...")
    
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist, TemplateSyntaxError
    
    templates_to_check = [
        'base.html',
        'home.html',
        'accounts/login.html',
        'accounts/register.html',
        'accounts/profile.html',
        'jobs/list.html'
    ]
    
    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            print(f"✅ {template_name} - syntax OK")
        except TemplateSyntaxError as e:
            print(f"❌ {template_name} - syntax error: {e}")
        except TemplateDoesNotExist:
            print(f"⚠️  {template_name} - not found")
        except Exception as e:
            print(f"❌ {template_name} - error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Comprehensive Project Test\n")
    test_basic_functionality()
    test_models()
    check_template_syntax()
    print("\n✅ Test completed!")