"""Guards against ever accidentally committing controlled-access data
(raw VCF/FASTQ/clinical documents) to this git repository, per the
Hackathon Data Transfer Agreement (redistribution prohibited)."""

import os
import subprocess
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN_SUFFIXES = (".vcf", ".vcf.gz", ".fastq", ".fastq.gz", ".fq.gz", ".docx", ".bam", ".cram")
FORBIDDEN_NAMES = (".env",)


class TestNoControlledDataTracked(unittest.TestCase):
    def test_git_tracked_files_exclude_controlled_data(self):
        result = subprocess.run(
            ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        )
        tracked = result.stdout.splitlines()

        offenders = [
            path for path in tracked
            if path.lower().endswith(FORBIDDEN_SUFFIXES) or os.path.basename(path) in FORBIDDEN_NAMES
        ]
        self.assertEqual(
            offenders, [],
            f"Controlled-access or secret files must never be committed: {offenders}",
        )


if __name__ == "__main__":
    unittest.main()
