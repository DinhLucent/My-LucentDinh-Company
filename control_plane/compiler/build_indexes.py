"""Build Indexes — Master builder that runs all compilers.

Call this once to regenerate all compiled knowledge artifacts.
Results go to knowledge/compiled/.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from control_plane.compiler.compile_roles import compile_roles
from control_plane.compiler.compile_skills import compile_skills
from control_plane.compiler.compile_docs import compile_docs


def build_all(repo_root: Path) -> dict[str, str]:
    """Run every compiler and return a manifest of generated files."""
    print("=" * 60)
    print("  Agents-of-SHIELD — Knowledge Compiler")
    print("=" * 60)

    results: dict[str, str] = {}

    # 1. Roles
    print("\n[1/3] Compiling roles from manifest.yaml ...")
    try:
        role_path = compile_roles(repo_root)
        results["role_index"] = str(role_path)
        print(f"  ✓ {role_path}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

    # 2. Skills
    print("\n[2/3] Compiling skills from Skills/ ...")
    try:
        skill_path = compile_skills(repo_root)
        results["skill_index"] = str(skill_path)
        print(f"  ✓ {skill_path}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

    # 3. Docs
    print("\n[3/3] Compiling docs ...")
    try:
        doc_paths = compile_docs(repo_root)
        for p in doc_paths:
            key = p.stem
            results[key] = str(p)
            print(f"  ✓ {p}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

    # Write build manifest
    manifest = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(repo_root),
        "outputs": results,
    }
    manifest_path = repo_root / "knowledge" / "compiled" / "build_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"  Build complete: {len(results)} artifacts")
    print(f"  Manifest: {manifest_path}")
    print(f"{'=' * 60}")

    return results


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
    build_all(root)
