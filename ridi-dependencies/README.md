# Preserved Chromium M58 dependency changes

Breakpad and SwiftShader changes are bundled inside the RIDI_CHROMIUM_M58
repository. projects.json pins upstream bases, patch hashes, exact result trees
and required gitlink revisions. The consolidated manifest prepares upstream DEPS
checkouts then invokes apply.py with the Chromium workspace root (parent of src).
The earlier individual dependency repositories are archived backups only.
