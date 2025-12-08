# stdlib
import ast
import codecs
import io
from itertools import starmap
from textwrap import dedent
from typing import Any, Callable, Dict

# 3rd party
import pytest

try:
	# 3rd party
	from emoji.unicode_codes.en import EMOJI_UNICODE_ENGLISH  # type: ignore[import-not-found]
except ImportError:
	# 3rd party
	from emoji.unicode_codes import EMOJI_DATA, LANGUAGES, STATUS

	_EMOJI_UNICODE: Dict[str, Any] = {lang: None for lang in LANGUAGES}

	def get_emoji_unicode_dict(lang: str) -> Dict:
		if _EMOJI_UNICODE[lang] is None:
			_EMOJI_UNICODE[lang] = {
					data[lang]: emj
					for emj,
					data in EMOJI_DATA.items()
					if lang in data and data["status"] <= STATUS["fully_qualified"]
					}

		return _EMOJI_UNICODE[lang]

	EMOJI_UNICODE_ENGLISH = get_emoji_unicode_dict("en")

# this package
from emoji_strings import StreamReader, decode


def _param(name: str, symbol: str):  # noqa: MAN002
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
