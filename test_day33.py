"""Unit tests for the Day 33 First Bad Version challenge."""

import pytest

from day33 import first_bad_version


def test_finds_first_bad_version():
	bad_version = 37

	assert first_bad_version(100, lambda version: version >= bad_version) == bad_version


def test_search_uses_logarithmic_number_of_api_calls():
	checks = []

	def is_bad_version(version: int) -> bool:
		checks.append(version)
		return version >= 513

	assert first_bad_version(1_000, is_bad_version) == 513
	assert len(checks) <= 10


@pytest.mark.parametrize("version_count, bad_version", [(1, 1), (2, 1), (2, 2)])
def test_handles_boundary_versions(version_count: int, bad_version: int):
	assert first_bad_version(
		version_count, lambda version: version >= bad_version
	) == bad_version


def test_rejects_empty_version_range():
	with pytest.raises(ValueError, match="at least 1"):
		first_bad_version(0, lambda version: True)