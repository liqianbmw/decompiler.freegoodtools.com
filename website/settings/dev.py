from .base import *
# DEBUG=False
DEBUG=True
INTERNAL_IPS = ['127.0.0.1', ]#debug_toolbar
ALLOWED_HOSTS = ['*']
JADX_HOME = 'jadx -d '
APKTOOL_HOME="/Users/qianli/workspace/python/www/tools/apktool_2.6.1.jar";
FILE_PATH = "/Users/qianli/workspace/python/www/tools";
DOWN_FILE ="/Users/qianli/workspace/python/www/tools/down"

# STATICFILES_DIRS = [ os.path.join(CORE_DIR, "../static/"),]
STATICFILES_DIRS = [ "/Users/qianli/workspace/python/www/decompiler.freegoodtools.com/website/static"]
STATIC_URL = '/static/'
# STATIC_URL = '/Users/qianli/workspace/python/www/decompiler.freegoodtools.com/website/static/'
# STATIC_ROOT = os.path.join(CORE_DIR, "static")
STATIC_ROOT = "/Users/qianli/workspace/python/www/decompiler.freegoodtools.com/static";