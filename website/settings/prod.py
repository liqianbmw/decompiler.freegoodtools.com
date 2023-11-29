from .base import *
DEBUG=False
# DEBUG=True
ALLOWED_HOSTS = ['*'] 
JADX_HOME = 'sh /www/tools/jadx/bin/jadx -d '
APKTOOL_HOME="/www/tools/apktool_2.6.1.jar";
FILE_PATH = "/www/tools";
DOWN_FILE ="/www/tools/down"

INTERNAL_IPS = ['127.0.0.1', ] #debug_toolbar

# STATICFILES_DIRS = [ os.path.join(CORE_DIR, "../static/"),]
STATICFILES_DIRS = [ "/www/wwwroot/decompiler.freegoodtools.com/website/static"]
STATIC_URL = '/static/'
# STATIC_URL = '/www/wwwroot/decompiler.freegoodtools.com/website/static/'
# STATIC_ROOT = os.path.join(CORE_DIR, "static")
STATIC_ROOT = "/www/wwwroot/decompiler.freegoodtools.com/static";