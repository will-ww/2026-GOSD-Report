"""Rebuild the eight print modules from the preserved source package."""
from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
base=R.parent/'front-v0.8'
subprocess.run([sys.executable,str(base/'prepare_fonts.py')],check=True)
(base/'.texmf-var').mkdir(exist_ok=True)
for root in [R/'frontmatter',R/'master']:
 for name,target in [('fonts',base/'fonts'),('.texmf-var',base/'.texmf-var')]:
  if not (root/name).exists():(root/name).symlink_to(target,target_is_directory=True)
subprocess.run([sys.executable,str(R/'prepare_front.py')],check=True)
subprocess.run([sys.executable,str(R/'frontmatter/build_front.py')],check=True)
subprocess.run([sys.executable,str(R/'build_modules.py')],check=True)
subprocess.run([sys.executable,str(R/'repair_page80.py'),'--in-place'],check=True)
subprocess.run([sys.executable,str(R/'refine_method_intro.py')],check=True)
