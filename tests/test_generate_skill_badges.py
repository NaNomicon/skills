import pathlib
import subprocess
import sys
import tempfile
import textwrap
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "generate_skill_badges.py"


class GenerateSkillBadgesTests(unittest.TestCase):
    def test_generator_creates_svg_badges_with_safe_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = pathlib.Path(temp_dir)
            repo_root = temp_path / "repo"
            repo_root.mkdir()

            for skill_name in ("dokploy-admin", "tilth"):
                skill_dir = repo_root / skill_name
                skill_dir.mkdir()
                (skill_dir / "SKILL.md").write_text(
                    textwrap.dedent(
                        f"""\
                        ---
                        name: {skill_name}
                        description: Example skill
                        ---
                        """
                    ),
                    encoding="utf-8",
                )

            fixtures = {
                "https://skills.sh/NaNomicon/skills/dokploy-admin": """
                    <html><body>
                    <h1>dokploy-admin</h1>
                    <div>Weekly Installs</div>
                    <div>128</div>
                    <div>Security Audits</div>
                    <div>Gen Agent Trust Hub</div><div>Pass</div>
                    <div>Socket</div><div>Fail</div>
                    <div>Snyk</div><div>Pass</div>
                    </body></html>
                """,
                "https://skills.sh/NaNomicon/skills/tilth": """
                    <html><body>
                    <h1>tilth</h1>
                    <div>Skill not found</div>
                    </body></html>
                """,
                "https://skills.sh/api/search?q=tilth": """
                    {
                      "skills": [
                        {"name": "something-else", "repo": "NaNomicon/skills", "url": "https://skills.sh/NaNomicon/skills/something-else"}
                      ]
                    }
                """,
            }
            fixtures_path = temp_path / "fixtures.json"
            fixtures_path.write_text(
                __import__("json").dumps(fixtures), encoding="utf-8"
            )

            output_dir = repo_root / "badges"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--repo-root",
                    str(repo_root),
                    "--output-dir",
                    str(output_dir),
                    "--source-repo",
                    "NaNomicon/skills",
                    "--fixtures",
                    str(fixtures_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)

            installs_badge = (
                output_dir / "dokploy-admin" / "weekly-installs.svg"
            ).read_text(encoding="utf-8")
            self.assertIn(">weekly installs<", installs_badge.lower())
            self.assertIn(">128<", installs_badge)

            audit_badge = (
                output_dir / "dokploy-admin" / "security-audit.svg"
            ).read_text(encoding="utf-8")
            self.assertIn(">security audit<", audit_badge.lower())
            self.assertIn(">fail<", audit_badge.lower())

            unknown_installs_badge = (
                output_dir / "tilth" / "weekly-installs.svg"
            ).read_text(encoding="utf-8")
            self.assertIn(">unknown<", unknown_installs_badge.lower())

            unlisted_badge = (output_dir / "tilth" / "listing-status.svg").read_text(
                encoding="utf-8"
            )
            self.assertIn(">unlisted<", unlisted_badge.lower())

            manifest = (output_dir / "manifest.json").read_text(encoding="utf-8")
            self.assertIn('"dokploy-admin"', manifest)
            self.assertIn('"tilth"', manifest)


if __name__ == "__main__":
    unittest.main()
