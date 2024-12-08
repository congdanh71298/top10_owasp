import subprocess
import os
from django.conf import settings

def check_dependencies():
    """Check Python and JavaScript dependencies for known security vulnerabilities.

    This function performs security audits on project dependencies by:
    1. Running safety check on Python dependencies if enabled in settings
    2. Running npm audit on JavaScript dependencies if package.json exists

    Can be run manually or integrated into CI pipelines. Uses safety tool to scan Python
    dependencies against CVE database and npm audit to check JavaScript dependencies
    for known vulnerabilities.

    Dependencies:
      - safety (Python package)
      - npm (Node.js package manager)

    Returns:
      None. Subprocess results are printed to stdout.

    Note:
      - Requires safety checks to be enabled in settings.SAFETY_CHECKS['ENABLED']
      - Only runs npm audit if package.json exists in current directory
      - Basic dependency checking focused on security vulnerabilities
      - Can be customized further based on project needs
    """
    # Check Python deps
    if settings.SAFETY_CHECKS['ENABLED']:
        subprocess.run(['safety', 'check'])

    # Check npm deps if package.json exists
    if os.path.exists('package.json'):
        subprocess.run(['npm', 'audit'])

if __name__ == '__main__':
    check_dependencies()