#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Button data type. Corresponds to a reaction on Discord.

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

import cached_property
import discord

from .abstract import AbstractIterableMachine

__all__ = ('Button', 'as_button')

callback_t = typing.Callable[
    [
        'Button',
        AbstractIterableMachine,
        discord.Reaction,
        discord.User
    ],
    typing.Any
]


class Button:
    """
    Data-type for a button. This is essentially a representation that is
    translated to a message react in Discord.

    :param name: sentinel name for a button.
    :param reaction: the reaction to use for the button.
    :param callback: the co-routine to call. This should take four parameters:
            this button, the abstract machine it relates to, the
            discord.Reaction and the discord.User. Whatever this co-routine
            returns is what the button will output back to the implementation
            of async iterator being used, and returned.
    """

    def __init__(self,
                 name: str,
                 reaction: str,
                 callback: callback_t) -> None:
        self.name, self.reaction, self.callback = name, reaction, callback
        self._predicates = set()
        self.__doc__ = getattr(callback, '__doc__', '')

    async def __call__(self,
                       machine: AbstractIterableMachine,
                       reaction: discord.Reaction,
                       user: discord.User) -> typing.Any:
        """Calls the coroutine callback and returns the result."""
        return await self.callback(self, machine, reaction, user)

    def __str__(self) -> str:
        """User-friendly representation."""
        return self.name

    def __repr__(self) -> str:
        """Machine-friendly representation."""
        return (
            f'<Button name={self.name!r}, reaction={self.reaction!r}, '
            f'callback={self.callback!r}>'
        )

    @cached_property.cached_property
    def help(self) -> str:
        """
        Gets the docstring for the button, if there is one. This is the
        docstring of the callback given to the constructor. If there is not
        one, we return a falsy emptystring.
        """
        import inspect
        return inspect.cleandoc(inspect.getdoc(self))

    def should_show(self, machine: AbstractIterableMachine) -> bool:
        """
        An overridable check that can be used to determine whether or not
        to show this specific button in the current state. For example, if
        we only have one page. By default, this returns True. Either override
        this method or set the predicate using the should_show_predicate
        decorator.
        """
        return all(p(machine) for p in self._predicates)

    def with_predicate(self,
                       predicate: typing.Callable[
                           [AbstractIterableMachine],
                           bool
                       ]) -> typing.Callable:
        """
        Decorates a predicate and sets the predicate. See `should_show` for
        more information.
        """
        self._predicates.add(predicate)

        return predicate

    should_show_predicate = with_predicate


def as_button(*,
              name: typing.Optional[str] = None,
              reaction: str,
              predicate: typing.Callable[
                  [AbstractIterableMachine],
                  bool
              ] = lambda _: True) -> typing.Callable[[callback_t], Button]:
    """Decorator for a co-routine to generate a new Button type."""

    def decorator(coro: callback_t) -> Button:
        nonlocal name
        if name is None:
            name = coro.__name__
        btn = Button(name, reaction, coro)
        btn.with_predicate(predicate)
        return btn

    return decorator
