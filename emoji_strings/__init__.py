#!/usr/bin/env python3
#
#  __init__.py
"""
Adds support for emoji-strings in Python, which convert emoji names into actual emoji.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on future-fstrings
#  Copyright (c) 2017 Anthony Sottile
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import codecs
import encodings
import io
from functools import lru_cache
from typing import List, Optional, Tuple

# 3rd party
import emoji
import tokenize_rt  # type: ignore

__all__ = ["decode", "register"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"

tokenize_rt._string_prefixes = frozenset("bfrug")

utf_8 = encodings.search_function("utf8")


class IncrementalDecoder(codecs.BufferedIncrementalDecoder):

	def _buffer_decode(
			self,
			input,  # noqa: A002  # pylint: disable=redefined-builtin
			errors,
			final,
			):  # pragma: no cover

		if final:
			return decode(input, errors)
		else:
			return '', 0


class StreamReader(utf_8.streamreader):  # type: ignore
	# decode is deferred to support better error messages
	_stream = None
	_decoded = False

	@property
	def stream(self):
		if not self._decoded:
			text, _ = decode(self._stream.read())  # type: ignore
			self._stream = io.BytesIO(text.encode("UTF-8"))
			self._decoded = True
		return self._stream

	@stream.setter
	def stream(self, stream):
		self._stream = stream
		self._decoded = False


def _is_g(token):
	prefix, _ = tokenize_rt.parse_string_literal(token.src)
	return 'g' in prefix.lower()


def _make_gstring(tokens):
	new_tokens = []

	for i, token in enumerate(tokens):
		if token.name == "STRING" and _is_g(token):
			prefix, s = tokenize_rt.parse_string_literal(token.src)

			for q in ('"' * 3, "'" * 3, '"', "'"):
				if s.startswith(q):
					s = s[len(q):len(s) - len(q)]
					break
			else:
				raise AssertionError("unreachable")

			parts = [q, s, q]

			if 'r' in prefix.lower():
				parts = [s.replace('\\', "\\\\") for s in parts]

			parts = [emoji.emojize(s) for s in parts]
			token = token._replace(src=''.join(parts))

		new_tokens.append(token)

	return new_tokens


def decode(
		input: bytes,  # noqa: A002  # pylint: disable=redefined-builtin
		errors: str = "strict",
		) -> Tuple[str, int]:
	"""
	Decode the given source as UTF-8 and convert emoji.

	:param input:
	:param errors:
	"""

	u, length = utf_8.decode(input, errors)
	tokens = tokenize_rt.src_to_tokens(u)

	to_replace: List[Tuple[int, Optional[int]]] = []
	start: Optional[int] = None
	end: Optional[int] = None
	seen_f: Optional[bool] = None

	for i, token in enumerate(tokens):
		if start is None:
			if token.name == "STRING":
				start, end = i, i + 1
				seen_f = _is_g(token)
		elif token.name == "STRING":
			end = i + 1
			seen_f |= _is_g(token)
		elif token.name not in tokenize_rt.NON_CODING_TOKENS:
			if seen_f:
				to_replace.append((start, end))
			start = end = seen_f = None

	for start, end in reversed(to_replace):
		tokens[start:end] = _make_gstring(tokens[start:end])

	return tokenize_rt.tokens_to_src(tokens), length


# codec api

codec_map = {
		name: codecs.CodecInfo(
				name=name,
				encode=utf_8.encode,
				decode=decode,
				incrementalencoder=utf_8.incrementalencoder,
				incrementaldecoder=IncrementalDecoder,
				streamreader=StreamReader,
				streamwriter=utf_8.streamwriter,
				)
		for name in ("emoji-strings", "emoji_strings", "gstrings")
		}


@lru_cache(1)
def register():  # pragma: no cover  # noqa: D103
	codecs.register(codec_map.get)


register()
