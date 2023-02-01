import os
import json, os

print(json.dumps(dict(os.environ), indent = 2))
print(os.environ.get('JDK_HOME'))
print(os.environ.get('JRE_HOME'))