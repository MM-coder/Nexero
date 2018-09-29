#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Stack implementation.

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
import collections
import typing

__all__ = ('Stack',)

StackType = typing.TypeVar('StackType')


class Stack(collections.Sequence, typing.Generic[StackType]):
    """Implementation of a stack."""

    def __init__(self,
                 items: typing.Optional[typing.Sequence[StackType]] = None) \
            -> None:
        """
        Initialise the stack.
        :param items: the items to add to the stack initially.
        """
        self._stack = []
        if items:
            self._stack.extend(items)

    def __len__(self) -> int:
        """Get the stack length."""
        return len(self._stack)

    def __iter__(self) -> typing.Iterator[StackType]:
        """Get an iterator across the stack."""
        return iter(self._stack)

    def __contains__(self, x: object) -> bool:
        """Determine if the given object is in the stack."""
        return x in self._stack

    def __getitem__(self, index: int) -> StackType:
        """
        Get the item at the given index in the stack. Zero implies
        the bottom of the stack (first in).
        """
        return self._stack[index]

    def __setitem__(self, index: int, value: object) -> None:
        """
        Sets the value of the item in the given position in the stack.
        :param index: the index to edit at.
        :param value: the value to edit at.
        """
        self._stack[index] = value

    def push(self, x: StackType) -> StackType:
        """Pushes the item onto the stack and returns it."""
        self._stack.append(x)
        return x

    def pop(self) -> StackType:
        """Pops from the stack."""
        return self._stack.pop()

    def flip(self) -> None:
        """Flips the stack into reverse order in place."""
        self._stack = list(reversed(self._stack))

    def __str__(self) -> str:
        """Gets the string representation of the stack."""
        return str(self._stack)

    def __repr__(self) -> str:
        """Gets the string representation of the stack."""
        return repr(self._stack)

    def __bool__(self) -> bool:
        """Returns true if the stack is non-empty."""
        return bool(self._stack)
