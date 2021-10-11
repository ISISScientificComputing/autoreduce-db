# ############################################################################### #
# Autoreduction Repository : https://github.com/ISISScientificComputing/autoreduce
#
# Copyright &copy; 2021 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""Tests for the ReductionRun class."""
# pylint:disable=no-member
from django.test import TestCase

from autoreduce_db.reduction_viewer.models import ReductionRun


class TestReductionRun(TestCase):
    """Directly tests the message handling classes."""
    fixtures = [
        "autoreduce_db/autoreduce_django/fixtures/status_fixture.json",
        "autoreduce_db/autoreduce_django/fixtures/run_with_multiple_variables.json"
    ]

    def setUp(self) -> None:
        self.reduction_run = ReductionRun.objects.first()
        return super().setUp()

    def test_title(self):
        """Test that retrieving the status returns the expected one."""
        assert self.reduction_run.title() == "123456"

    def test_title_multiple_run_numbers(self):
        """Test that retrieving the status returns the expected one."""
        self.reduction_run.run_numbers.create(run_number=123457)
        assert self.reduction_run.title() == "Batch 123456 → 123457"

    def test_run_number(self):
        """Test that retrieving the status returns the expected one."""
        assert self.reduction_run.run_number == 123456

    def test_run_number_multiple_run_numbers(self):
        """Test that retrieving the status returns the expected one."""
        self.reduction_run.run_numbers.create(run_number=123457)
        with self.assertRaises(ValueError):
            self.reduction_run.run_number
        assert [run.run_number for run in self.reduction_run.run_numbers.all()] == [123456, 123457]
