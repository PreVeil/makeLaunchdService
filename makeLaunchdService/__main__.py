import os
import sys
import shutil
import plistlib
import stat
import subprocess
import tempfile

import pvHelpers

if len(sys.argv) != 3:
    print "error, usage: %s <label> <module>" % sys.argv[0]
    sys.exit(1)
label = sys.argv[1]
module = sys.argv[2]

template_path = os.path.join(pvHelpers.getdir(__file__), "launchd.template.plist")
plist = plistlib.readPlist(template_path)

plist['Label'] = label
plist['ProgramArguments'] = [
    "/Applications/PreVeil/penv/bin/python",
    "-m",
    module,
]

temp_handle, plist_path = tempfile.mkstemp()
os.close(temp_handle)
plistlib.writePlist(plist, plist_path)

# Fix permissions and filename so launchd will accept it
os.chmod(plist_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
shutil.move(plist_path, "%s.plist" % plist_path)
plist_path = "%s.plist" % plist_path
print "success: plist file created"

ret = subprocess.call(["plutil", "-lint", plist_path])
if ret != 0:
    print "error: plutil -lint failed"
    sys.exit(1)
print "success: lint"

ret = subprocess.call(["launchctl", "load", plist_path])
if ret != 0:
    print "error: launchctl load failed"
    sys.exit(1)
print "success: launchctl load"

print "success"
sys.exit(0)
