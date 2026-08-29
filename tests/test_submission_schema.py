"""Validates that submissions/track1/*.csv match the exact schema required
by the hackathon's Track 1 submission format."""

import csv
import glob
import os
import unittest

REQUIRED_FIELDS = [
    "proband_id", "chrom_1", "pos_1", "ref_1", "alt_1",
    "chrom_2", "pos_2", "ref_2", "alt_2", "epcr", "finding_type", "notes",
]
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSubmissionSchema(unittest.TestCase):
    def test_track1_csvs_match_schema(self):
        pattern = os.path.join(REPO_ROOT, "submissions", "track1", "*.csv")
        files = glob.glob(pattern)
        self.assertTrue(files, f"No Track 1 submission CSV found matching {pattern}")

        for path in files:
            with self.subTest(file=path):
                with open(path, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    self.assertEqual(
                        reader.fieldnames, REQUIRED_FIELDS,
                        f"{path}: header must be exactly {REQUIRED_FIELDS}",
                    )
                    rows = list(reader)
                    self.assertLessEqual(len(rows), 10, f"{path}: max 10 candidate rows allowed")
                    self.assertGreaterEqual(len(rows), 1, f"{path}: at least one row required")

                    for row in rows:
                        self.assertIn(row["finding_type"], ("primary", "secondary"),
                                      f"{path}: finding_type must be primary/secondary, got {row['finding_type']!r}")
                        epcr = float(row["epcr"])
                        self.assertTrue(0 < epcr <= 1, f"{path}: epcr must be in (0, 1], got {epcr}")
                        self.assertTrue(row["chrom_1"].startswith("chr"),
                                         f"{path}: chrom_1 must use 'chr' prefix, got {row['chrom_1']!r}")
                        if row["chrom_2"]:
                            self.assertTrue(row["chrom_2"].startswith("chr"),
                                             f"{path}: chrom_2 must use 'chr' prefix, got {row['chrom_2']!r}")


if __name__ == "__main__":
    unittest.main()
