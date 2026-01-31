
#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','REG_ICT_WADP_L4_001154_ARFAT_RAHMAN_JOB_PORTAL.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
if __name__=='__main__':
    main()
