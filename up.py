#!/usr/bin/env python3
# update the imt frontpage...
import subprocess
import sys
from pathlib import Path

import re

rev = sys.argv[1]

print("putting", rev)

filename = Path("flake.nix")
input = filename.read_text()

output = re.sub('version = "[^"]+"', f'version = "{rev}"', input)
output = re.sub('sha256 = [^;]+', "sha256 = pkgs.lib.fakeSha256", output)
filename.write_text(output)

p = subprocess.Popen(
    ["nix", "build"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
stdout, stderr = p.communicate()
if p.returncode == 0:
    print("all done")
    print(stdout)
else:
    stderr = stderr.decode("utf-8")
    print(stderr)
    new_hash = re.findall(r"got:\s+([^=]+=)", stderr)[0]
    print("new hash", new_hash)
    output = re.sub("pkgs.lib.fakeSha256", f'"{new_hash}"', output)
    filename.write_text(output)
    subprocess.check_call(["nix", "build"])


subprocess.check_call(['git','add','.'])
subprocess.check_call(['git','commit','-m', rev])
subprocess.check_call(['git','tag', rev])
subprocess.check_call(['git','push', 'origin','--tags'])
