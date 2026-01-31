#!/usr/bin/env python
"""
Template Syntax Fixer - Prevents and fixes Django template syntax errors
"""
import re

def fix_template_file(file_path):
    """Fix common template syntax issues in a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix multiple template tags on same line
    # Pattern: } {% -> }\n  {% (add newline and indentation)
    content = re.sub(r'%}\s*{%', '%}\n              {%', content)
    
    # Fix specific problematic patterns
    content = re.sub(r'{% endif %}\s*{% else %}', '{% endif %}\n              {% else %}', content)
    content = re.sub(r'{% endif %}\s*{% elif', '{% endif %}\n              {% elif', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed template syntax in {file_path}")

if __name__ == "__main__":
    template_file = r"c:\Users\TNS PC 20\Downloads\New folder\job_portal_final\REG_ICT_WADP_L4_001154_ARFAT_RAHMAN_JOBPortal\templates\base.html"
    fix_template_file(template_file)
    print("🔧 Template syntax fixed!")