# Based on future-fstrings
# https://github.com/asottile/future-fstrings/blob/master/tests/future_fstrings_test.py
# Copyright (c) 2017 Anthony Sottile

# stdlib
import io

# this package
from emoji_strings import StreamReader


def test_streamreader_does_not_error_on_construction():
	StreamReader(io.BytesIO(b"g'error:'"))
