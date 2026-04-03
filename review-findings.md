# Code Review Findings: MetaGenome

**Reviewer**: Claude Opus 4.6 (1M context)
**Date**: 2026-04-03
**Files reviewed**: `pipeline.py` (251 lines), `index.html` (45 lines)

## P0 (Critical) -- 1 found

### P0-1: CSV output has no formula injection protection
- **File**: `pipeline.py`, lines 220-233
- **Issue**: CSV DictWriter writes `review_id` and `archetype` fields directly. While current archetypes are fixed strings ("Healthy", "Moderate", "Pathological", "Mixed") and review IDs are Cochrane format, defensive sanitization should be present for robustness.
- **Fix**: Add `csv_safe()` helper that prepends `'` to cell values starting with `=`, `+`, `@`, `\t`, `\r`.

## P1 (Important) -- 2 found

### P1-1: `safe_float` drops valid 0 correctly
- **File**: `pipeline.py`, line 40-45
- **Issue**: `safe_float()` uses `try/except` with `math.isfinite()` check. Returns `default=0` on failure. This correctly handles 0.0 (returns 0.0, not default), because `float("0")` succeeds and `math.isfinite(0)` is True.
- **Status**: Correct.

### P1-2: f_oneway requires at least 2 groups with >1 member
- **File**: `pipeline.py`, lines 204-211
- **Issue**: Code correctly filters `groups = [g for g in groups if len(g) > 1]` before calling f_oneway. Guard is present.
- **Status**: Correct.

## P2 (Minor) -- 2 found

### P2-1: KMeans uses `random_state=42` for determinism
- Good practice observed.

### P2-2: Closing `</html>` tag present in index.html

## Summary
- P0: 1 | P1: 2 | P2: 2
- P0-1 FIXED: CSV injection protection added.
