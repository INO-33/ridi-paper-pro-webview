#!/usr/bin/env python3
"""Apply a pinned RIDI patch set and verify exact Git source trees."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('source_root', type=Path)
parser.add_argument('--verify', action='store_true')
args = parser.parse_args()
package = Path(__file__).resolve().parent
root = args.source_root.resolve()
metadata = json.loads((package / 'projects.json').read_text())

def git(path, *arguments):
    result = subprocess.run(['git', '-C', str(path), *arguments],
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(str(path) + ': ' + result.stderr.strip())
    return result.stdout.strip()

pending = []
for row in metadata['projects']:
    project = (root / row['path']).resolve()
    patch = (package / row['patch']).resolve()
    if not project.is_relative_to(root) or not patch.is_relative_to(package):
        raise SystemExit('Package path escapes its root')
    if hashlib.sha256(patch.read_bytes()).hexdigest() != row['patch_sha256']:
        raise SystemExit('Patch hash mismatch: ' + row['path'])
    tree = git(project, 'rev-parse', 'HEAD^{tree}')
    # Gclient manages submodule checkouts separately. Verify their exact target
    # revisions explicitly rather than treating a configured gitlink as a code
    # edit in the enclosing dependency.
    for name, revision in row.get('gitlink_targets', {}).items():
        child = project / name
        if not child.is_dir() or git(child, 'rev-parse', 'HEAD') != revision:
            raise SystemExit('Required submodule revision missing: ' + str(child))
    status = git(project, 'status', '--porcelain=v1', '-uall', '--ignore-submodules=all')
    if status:
        raise SystemExit('Refusing a modified project: ' + row['path'])
    if tree == row['result_tree']:
        continue
    if args.verify:
        raise SystemExit('Restored tree mismatch: ' + row['path'])
    if git(project, 'rev-parse', 'HEAD') != row['base_commit']:
        raise SystemExit('Base commit mismatch: ' + row['path'])
    # Validate every patch before modifying any project.
    git(project, 'apply', '--check', '--index', '--binary', str(patch))
    pending.append((row, project, patch))

for row, project, patch in pending:
    git(project, 'apply', '--index', '--binary', str(patch))
    if git(project, 'write-tree') != row['result_tree']:
        raise SystemExit('Applied tree mismatch; changes retained for inspection: ' + row['path'])
    commit = git(project, '-c', 'user.name=RIDI checkpoint restore',
                 '-c', 'user.email=ridi-restore@localhost',
                 'commit-tree', row['result_tree'], '-p', row['base_commit'],
                 '-m', 'Restore RIDI ' + metadata['checkpoint'])
    # A detached local checkpoint commit does not replace upstream refs. The
    # index and files already match this tree, so only HEAD moves here.
    git(project, 'update-ref', '--no-deref', 'HEAD', commit, row['base_commit'])
print('Verified ' + str(len(metadata['projects'])) + ' exact RIDI project trees')
