import os
import re
import urllib.parse

repo = os.environ["GITHUB_REPOSITORY"]
wiki_dir = "wiki"
readme_path = "repo/README.md"
skip = {"Home", "_Sidebar", "_Footer"}

lines = []
for f in sorted(os.listdir(wiki_dir), key=str.lower):
    name, ext = os.path.splitext(f)
    if ext.lower() not in (".md", ".markdown") or name in skip:
        continue
    title = name.replace("-", " ").replace("[", r"\[").replace("]", r"\]")
    url = f"https://github.com/{repo}/wiki/{urllib.parse.quote(name)}"
    lines.append(f"- [{title}]({url})")

block = "<!-- WIKI-PAGES:START -->\n" + "\n".join(lines) + "\n<!-- WIKI-PAGES:END -->"

with open(readme_path, encoding="utf-8") as fh:
    readme = fh.read()

pattern = re.compile(r"<!-- WIKI-PAGES:START -->.*?<!-- WIKI-PAGES:END -->", re.DOTALL)
if not pattern.search(readme):
    raise SystemExit("README markers not found")

new = pattern.sub(lambda m: block, readme)
if new != readme:
    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write(new)