#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Factory classes and components to simplify making basic booklet objects.

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
import typing

import discord
import discord.ext.commands as discord_cmds

from .abstractfactory import AbstractFactory
from .. import button
from ..book import FormatterType, StringBooklet, default_buttons, default_formatter
from ..util import pag

__all__ = ("StringBookBinder",)


class StringBookBinder(AbstractFactory[str, StringBooklet]):
    """
    A factory for creating a string book.
    These calls can be chained. Many of the characteristics can be set with
    a function call, or using a keyword argument in the constructor. This is
    designed to suit your coding requirements, so that you can use whatever is
    neatest.
    Required parameters
    -------------------
    :param context: the context to use when building the booklet. This is
        required. If you do not have a context object, you may provide
        a tuple containing the sender `discord.Message`, the
        `discord.TextChannel` to reply on, and the `discord.Client` bot object.

    Optional parameters
    -------------------
    :param max_chars: maximum characters to allow per page. Defaults to 1998
        as per the implementation of Danny's paginator.
    :param max_lines: maximum lines to allow per page. If this is reached
        before the character count is, then we will start a new page. This is
        optional (if omitted, then we do not consider the line count on each
        page), but will default to 10 if unspecified.
    :param prefix: the prefix to prepend to each page.
    :param suffix: the suffix to append to each page.
    :param line_sep: deprecated.
    :param page_number_formatter: the page number formatter to use. Defaults
        to the default implementation of the book we are using.
    :param pag_class: the implementation of pag.Paginator to use, if you have
        defined your own derivative to use. Defaults to pag.Paginator.
    :param buttons: the buttons to use. If none are specified by the time the
        booklet is built, then we add the default button collection defined
        in `book.py`.
    :param timeout: the default timeout for zero positive interaction before
        the booklet destroys the pagination and decays into a message. Defaults
        to 300 seconds.
    :param start_page: the page number (1 based to start on. Defaults to 1.
    :param only_author: defaults to True. If true, only the author of the
        context can control the booklet object using the buttons. Otherwise,
        anyone can use it.
    """
    def __init__(
        self,
        context: typing.Union[
            discord_cmds.Context,
            typing.Tuple[discord.Message, discord.TextChannel, discord.Client],
        ],
        *,
        max_chars: int = 1998,
        max_lines: typing.Optional[int] = 10,
        prefix: str = "",
        suffix: str = "",
        line_sep=None,
        page_number_formatter: typing.Optional[FormatterType] = None,
        buttons: typing.Optional[typing.List[button.Button]] = None,
        timeout: typing.Optional[float] = 300,
        start_page: int = 1,
        only_author: bool = True,
        pag_class: typing.Type[pag.Paginator] = pag.Paginator,
    ):
        self._context = context
        self._paginator = pag_class(
            max_chars=max_chars,
            max_lines=max_lines,
            prefix=prefix,
            suffix=suffix,
            _unused_line_sep=line_sep,
        )
        self._page_number_formatter = page_number_formatter
        self._buttons: typing.List[button.Button] = buttons
        self._timeout = timeout
        self._start_page = start_page - 1
        self._only_author = only_author
    def with_respond_to_author_only(self, only_author=True) -> "StringBookBinder":
        """Sets whether to only respond to the author or not."""
        self._only_author = only_author
        return self
    def with_max_chars(self, count: int) -> "StringBookBinder":
        """Sets the maximum characters to allow per page."""
        self._paginator._max_chars = count
        return self
    def with_max_lines(self, count: typing.Optional[int]) -> "StringBookBinder":
        """
        Sets the maximum lines to allow per page. If `None` is given,
        we instead disable this check.
        """
        self._paginator._max_lines = count
        return self
    def with_timeout(self, timeout: float) -> "StringBookBinder":
        """Sets the timeout."""
        self._timeout = timeout
        return self
    def with_open_on_index(self, page_index: int) -> "StringBookBinder":
        """Sets the page to start on (zero based index)."""
        self._start_page = page_index
        return self
    def with_open_on_number(self, page_number: int) -> "StringBookBinder":
        """Sets the page to start on (one based index)."""
        self._start_page = page_number - 1
        return self
    def with_prefix(self, prefix: str) -> "StringBookBinder":
        """Sets the prefix. Returns this."""
        self._paginator._prefix = prefix
        return self
    def with_suffix(self, suffix: str) -> "StringBookBinder":
        """Sets the suffix. Returns this."""
        self._paginator._suffix = suffix
        return self
    def with_button(self, btn: button.Button) -> "StringBookBinder":
        """Adds a button. Returns this."""
        if self._buttons is None:
            self._buttons = []
        self._buttons.append(btn)
        return self
    def with_buttons(self, *btns: button.Button) -> "StringBookBinder":
        """Adds multiple buttons. Returns this."""
        for btn in btns:
            self.with_button(btn)
        return self
    def with_page_number_formatter(
        self, formatter: FormatterType
    ) -> "StringBookBinder":
        """
        Sets the page number formatter to use.
        :param formatter: the page number formatter.
        :return: this.
        """
        self._page_number_formatter = formatter
        return self
    def add_raw(
        self, obj: typing.Any, *, to_start: bool = False, dont_alter: bool = False
    ) -> "StringBookBinder":
        """
        Same as `add`, but no string casting takes place.
        :param obj: the object to add.
        :param to_start: defaults to false, if true then we prepend.
        :param dont_alter: if true, it prevents this element being split or
            reformatted to fit the page. This may cause errors if lines are too
            long, but it enables maintaining any formatting. This does not
            guarantee that lines will be kept, only other separators.
        :returns: this.
        """
        self._paginator.add(obj, to_start=to_start, dont_alter=dont_alter)
        return self
    def add(
        self,
        text: str,
        *,
        to_start: bool = False,
        empty_after: bool = False,
        dont_alter: bool = False,
    ) -> "StringBookBinder":
        """
        Adds a string of text to the internal paginator.
        :param text: the text to add.
        :param to_start: defaults to false. If true, this adds to the front
            of the paginator instead of at the end.
        :param empty_after: whether to add an additional empty line afterwards.
        :param dont_alter: if true, it prevents this element being split or
            reformatted to fit the page. This may cause errors if lines are too
            long, but it enables maintaining any formatting. This does not
            guarantee that lines will be kept, only other separators.
        :return: this.
        """
        text = str(text)
        if empty_after:
            text = text + "\n"
        self._paginator.add(text, to_start=to_start, dont_alter=dont_alter)
        return self
    def add_line(
        self,
        text: str,
        *,
        to_start: bool = False,
        empty_after: bool = False,
        dont_alter: bool = False,
    ) -> "StringBookBinder":
        """
        Adds a line of text to the internal paginator. This appends a newline
        onto the end of the string.
        :param text: the line of text to add.
        :param to_start: false by default, if true, this adds to the front.
        :param empty_after: whether to add a second empty line afterwards.
        :param dont_alter: if true, it prevents this element being split or
            reformatted to fit the page. This may cause errors if lines are too
            long, but it enables maintaining any formatting. This does not
            guarantee that lines will be kept, only other separators.
        :return: this.
        """
        text = str(text) + "\n"
        self.add(
            text, to_start=to_start, empty_after=empty_after, dont_alter=dont_alter
        )
        return self
    def add_break(self, *, to_start: bool = False) -> "StringBookBinder":
        """
        Adds a page break to the internal paginator.
        :param to_start: defaults to false. If true, we add to the
            start of the internal paginator rather than the end.
        :return: this.
        """
        self._paginator.add_break(to_start=to_start)
        return self
    # Originally misnamed this.
    add_page_break = add_break
    def build(self) -> StringBooklet:
        """Builds the StringBooklet object and returns it."""
        if not self._buttons:
            self._buttons = default_buttons()
        if not self._page_number_formatter:
            self._page_number_formatter = default_formatter
        sb = StringBooklet(
            buttons=self._buttons,
            pages=self._paginator.pages,
            ctx=self._context,
            timeout=self._timeout,
            start_page=self._start_page,
            only_author=self._only_author,
            formatter=self._page_number_formatter,
        )
        return sb
    def start(self) -> typing.Awaitable:
        """
        Builds the booklet and returns a future to it's execution loop that
        can optionally be awaited.
        """
        return self.build().start()
