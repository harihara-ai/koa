"""purpose: facts gate_check reads from git and the change folder: base, base-commit files, changed paths, texts.

Every value comes from git or the files themselves, never from what an agent says about them. Also the one reader
of metrics.csv (built slices) and of each slice's requirements, for trace_check, gate_check, slice_pr and pr_body.
"""
import json
import os
import re
import subprocess
import tempfile

DATA = ("comments/", "fetched/")
REQ = re.compile(r"REQ-[A-Z0-9]+-[0-9]+")
PLAN_FILES = ["spec.md", "slices.md", "inputs/diff_scope.json", "inputs/granularity.json"]


def git(*args):
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def default_base():
    for ref in ("origin/HEAD", "origin/main", "origin/master"):
        sha = git("merge-base", "HEAD", ref)
        if sha:
            return sha
    return None


def decode(raw):
    for bom, enc in ((b"\xff\xfe", "utf-16"), (b"\xfe\xff", "utf-16"), (b"\xef\xbb\xbf", "utf-8-sig")):
        if raw.startswith(bom):
            return raw.decode(enc, errors="ignore")
    return raw.decode("utf-8", errors="ignore")


def texts_under(ch):
    out, names = [], set()
    for root, _d, files in os.walk(ch):
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), ch).replace(os.sep, "/")
            if re.fullmatch(r"gates-\w+\.json", rel):
                continue
            kind = "data" if rel == "ticket.md" or rel.startswith(DATA) else "authored"
            names |= {(seg, kind) for seg in rel.split("/")}
            with open(os.path.join(root, name), "rb") as fh:
                text = decode(fh.read())
            if "\x00" not in text:
                out.append({"source": rel, "text": text, "kind": kind})
    return out + [{"source": "file name %s" % n, "text": n, "kind": k} for n, k in sorted(names)]


def from_base(base, rel):
    """A file as it is in the base commit (written to a temp file), or None."""
    text = git("show", "%s:%s" % (base, rel)) if base else None
    if not text:
        return None
    fd, path = tempfile.mkstemp(suffix=os.path.splitext(rel)[1])
    with os.fdopen(fd, "w") as fh:
        fh.write(text + "\n")
    return path


def changed_paths(base):
    return [n for n in ((git("diff", "--no-ext-diff", "--name-only", "--no-renames", base, "--") or "").splitlines()
                        + (git("ls-files", "--others", "--exclude-standard") or "").splitlines()) if n]


def exists_in_base(base, rel):
    """True if the file exists in the base commit, even when it is empty."""
    return bool(base) and subprocess.run(["git", "cat-file", "-e", "%s:%s" % (base, rel)],
                                         capture_output=True).returncode == 0


def slice_of(row):
    """The slice ID of one metrics.csv row (its first column)."""
    return row.split(",")[0].strip()


def built_slices(path):
    """Slice IDs with a metrics.csv row (slicer actual --metrics), or None when there is no metrics.csv."""
    if not (path and os.path.isfile(path)):
        return None
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return {slice_of(row) for row in fh.readlines()[1:]}


def slice_requirements(d):
    """{slice ID: REQ IDs} from inputs/granularity.json "requirements"; older plans: the slices.md table rows."""
    try:
        with open(os.path.join(d, "inputs", "granularity.json"), encoding="utf-8") as fh:
            slices = json.load(fh).get("slices", [])
    except (OSError, ValueError, AttributeError):
        slices = []
    if any(isinstance(s, dict) and "requirements" in s for s in slices):
        return {str(s.get("id")): {r for r in s.get("requirements") or [] if isinstance(r, str) and REQ.fullmatch(r)}
                for s in slices if isinstance(s, dict) and "requirements" in s}
    out = {}
    try:
        with open(os.path.join(d, "slices.md"), encoding="utf-8", errors="ignore") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return out
    for line in lines:
        cells = line.strip().strip("|").split("|")
        reqs = set(REQ.findall(line))
        if line.startswith("|") and len(cells) > 1 and reqs:
            out.setdefault(cells[0].strip(), set()).update(reqs)
    return out


def slices_left(base, ch, plan):
    """One code PR per slice (S06): planned slices with no metrics.csv row in the base commit."""
    done = built_slices(from_base(base, ch + "/metrics.csv"))
    if done is None:
        return []
    with open(os.path.join(plan, "inputs", "granularity.json"), encoding="utf-8") as fh:
        return [s.get("id") for s in json.load(fh).get("slices", []) if str(s.get("id")) not in done]


def approved_plan(base, ch):
    """The plan as merged to the base commit (G1 approval), copied to a temp dir, or None if not merged."""
    d = tempfile.mkdtemp(prefix="plan-")
    for rel in PLAN_FILES:
        src = from_base(base, "%s/%s" % (ch, rel))
        if src:
            os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
            os.replace(src, os.path.join(d, rel))
    return d if os.path.isfile(os.path.join(d, "spec.md")) else None
