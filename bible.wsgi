import sys
sys.path.insert(0,'/var/bible')
from bible import create_app as application

application = create_app('conf/deploy.cfg')
