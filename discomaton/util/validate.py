#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Various validation bits and pieces.

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

from discord import embeds

__all__ = ('FormatError', 'validate_embed', 'validate_message')


class FormatError(ValueError):
    """Message formatting error."""

    def __init__(self, reason: str) -> None:
        """
        Init this formatting error.
        :param reason: the reason for the error.
        """
        self.reason = reason

    def __str__(self) -> str:
        """
        Get the string representation of this error.
        """
        return self.reason

    __repr__ = __str__


def _len_validation(content: str,
                    *,
                    min_l: int = 0,
                    max_l: int,
                    name: str,
                    acceptable: typing.Iterable = None) -> None:
    """
    Validates a string. Used internally to make error checking more concise.

    :param content: the content to check.
    :param min_l: the non-inclusive minimum length of stripped content.
    :param max_l: the inclusive max length of unstripped code.
    :param name: the element name to use in any error message.
    :param acceptable: acceptable values to allow regardless (iterable).
    :raises: FormatError if any checks fail.
    """
    if acceptable and content in acceptable:
        return

    cropped = content.strip()

    if len(cropped) <= min_l:
        raise FormatError(f'{name} cannot be shorter than '
                          f'{min_l + 1} characters. This excludes '
                          'padding whitespace.')
    elif len(cropped) > max_l:
        raise FormatError(f'{name} cannot be longer than '
                          f'{max_l} characters. This includes padding '
                          f'whitespace. The given field is {len(cropped)} '
                          'characters wide.')


def validate_message(message: str) -> None:
    """
    Validates the given string message to determine if it is a valid Discord
    message body.
    :param message: the message body to validate
    :raises: FormatError if validation fails.
    """
    _len_validation(message, max_l=2000, name='Message content')


# noinspection PyProtectedMember
def validate_embed(embed: embeds.Embed) -> None:
    """
    Validates the given embed message to determine if it is a valid embed.

    https://discordapp.com/developers/docs/resources/channel#embed-limits

    :param embed: the embed to validate.
    :raises: FormatError if validation fails.
    """
    total_length = 0

    def add_len(x):
        nonlocal total_length
        if x is not embeds.EmptyEmbed and x is not None:
            total_length += len(x)

    _len_validation(
        embed.title,
        max_l=256,
        name='Embed title',
        acceptable=[embeds.EmptyEmbed])
    add_len(embed.title)

    _len_validation(
        embed.description,
        max_l=2048,
        name='Embed description',
        acceptable=[embeds.EmptyEmbed])
    add_len(embed.title)

    if len(embed.fields) >= 25:
        raise FormatError('Embed can only have up to 25 fields.')

    fields = getattr(embed, '_fields', [])

    for i in range(0, len(fields)):
        field = fields[i]
        name, value = field['name'], field['value']
        add_len(name)
        add_len(value)
        _len_validation(name, max_l=256, name=f'Name in field {i} (0 based)')
        _len_validation(value, max_l=1024,
                        name=f'Value in field {i} (0 based)')

    if hasattr(embed, '_footer'):
        add_len(embed._footer.get('text', ''))
        _len_validation(
            embed._footer.get('text', ''),
            max_l=2048,
            name='Embed footer text')

    if hasattr(embed, '_author'):
        add_len(embed._author.get('name', ''))
        _len_validation(
            embed._author.get('name', ''),
            max_l=2048,
            name='Embed author name')

    if total_length > 6000:
        raise FormatError('Total embed length cannot exceed 6000 characters.')
