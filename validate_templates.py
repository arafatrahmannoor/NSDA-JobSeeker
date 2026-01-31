#!/usr/bin/env python
"""
Template Syntax Validator - Prevents Django template syntax errors
"""
import os
import re
import sys

def validate_template_file(file_path):
    """Check a single template file for common syntax issues"""
    errors = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        
        # Check for multiple template tags on single line
        if re.search(r'%}\s*{%', line):
            errors.append(f"Line {i}: Multiple template tags on same line: {line}")
        
        # Check for unmatched if/endif patterns
        if line.count('{% if') > 0 and line.count('{% endif') > 0:
            errors.append(f"Line {i}: Mixed if/endif on same line: {line}")
            
        # Check for broken tag patterns
        if re.search(r'%}\s*{%\s*(else|elif)', line):
            errors.append(f"Line {i}: Malformed else/elif after endif: {line}")
    
    return errors

def validate_all_templates(project_path):
    """Validate all templates in the project"""
    template_dir = os.path.join(project_path, 'templates')
    all_errors = []
    
    if not os.path.exists(template_dir):
        print(f"❌ Templates directory not found: {template_dir}")
        return
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                
                errors = validate_template_file(file_path)
                if errors:
                    all_errors.extend([(relative_path, error) for error in errors])
                else:
                    print(f"✅ {relative_path} - OK")
    
    if all_errors:
        print("\n❌ Template syntax issues found:")
        for file_path, error in all_errors:
            print(f"   {file_path}: {error}")
        return False
    else:
        print("\n✅ All templates pass syntax validation!")
        return True

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.abspath(__file__))
    print("🔍 Validating Django Templates...")
    print("=" * 50)
    
    success = validate_all_templates(project_path)
    if success:
        print("\n🎉 No template syntax issues detected!")
        sys.exit(0)
    else:
        print("\n💡 Fix the above issues to prevent Django template errors.")
        sys.exit(1)