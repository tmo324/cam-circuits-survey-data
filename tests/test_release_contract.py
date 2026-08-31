# Verify the public-release files and README links stay connected.
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseContractTests(unittest.TestCase):
    def test_required_public_release_files_exist(self):
        required = [
            ".github/workflows/ci.yml",
            ".github/workflows/secret-scan.yml",
            "CODE_OF_CONDUCT.md",
            "REPRODUCIBILITY.md",
            "SECURITY.md",
            "THIRD_PARTY_NOTICES.md",
            "pyproject.toml",
        ]
        missing = []
        for path in required:
            if not (ROOT / path).is_file():
                missing.append(path)

        self.assertEqual(missing, [])

    def test_readme_uses_the_project_house_style(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        required = [
            '<h1 align="center">CAM Circuits Survey</h1>',
            'actions/workflows/ci.yml/badge.svg',
            'actions/workflows/secret-scan.yml/badge.svg',
            "REPRODUCIBILITY.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "THIRD_PARTY_NOTICES.md",
        ]
        missing = []
        for text in required:
            if text not in readme:
                missing.append(text)

        self.assertEqual(missing, [])

    def test_makefile_exposes_standard_release_targets(self):
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        targets = ["install:", "install-test:", "test:", "check:", "paper:"]
        missing = []
        for target in targets:
            if target not in makefile:
                missing.append(target)

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
