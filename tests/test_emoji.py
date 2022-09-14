# stdlib
import ast
import codecs
import io
from itertools import starmap
from textwrap import dedent
from typing import Callable, Dict

# 3rd party
import pytest

try:
	from emoji.unicode_codes.en import EMOJI_UNICODE_ENGLISH  # type: ignore
except ImportError:
	try:
		from emoji.unicode_codes import get_emoji_unicode_dict
		EMOJI_UNICODE_ENGLISH = get_emoji_unicode_dict("en")
	except ImportError:
		from emoji.unicode_codes import get_unicode_dict  # type: ignore[attr-defined]
		EMOJI_UNICODE_ENGLISH = get_unicode_dict("en")

# this package
from emoji_strings import StreamReader, decode


def _param(name: str, symbol: str):
	return pytest.param(name, symbol, id=name)


@pytest.mark.parametrize("emoji_name, emoji_symbol", starmap(_param, EMOJI_UNICODE_ENGLISH.items()))
def test_emoji(emoji_name: str, emoji_symbol: str):

	source = dedent("""\
	def foo():
		print({}"An emoji: {}")
	""")

	expected = source.format('', emoji_symbol)
	assert decode(source.format('g', emoji_name).encode("UTF-8"))[0] == expected

	assert codecs.decode(source.format('g', emoji_name).encode("UTF-8"), "emoji-strings") == expected
	assert source.format('g', emoji_name).encode("UTF-8").decode("emoji-strings")

	reader = StreamReader(io.BytesIO(source.format('g', emoji_name).encode("UTF-8")))
	assert reader.read() == expected


def test_multiple_emoji():
	source = dedent("""\
	def foo():
		print(g'Starting :package:')
		print(g'Done :rocket:')
	""").encode("UTF-8")

	expected = dedent("""\
	def foo():
		print('Starting 📦')
		print('Done 🚀')
	""")

	assert decode(source)[0] == expected


def test_ast_parse(capsys):
	globalns: Dict[str, Callable] = {}

	source = dedent(
			"""\
	# -*- coding: emoji_strings -*-
	def foo():
		print(g'Starting :package:')
		print(g'Done :rocket:')
	"""
			).encode("UTF-8")

	tree = ast.parse(source)

	exec(compile(tree, "code.py", "exec"), globalns)

	assert "foo" in globalns

	globalns["foo"]()

	assert capsys.readouterr().out.split('\n') == [
			"Starting 📦",
			"Done 🚀",
			'',
			]


def test_ast_parse_raw(capsys):
	globalns: Dict[str, Callable] = {}

	source = dedent(
			"""\
	# coding: emoji-strings
	def foo():
		print(g'Starting :package:')
		print(rg"¯\\_(ツ)_/¯")
		print(g'Done :rocket:')
	"""
			).encode("UTF-8")

	tree = ast.parse(source)

	exec(compile(tree, "code.py", "exec"), globalns)

	assert "foo" in globalns

	globalns["foo"]()

	assert capsys.readouterr().out.split('\n') == [
			"Starting 📦",
			"¯\\_(ツ)_/¯",
			"Done 🚀",
			'',
			]
