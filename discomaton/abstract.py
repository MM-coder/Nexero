#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Abstract iterator base type.

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
import abc
import asyncio
import collections
import types
import typing

__all__ = ('AbstractIterableMachine',)

IterRetT = typing.TypeVar('IterRetT')


class AbstractIterableMachine(abc.ABC,
                              collections.AsyncIterable):
    """
    A reusable asynchronous iterable state machine. This is a basic
    abstract implementation that should be derived from when defining simple
    state machine objects. This is a disposable iterator instance, and can
    be used inside an asynchronous context manager to enable application of
    a condition. This enables other co-routines to await the completion of this
    async iterator.

    Correct usage should be:

    .. code-block:: python
       # Suppose IterableMachine is an implementation of
       # AbstractIterableMachine.
       iter = IterableMachine()
       async with iter:
           async for _ in iter:
               pass

       result = iter.some_result

    Other co-routines can then await the result of this like so:

    .. code-block:: python
       await iter
    """

    def __init__(self) -> None:
        self._condition = asyncio.Condition()

    def __aiter__(self) -> typing.AsyncIterator[IterRetT]:
        """
        Returns an iterator over this machine, forcing it to change state or do
        some form of meaningful work.
        """
        return self

    async def __aenter__(self) -> 'AbstractIterableMachine':
        """
        Acquires a lock on this iterator. This allows other co-routines
        to await our completion.
        """
        await self._condition.acquire()
        return self

    async def __aexit__(self,
                        exc_type: typing.Optional[typing.Type[BaseException]],
                        exc_val: typing.Optional[BaseException],
                        exc_tb: typing.Optional[types.TracebackType]) -> None:
        """
        Releases our lock.
        :param exc_type: Exception type that was raised.
        :param exc_val: Exception that was raised.
        :param exc_tb: Traceback.
        """
        if self._condition.locked:
            self._condition.notify_all()
            self._condition.release()

    def __await__(self) -> typing.Awaitable:
        """
        Awaits the completion of this iterator.

        :raises: RuntimeError if we have not yet started. This is to prevent
            deadlocking other co-routines if for whatever reason, this object
            never starts iterating.
        """
        return self.await_for(None)

    def await_for(self, timeout: typing.Optional[float]) -> typing.Awaitable:
        """
        Awaits the completion of this iterator.

        :param timeout: the timeout to wait for before raising
            `asyncio.TimeoutError`.
        :raises: RuntimeError if we have not yet started. This is to prevent
            deadlocking other co-routines if for whatever reason, this object
            never starts iterating.
        """

        async def awaitable():
            nonlocal self
            async with self._condition:
                await self._condition.wait(timeout=timeout)
            return self

        return awaitable()

    def is_running(self):
        """
        Return true if the iterator has acquired its lock, or false if
        we assume the lock is released, and the iterator has finished, or
        has yet to start.
        """
        return self._condition.locked

    @abc.abstractmethod
    async def __anext__(self) -> IterRetT:
        """
        Changes the state of the machine. Raises AsyncStopIteration at the end.
        """
        pass
