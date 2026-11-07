#!/usr/bin/env bash
# purpose: diff-scoped mutation testing (fix plan item 2): Stryker mutates only the lines a PR changed in lib/.
# Report only, never a gate. Run from the PR checkout; this file and its config come from ../approved.
# Usage: mutation.sh BASE_SHA OUT_DIR. Writes OUT_DIR/summary.md; exit 0 unless Stryker itself fails.
set -eu
base=$1; out=$2; here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
ranges=$(git diff -U0 "$base" HEAD -- 'lib/*.js' | python3 -I -c '
import re, sys
f, out = None, []
for line in sys.stdin:
    if line.startswith("+++ "):
        f = line[6:].strip() if line.startswith("+++ b/") else None
    m = re.match(r"@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
    if m and f:
        start, n = int(m.group(1)), int(m.group(2) or 1)
        if n:
            out.append("%s:%d-%d" % (f, start, start + n - 1))
print(",".join(out))')
if [ -z "$ranges" ]; then
  echo "Mutation testing: no changed lines in lib/ (nothing to mutate)." > "$out/summary.md"
  exit 0
fi
python3 -I -c 'import json,sys; c=json.load(open(sys.argv[1])); c["jsonReporter"]={"fileName": sys.argv[2]}; c["tempDirName"]=sys.argv[3]; json.dump(c, open(sys.argv[4], "w"))' \
  "$here/stryker.conf.json" "$out/stryker.json" "$out/tmp" "$out/stryker.conf.json"
npx --yes @stryker-mutator/core@9.6.1 run "$out/stryker.conf.json" --mutate "$ranges" > "$out/stryker.log" 2>&1
python3 -I -c '
import json, sys
r = json.load(open(sys.argv[1]))
rows, k, n = [], 0, 0
for path, f in sorted(r["files"].items()):
    for m in f["mutants"]:
        if m["status"] in ("CompileError", "RuntimeError", "Ignored"):
            continue
        n += 1
        if m["status"] in ("Killed", "Timeout"):
            k += 1
        else:
            rows.append("| %s:%s | %s | %s |" % (path, m["location"]["start"]["line"], m["mutatorName"], m["status"]))
score = 100.0 * k / n if n else 100.0
print("### Mutation testing (changed lines, report only)\n")
print("Score **%.1f%%**: %d of %d mutants killed. Ranges: `%s`\n" % (score, k, n, sys.argv[2]))
if rows:
    print("| Line | Mutator | Status |\n| --- | --- | --- |\n" + "\n".join(rows))
' "$out/stryker.json" "$ranges" > "$out/summary.md"
cat "$out/summary.md"
