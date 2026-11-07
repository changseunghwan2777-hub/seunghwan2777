# Visual review / Pardesco workflow

Seeds affect the fine endpoints and stroke weight only. Architectural placement, courts and overlaps remain deterministic across all seeds. This is an explicit project constraint: randomness must not redesign the plan.

## Round 1 — density stride 2; weight 0.20px
Viewed hatch-round1.png, seeds 1–9.
- Value structure — weak: all nine thumbnails are pale and overlaps barely separate from single-wing regions.
- Focal hierarchy — weak: repeated internal nodes have insufficient contrast.
- Density variation — weak: empty courts are clear but shared nodes remain light.
- Edges — good: complete envelope with deliberate white margin in all nine.
- Color discipline — good: grayscale only; white paper preserved.
- The tell — good: geometry follows the architectural module; no unrelated noise field. Repetition is intentional, not a failure to randomize.
- Seed robustness — weak visually in all nine, although none is blank or geometrically degenerate.
- Craft — weak: fine lines disappear in thumbnail output.
Worst failure: insufficient value separation. Revision: include every clipped line instead of every second line and increase mean stroke from 0.20 to 0.40 logical px (0.20mm at A2).

## Round 2 — density stride 1; weight 0.40px
Viewed hatch-round2.png, seeds 1–9, and hatch-print-crop.png at pixel scale.
- Value structure — good: single-direction bands, two-direction joints and denser multi-direction nodes are distinguishable in all nine.
- Focal hierarchy — good for a field drawing: repeated darker nodes guide the eye diagonally. No single arbitrary focal spot was imposed on the architecture.
- Density variation — good: untouched courts and exterior alternate with denser connections.
- Edges — good: margin retained; endpoints stop at the floor and court boundaries.
- Color discipline — good: grayscale remained sufficient; no accent color needed in artwork.
- The tell — good: line orientations encode 165/45/285 degree architectural directions.
- Seed robustness — good: 9/9 preserve the composition. Small seed differences are intentionally subtle.
- Craft — good: enlarged crop shows distinct vector strokes and clean court voids. Screen reductions can create moiré; print PDF remains vector.

## Board review
Viewed 01_Array_Rules.png and boards-contact.png. Changed the shared-seam detail to a real pairwise intersection rather than a connected union of several seams. Added indicative desks/chairs only where they fit outside the proposed route strip. The figure–ground and hatch board use exactly the same placement and orientation. Checked final office board after furniture revision.

Rhino desktop is unavailable; the .3dm was written and read back with rhino3dm. Interactive browser tests cover 9 cases, layer changes, SVG export, deterministic hatch seed replay and JS errors. No claim of architectural code compliance is made.
