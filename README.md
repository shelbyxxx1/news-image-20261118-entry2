# The World in One Day

A 1024 × 1024 broadsheet front page for the make.fun 18 November 2026 world news bounty. The maps, market strip, and typography are drawn in code from the supplied news brief, with no downloaded assets.

Run `python3 render.py` to rebuild `entry.png` with Pillow and the Noto font files listed in the renderer. The renderer checks text against its layout boxes before saving.

The grader runs `python3 main.py` with only the Python standard library. It clears existing files from `MAKEFUN_OUTPUT_DIR` (default `/output`) and copies the committed PNG there unchanged.
