#!/usr/bin/env python3
"""Emit a deploy-safe, fully anonymized copy of the site."""
import re, os, sys

src = open('index.html', encoding='utf-8').read()

# 1) Blank confidential fields in the APPS tracker array.
src = re.sub(r'co:"[^"]*"', 'co:""', src)
src = re.sub(r'sal:"[^"]*"', 'sal:""', src)

# 2) Force public mode.
src = src.replace('let MODE = "public"', 'let MODE = "public"  /* deploy build */')

# 3) REMOVE the Public/Private toggle markup entirely.
src = src.replace(
'''    <div class="modebar" style="margin-top:26px">
      <div class="switch" id="modeSwitch" role="switch" aria-label="Toggle public or private view" tabindex="0">
        <span class="lbl pub">Public</span><span class="lbl pri">Private</span><span class="knob"></span>
      </div>
      <span id="modeDesc" class="pill"></span>
    </div>
''', '')

# 4) Remove the toggle's script references.
src = src.replace(
'''  modeSwitch.classList.toggle("private", priv);
  modeSwitch.setAttribute("aria-checked", priv);
  modeDesc.textContent = priv ? "🔓 Full detail — companies, comp, contacts" : "🌐 Safe to share — industries only, no comp";
''', '')
src = src.replace(
'''  const note = priv
    ? "🔒 You're viewing the private build. Real companies, salaries, and contacts are visible."
    : "🌐 Public build: companies shown as industries, compensation hidden, contacts anonymized.";
  heroPriv.innerHTML = note; footPriv.textContent = priv ? "Private view active." : "Public view — shareable.";''',
'''  heroPriv.innerHTML = "🌐 Public build: companies shown as industries, compensation hidden, contacts anonymized.";
  footPriv.textContent = "Public view — shareable.";''')
src = src.replace(
'''modeSwitch.addEventListener("click", ()=>{ MODE = MODE==="public"?"private":"public"; renderMode(); });
modeSwitch.addEventListener("keydown", e=>{ if(e.key===" "||e.key==="Enter"){e.preventDefault(); modeSwitch.click();} });
''', '')

# 5) Drop the hero line inviting a flip.
src = src.replace(
  'Every section below flips to reveal the code behind it. Flip the switch to see the difference between what I keep private and what I share publicly.',
  'Every section below flips to reveal the code behind it — the whole search, engineered in the open.')

out_dir = 'public'
os.makedirs(out_dir, exist_ok=True)
open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8').write(src)

co_left  = [c for c in re.findall(r'co:"([^"]*)"',  src) if c.strip()]
sal_left = [s for s in re.findall(r'sal:"([^"]*)"', src) if s.strip()]
dollars  = re.findall(r'\$\s?\d{2,3}\s?[Kk]', src)
problems = []
if co_left:  problems.append(f"{len(co_left)} company value(s) not blanked")
if sal_left: problems.append(f"{len(sal_left)} salary value(s) not blanked")
if dollars:  problems.append(f"{len(dollars)} salary-like token(s) remain")
if 'modeSwitch' in src:      problems.append("toggle script still present")
if 'id="modeSwitch"' in src: problems.append("toggle markup still present")

print("Wrote public/index.html (%d bytes)" % len(src))
print("Safety check:", "; ".join(problems) if problems else "clean")
sys.exit(1 if problems else 0)
