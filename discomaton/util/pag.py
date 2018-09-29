#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Additional pagination utilities and helpers.

===

MIT License

Copyright (c) 2018 Neko404NotFound

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import re
import typing

import cached_property
from discord.ext.commands import Paginator as RapptzPaginator

__all__ = ('Paginator', 'RapptzPaginator')


class DontAlter:
    """Used to prevent breaking up a piece of input to fit the page."""

    def __init__(self, bit):
        self.bit = bit

    def __str__(self):
        return str(self.bit)

    def __repr__(self):
        return repr(self.bit)

    def __len__(self):
        return len(self.bit)


class Paginator:
    """
    Consumes multi-line string input and cuts it into multiple "page" strings
    with a specified maximum character count. This is useful for splitting
    up strings into multiple chunks to send when each Message on Discord has a
    2K character limit.

    Similar to Danny/Rapptz's paginator, but we can check the value at any
    time,
    whether or not this is fully constructed yet. This also will attempt to
    make a string fit by splitting on common breaking characters such as
    hyphens, spaces, tabs, newlines, etc if needbe. This originally used
    Danny's
    paginator but it became too complicated to work with, so it was easier to
    write my own implementation.

    Note: this does not implement any buttons. It purely formats our string.

    This also accepts a max_lines argument to specify the maximum number of
    lines to allow per page.

    This effectively functions by refusing to produce the page output until
    we actually request it. Then it is cached until the next time the object
    contents are modified.

    :param max_chars: maximum characters to allow per page.
    :param max_lines: maximum lines to allow per page (precedence over
            max_chars, optional, defaults to 20 lines).
    :param prefix: a string to prefix each page content with. Defaults to ''
    :param suffix: a string to suffix each page content with. Defaults to ''
    :param _unused_line_sep: deprecated.

    Note that the max number of lines takes into account page content only.
    """
    # Sentinel value to represent a place to manually break the page on.
    _page_break = object()

    def __init__(self,
                 max_chars: int = 2000,
                 max_lines: typing.Optional[int] = 20,
                 prefix: str = '',
                 suffix: str = '',
                 _unused_line_sep: str = None) -> None:

        assert max_lines is None or 0 < max_lines <= max_chars

        # Holds the bits of string to put together when we generate pages.
        self._bits = []
        self._max_chars = max_chars
        self._max_lines = max_lines if max_lines is not None else max_chars -1
        self._prefix = prefix
        self._suffix = suffix

    @cached_property.cached_property
    def pages(self) -> typing.Tuple[str]:
        pages = []

        max_len = self._max_chars - len(self._prefix) - len(self._suffix) - 2
        max_lns = self._max_lines - (
                self._prefix + self._suffix).count('\n') + 1

        if max_len <= 0:
            raise ValueError(f'The max character count ({self._max_chars}) is '
                             'too short to produce pages with the given '
                             'suffix and prefix. Please choose a larger '
                             'value.')

        current_page = ''
        current_lines = 0

        # Separate bits on spaces, keeping spaces.
        bits = []

        # This ensures that we are more likely to split on a space than we are
        # mid word, if possible.
        for bit in self._bits:
            if not isinstance(bit, DontAlter) and bit is not self._page_break:
                bit = str(bit)
                while ' ' in bit:
                    first_bit, space, rest = bit.partition(' ')
                    bits.append(first_bit + space)
                    bit = rest
            bits.append(bit)

        def finish_page():
            """Finalises the current page, moves onto the next."""
            nonlocal current_page, current_lines

            if current_page:
                pages.append(current_page)
                current_page = ''
                current_lines = 0

        for bit, strbit in map(lambda b: (b, str(b)), bits):
            if bit is self._page_break:
                finish_page()
                continue

            # We must not alter this section by splitting it.
            if isinstance(bit, DontAlter):
                no_chars = len(strbit)
                no_lines = strbit.count('\n')

                if no_chars > max_len:
                    raise RuntimeError(f'Cannot fit `{strbit}` onto one page, '
                                       'and it is marked as DontAlter. '
                                       'TOO MANY CHARACTERS')
                elif no_lines > max_lns:
                    raise RuntimeError(f'Cannot fit `{strbit}` onto one page, '
                                       'and it is marked as DontAlter. '
                                       'TOO MANY LINES')

                new_len = no_chars + len(current_page)
                new_lns = no_lines + current_lines

                if new_len > max_len:
                    finish_page()
                elif 0 < max_lns < new_lns:
                    finish_page()

            for char in strbit:
                if char == '\n' and current_lines == max_lns:
                    finish_page()

                    # We cant safely add this character ever without
                    # hitting an infinite loop.
                    if max_lns <= 0:
                        continue
                elif char == '\n':
                    current_lines += 1

                elif len(current_page) == max_len:
                    finish_page()

                current_page += char

        finish_page()

        pages = map(lambda p: f'{self._prefix}\n{p}\n{self._suffix}', pages)
        return tuple(pages)

    def _invalidate(self) -> None:
        """Invalidates the pages cache if any exists."""
        if 'pages' in self.__dict__ and self.__dict__['pages']:
            del self.__dict__['pages']

    def __len__(self) -> int:
        """Returns the raw input length before pagination."""
        return sum(len(bit) for bit in self._bits)

    def add_raw(self, obj: typing.Any, *,
                to_start: bool = False,
                dont_alter: bool = False) -> None:
        """
        Same as `add`, but no string casting takes place.
        :param obj: the object to add.
        :param to_start: defaults to false, if true then we prepend.
        :param dont_alter: if true, it prevents this element being split or
            reformatted to fit the page. This may cause errors if lines are too
            long, but it enables maintaining any formatting. This does not
            guarantee that lines will be kept, only other separators.
        """
        if not obj:
            return

        if dont_alter:
            obj = DontAlter(obj)

        self._invalidate()

        if to_start:
            self._bits.insert(0, obj)
        else:
            self._bits.append(obj)

    def add(self, obj: typing.Any, *,
            to_start: bool = False,
            dont_alter: bool = False) -> None:
        """
        Add a string. Content cannot be more than the max length, otherwise
        it may be mis-formatted or rejected.

        :param obj: the object to stringify.
        :param to_start: defaults to false. If true, we prepend instead of
            append this item.
        :param dont_alter: if true, it prevents this element being split or
            reformatted to fit the page. This may cause errors if lines are too
            long, but it enables maintaining any formatting. This does not
            guarantee that lines will be kept, only other separators.
        """

        string = str(obj) if obj is not self._page_break else obj
        self.add_raw(string, to_start=to_start, dont_alter=dont_alter)

    def add_line(self, obj: typing.Any, *,
                 to_start: bool = False,
                 _unused_dont_alter: bool = False) -> None:
        """Adds a string, and a new line."""
        if to_start:
            self.add('\n', to_start=True)

            for line in reversed(str(obj).splitlines(keepends=True)):
                self.add(line, to_start=True)
        else:
            for line in str(obj).splitlines(keepends=True):
                self.add(line)
            self.add('\n')

    def add_break(self, *,
                  to_start: bool = False) -> None:
        """Inserts in a page break."""
        self.add(self._page_break, to_start=to_start)
