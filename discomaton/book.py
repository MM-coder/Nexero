#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Implementation of an interactive button/reaction driven pagination control.
"""
import abc
import asyncio
import collections
import logging
import random
import traceback
import typing

import discord
from discord.ext import commands as discord_cmds

from .abstract import AbstractIterableMachine
from .button import Button, as_button
from .util import validate
from .util.helpers import attempt_delete
from .util.stack import Stack

__all__ = ('default_buttons', 'default_formatter', 'AbstractBooklet',
           'StringBooklet', 'EmbedBooklet', 'FormatterType')

PageType = typing.TypeVar('PageType')
PagesType = typing.Union[
    typing.Tuple[PageType],
    typing.List[PageType]]
CheckType = typing.Callable[[discord.Reaction, discord.User], bool]
FormatterType = typing.Callable[['AbstractBooklet'], str]

# Can be reassigned if we need to do something else for debugging.
in_future = asyncio.ensure_future


def default_buttons() -> typing.List[Button]:
    """
    Generates some default buttons in a list to use for books.
    """
    buttons = []

    def _as_button(**kwargs) -> typing.Callable:
        def decorator(coro: typing.Callable) -> Button:
            button = as_button(**kwargs)(coro)
            buttons.append(button)
            return button

        return decorator

    @_as_button(name='Go to the first page', reaction='⏮')
    async def go_to_start(_unused_button: Button,
                          machine: 'AbstractBooklet',
                          _unused_reaction: discord.Reaction,
                          _unused_user: discord.User) -> None:
        # print('|<<')
        await machine.set_page_index(0)

    @_as_button(name='Go back 10 pages', reaction='⏪')
    async def go_back_10_pages(_unused_button: Button,
                               machine: 'AbstractBooklet',
                               _unused_reaction: discord.Reaction,
                               _unused_user: discord.User) -> None:
        minimum = 0
        current = machine.page_index
        await machine.set_page_index(max(minimum, current - 10))

    @_as_button(name='Previous page', reaction='◀')
    async def previous_page(_unused_button: Button,
                            machine: 'AbstractBooklet',
                            _unused_reaction: discord.Reaction,
                            _unused_user: discord.User) -> None:
        # print('<-')
        await machine.move_forwards_by(-1)

    """
    @_as_button(name='Let anyone control this', reaction='🔓')
    async def unlock(_unused_button: Button,
                     machine: 'AbstractBooklet',
                     _unused_reaction: discord.Reaction,
                     _unused_user: discord.User) -> None:
        machine.only_author = False
    """

    @_as_button(name='Enter a page number', reaction='🔢')
    async def enter_page(_unused_button: Button,
                         machine: 'AbstractBooklet',
                         _usused_reaction: discord.Reaction,
                         user: discord.User) -> None:
        from .userinput import get_user_input

        setattr(machine, '_is_showing_page_prompt', True)

        def predicate(message):
            if not message.content.isdigit():
                return False
            elif machine.only_author and user != machine.author:
                return False
            else:
                page = int(message.content)
                return 1 < page <= len(machine.pages)

        prompt = await machine.channel.send('Enter a page number:')
        msg = None

        # noinspection PyProtectedMember
        async def later_callback():
            nonlocal msg
            try:
                msg = await get_user_input((machine.channel, machine.client),
                                           only_if=predicate,
                                           timeout=30)
            except asyncio.TimeoutError:
                await machine.channel.send('Took too long.', delete_after=10)
            else:
                page_number = int(msg.content)
                await machine.set_page_number(page_number)
            finally:
                await (attempt_delete(prompt, msg) if msg else attempt_delete(prompt))
                setattr(machine, '_is_showing_page_prompt', False)
                await machine._flush_reacts()

        return in_future(later_callback())

    """
    @_as_button(name='Show help', reaction='❓')
    async def show_help(_unused_button: Button,
                        machine: 'AbstractBooklet',
                        _unused_reaction: discord.Reaction,
                        whom: discord.User) -> None:
        explanation = []
        for button in machine.buttons.values():
            explanation.append(f'{button.reaction} → {button.name}')

        assert len(explanation), 'No buttons?'

        help_embed = discord.Embed(
            title='Discomaton Pagination for Casino',
            description=f'@{whom.name}#{whom.discriminator}! Here are the '
                        'basics for using this control:',
            colour=random.randint(0, 0xFFFFFF))

        help_embed.add_field(name='Buttons',
                             value='\n'.join(explanation[:len(explanation) // 2]))
        help_embed.add_field(name='\u200B',
                             value='\n'.join(explanation[len(explanation) // 2:]))

        help_embed.set_footer(
            text='At the time of showing this help message, '
                 f'{"only the author" if machine.only_author else "anyone"} '
                 'is allowed control the book above by using reactions.')
        root_resp = await machine.root_resp

        if root_resp.embeds:
            m = await root_resp.channel.send(embed=help_embed)
            machine.response_stk.push(m)
        else:
            await root_resp.edit(embed=help_embed)

        setattr(machine, '_help_shown', True)
    """

    @_as_button(name='Next page', reaction='▶')
    async def next_page(_unused_button: Button,
                        machine: 'AbstractBooklet',
                        _unused_reaction: discord.Reaction,
                        _unused_user: discord.User) -> None:
        # print('->')
        await machine.move_forwards_by(1)

    @_as_button(name='Go forwards 10 pages', reaction='⏩')
    async def go_forwards_10_pages(_unused_button: Button,
                                   machine: 'AbstractBooklet',
                                   _unused_reaction: discord.Reaction,
                                   _unused_user: discord.User) -> None:
        maximum = len(machine)
        current = machine.page_number
        await machine.set_page_number(min(maximum, current + 10))

    @_as_button(name='Go to the last page', reaction='⏭')
    async def go_to_end(_unused_button: Button,
                        machine: 'AbstractBooklet',
                        _unused_reaction: discord.Reaction,
                        _unused_user: discord.User) -> None:
        # print('>>|')
        await machine.set_page_index(-1)

    @_as_button(name='Delete message',
                reaction='\N{REGIONAL INDICATOR SYMBOL LETTER X}')
    async def delete(_unused_button: Button,
                     machine: 'AbstractBooklet',
                     _unused_reaction: discord.Reaction,
                     _unused_user: discord.User) -> None:
        await machine.clear_stack()
        await machine.initial_message.delete()
        raise StopAsyncIteration

    """
    @show_help.with_predicate
    def help_show_if(machine: 'AbstractBooklet') -> bool:
        return not hasattr(machine, '_help_shown')
    """

    @go_to_start.with_predicate
    @previous_page.with_predicate
    @next_page.with_predicate
    @go_to_end.with_predicate
    @enter_page.with_predicate
    @go_back_10_pages.with_predicate
    @go_forwards_10_pages.with_predicate
    def multiple_pages_only(machine: 'AbstractBooklet') -> bool:
        return len(machine) > 1

    """
    @unlock.with_predicate
    def show_unlock_iff(machine: 'AbstractBooklet') -> bool:
        return machine.only_author
    """

    @go_back_10_pages.with_predicate
    @go_forwards_10_pages.with_predicate
    def ten_or_more_pages(machine: 'AbstractBooklet') -> bool:
        return len(machine) >= 30

    @enter_page.with_predicate
    def only_one_prompt_at_once(machine: 'AbstractBooklet') -> bool:
        return not getattr(machine, '_is_showing_page_prompt', False)

    return buttons


def default_formatter(self: 'AbstractBooklet') -> str:
    return f'**[{self.page_number:,}/{len(self):,}]**\n'


class AbstractBooklet(AbstractIterableMachine,
                      abc.ABC,
                      typing.Generic[PageType]):
    """
    Abstract class type for a type of booklet. Most of the logic for booklets
    is defined here. The only thing that is not implemented is how to format
    and send the pages, and their concrete data-type. This allows defining a
    book that uses embeds, messages, etc.

    :param buttons: the buttons to show. There must be at least one.
    :param ctx: the context to respond to. Pass a tuple of Message, TextChannel,
            and discord.Client or discord.ext.commands.Bot if for any reason
            you cannot pass an actual Context object (e.g. are using this
            in some event handler rather than a command).
    :param timeout: the timeout in seconds to wait for during inactivity before
            destroying the pagination. Defaults to 300s (5 mins).
    :param only_author: defaults to true. If true, then the pagination
            only responds to the author. If false, the pagination responds
            to any user who interacts with it.
    :param pages: the pages to show in the book.
    :param start_page: the page index to start on. Defaults to 0.
    :param formatter: a unary function that takes `self` as a parameter and
            outputs the string representing the current page number string
            to prepend to the page body. If this will not fit in a single
            Discord message neatly due to lack of space, it is omitted for
            pages on an individually assessed basis.
            Defaults to a unary function returning `Page x of y`

    Attributes
    ----------
    timeout: float
        The timeout to wait for a positive event before closing the book.
    channel: discord.TextChannel
        The channel to send output to.
    initial_message: discord.Message
        The message the user sent that triggered this book to be output.
    only_author: bool
        True if only the initial author can manipulate this object's state.
        False otherwise.
    buttons: OrderedDict[str, Button]
        An ordered dictionary mapping reaction emojis to button callback objects
        to call when their respective event is invoked.
    response_stk: Stack[discord.Message]
        A stack of responses this class has sent to the user. A stack is used
        to ensure the most recent item maintains focus.
    pages: Tuple[PageType]
        A tuple of the pages to access.
    page_number: int
        The current page number. This is 1-indexed.
    page_index: int
        The current page index. This is 0-indexed.
    client: discord.Client
        The bot client that generated this object. This determines which bot
        instance, if multiple exist, we listen to events on.
    iterations: int
        The number of iterations that have been performed.
    formatter: Callable[[AbstractBooklet], str]
        The current page number formatter.
    """
    buttons: typing.Iterable[Button]
    pages: PagesType
    client: discord.Client
    initial_message: discord.Message
    channel: discord.TextChannel
    response_stk: Stack[discord.Message]
    timeout: float
    start_page: int
    only_author: bool
    iterations: int
    formatter: FormatterType

    def __init__(self,
                 *,
                 buttons: typing.List[Button],
                 pages: typing.List[PageType],
                 ctx: typing.Union[
                     discord_cmds.Context,
                     typing.Tuple[
                         discord.Message,
                         discord.TextChannel,
                         discord.Client
                     ]],
                 timeout: typing.Optional[float] = 300,
                 start_page: int = 0,
                 only_author: bool = True,
                 formatter: FormatterType = default_formatter
                 ) -> None:
        """
        Initialise the booklet.
        """
        super().__init__()
        self.logger = logging.getLogger(__class__.__qualname__)

        self.iterations = 0
        self.formatter = formatter

        self.timeout = timeout
        self.pages: typing.Sequence[PageType] = tuple(pages)

        # From here, use `page_index` to change the page.
        try:
            self.__current_page = pages[0]
            self.__page_index = 0
            self._page_index = start_page
        except IndexError:
            raise IndexError('Expected at least one page') from None
        except TypeError:
            raise IndexError('Expected a sequence of pages') from None

        if isinstance(ctx, discord_cmds.Context):
            self.initial_message = ctx.message
            self.channel = ctx.channel
            self.client = ctx.bot
        else:
            self.initial_message, self.channel, self.client = ctx

        if self.initial_message.guild is None:
            raise discord_cmds.NoPrivateMessage(
                'Cannot add buttons to a book in a DM.')

        self.only_author = only_author

        # Maps string reactions to their corresponding buttons.
        self.buttons: typing.Dict[str, Button] = collections.OrderedDict()
        for button in buttons:
            # noinspection PyUnresolvedReferences
            self.buttons[button.reaction] = button

        self.response_stk: Stack[discord.Message] = Stack()
           
    async def set_starting_page_number(self, number):
        self._page_number = number
        self.__current_page = self.pages[number]

    @property
    def loading_message(self) -> str:
        """Message to show when loading."""
        return self.current_page

    @property
    def author(self) -> discord.User:
        """Gets the author of the invocation."""
        return self.initial_message.author

    @property
    def me(self) -> discord.ClientUser:
        """Gets my user."""
        return self.client.user

    @property
    def _page_index(self) -> int:
        """Gets the page index."""
        return self.__page_index

    def __getitem__(self, index: int) -> int:
        """Index operator. Acts as a 0-indexed list access."""
        return self.pages[index]

    def __index__(self) -> int:
        """Gets an index. This is the page index we are currently on."""
        return self.page_index

    def __int__(self) -> int:
        """Gets a number. This is the page number we are currently on."""
        return self.page_number

    @property
    def page_index(self) -> int:
        """Gets the page index."""
        return self._page_index

    @_page_index.setter
    def _page_index(self, index: int) -> None:
        """Sets the page index. You must then synchronise this with Discord."""
        # We use the length of pages as a condition to prevent infinite looping
        # if the user changes this to have zero pages.
        if not self.pages:
            raise ValueError('Must have at least one page.')

        # Enables us to wrap around the front and back of the book seamlessly.
        while index < 0:
            index += len(self.pages)
        while index >= len(self.pages):
            index -= len(self.pages)

        self.__page_index = index
        self.__current_page = self.pages[index]

    @property
    async def root_resp(self) -> discord.Message:
        """
        The root response is the Message we send to Discord that buttons are
        applied to.

        This can be overridden if messages are sent before the root
        response. If there is no root response, we send a placeholder
        message which is updated as soon as we sync.
        """
        try:
            return self.response_stk[0]
        except IndexError:
            # We lost the reference to the original message, sadly.
            msg = await self.channel.send(self.loading_message)
            self.root_resp = msg
            return msg

    @root_resp.setter
    def root_resp(self, value: discord.Message) -> None:
        if self.response_stk:
            self.response_stk[0] = value
        else:
            self.response_stk.push(value)

    @property
    def _page_number(self) -> int:
        """Gets the page number, which is 1-indexed."""
        return self._page_index + 1

    @property
    def page_number(self) -> int:
        """Gets the page number, which is 1-indexed."""
        return self._page_number

    @_page_number.setter
    def _page_number(self, number: int) -> None:
        """Sets the page number. You must then synchronise this with Discord"""
        if 0 < number <= len(self.pages):
            self._page_index = number - 1
        else:
            raise IndexError(f'{number} is outside range [1,{len(self.pages)}]')

    def __len__(self):
        """Gets the number of pages in this booklet."""
        return len(self.pages)

    def __index__(self):
        """Gets the current page index."""
        return self._page_index

    async def set_page_index(self, index: int) -> None:
        """
        Sets the page index and updates the object on Discord.

        This will automatically wrap around if negative or greater than the
        book length.
        """
        self._page_index = index
        await self.sync()

    async def set_page_number(self, number: int) -> None:
        """
        Sets the page number and updates the object on Discord.
        This will not wrap around.
        """
        self._page_number = number
        await self.sync()

    async def move_forwards_by(self, pages: int) -> None:
        """
        Attempts to move forwards the given number of pages. If this is
        negative, then we reverse.
        """
        await self.set_page_index(self.page_index + pages)

    @property
    def current_page(self) -> PageType:
        """Gets the current page we are set to display on sync."""
        return self.__current_page

    def _is_reaction_valid(self,
                           reaction: discord.Reaction,
                           user: discord.User) -> bool:
        """
        Internal predicate used to determine whether or not to acknowledge this
        event as a potential change of state. If this returns True, then
        we process this event, otherwise we continue waiting until we get a
        positive event, or timeout is reached. If you want to enforce custom
        behaviours, this is the method to edit to do so.

        This corresponds to the (on_)reaction_add event that Discord.py will
        dispatch.

        The implementation provided here returns True if and only if:

            1. The message reacted to is the initial message.
            2. The reaction is added by the initial message author, OR
                `only_author` is False.
            3. The reaction is a valid registered button.
            4. The user IS NOT A BOT ACCOUNT. This prevents potential looping
                between this bot and another bot.

        :param reaction: reaction of the event.
        :param user: the member/user that triggered the event.
        :return: True if we should respond to this event, False otherwise.
        """
        if not self.response_stk:
            return False
        root = self.response_stk[0]

        if not root:
            return False

        if user == self.client.user:
            return False

        if self.only_author:
            is_valid_author = user.id == self.initial_message.author.id
        else:
            is_valid_author = True

        is_same_message = reaction.message.id == root.id
        is_valid_button = reaction.emoji in self.buttons
        is_not_bot = not user.bot

        return all((
            is_same_message, is_valid_author, is_valid_button, is_not_bot))

    async def clear_stack(self) -> None:
        """Clears all messages on the message stack and deletes them."""
        await attempt_delete(*self.response_stk)
        while self.response_stk:
            self.response_stk.pop()

    async def delete(self) -> None:
        """Deletes all output."""
        await self.clear_stack()

    async def clear_except_root(self) -> None:
        """
        Clears all messages on the message stack and deletes them,
        except for the root element.
        """
        while len(self.response_stk) > 1:
            await attempt_delete(self.response_stk.pop())

    async def __update_root(self):
        """Gets a more up to date copy of the root message metadata."""

        async def up():
            self.root_resp = await self.channel.get_message((await self.root_resp).id)

        self.client.loop.create_task(up())

    async def __initialise_reacts(self):
        """Initialises the reacts, and awaits them to be present."""
        for react in self.buttons:
            await (await self.root_resp).add_reaction(react)

    async def __aenter__(self):
        """Initialises the message."""
        await self.sync()
        return await super().__aenter__()

    async def __aexit__(self, *args, **kwargs):
        """Deinitialises everything."""
        if self.response_stk:
            await self.clear_except_root()
        if self.response_stk:
            # Provides a background fail safe check to prevent unhandled
            # exceptions from occurring.
            in_future(self._maybe_clear_reactions())

        return await super().__aexit__(*args, **kwargs)

    async def _maybe_add_reaction(self, reaction) -> None:
        """Only adds the reaction if we are able to. Otherwise, we ignore."""
        try:
            root = await self.root_resp
            # In this case, it is easier to ask for forgiveness than
            # permission.
            await root.add_reaction(reaction)
        except BaseException as ex:
            self.logger.debug(f'IGNORING API ERROR {type(ex).__name__}: {ex}')

    async def _maybe_clear_reactions(self) -> None:
        try:
            msg = await self.channel.get_message((await self.root_resp).id)
            if msg:
                await msg.clear_reactions()
        except BaseException as ex:
            self.logger.debug(f'IGNORING API ERROR {type(ex).__name__}: {ex}')

    async def _flush_reacts(self) -> None:
        """
        Reorders and removes any non applicable reacts.

        This takes a brute-force approach.
        """
        # print('flush')

        # Delay slightly to enable discord to catch up. Ensure to update the
        # root otherwise we won't know what reacts we need to clear.
        await asyncio.gather(
            asyncio.sleep(0.1),
            self.__update_root()
        )

        root = await self.root_resp

        # Actual reacts that exist on Discord
        curr_reacts = root.reactions

        # Expected clean state. We filter non-applicable reacts out based on
        # the current state. The list contains the emoji strings to expect.
        targets: typing.List[str] = []
        for button in self.buttons.values():
            if button.should_show(self):
                targets.append(button.reaction)

        assert targets, 'No buttons'

        try:
            for curr in curr_reacts:
                # If the current react doesn't match the one at the list head,
                # then we assume it should not be here, so we remove it. If we
                # have got to the end of our targets list, we assume everything
                # else is garbage, and thus we delete it.
                if not targets or curr.emoji != targets[0]:
                    async for user in curr.users():
                        await root.remove_reaction(curr, user)

                # If there are still targets left to check and the current
                # reaction is the next target, remove all reacts that are not by
                # me.
                elif curr.emoji == targets[0]:
                    targets.pop(0)
                    async for user in curr.users():
                        # Ignore our own react. We want to keep that.
                        if user == self.me:
                            continue

                        await root.remove_reaction(curr, user)
        except BaseException as ex:
            traceback.print_exc()
            # Any exception and we should just stop.
            raise StopAsyncIteration(ex)
        else:
            # If we did not validate all targets by now, we know they are
            # missing and should be added
            while targets:
                in_future(self._maybe_add_reaction(targets.pop(0)))

    async def __anext__(self) -> None:
        """Returns the next result."""
        try:
            flush_future = in_future(self._flush_reacts())

            reaction, user = await self.client.wait_for(
                'reaction_add',
                check=self._is_reaction_valid,
                timeout=self.timeout)

            await flush_future
            await (await self.root_resp).remove_reaction(reaction, user)
            await self.buttons[reaction.emoji](self, reaction, user)

        except asyncio.TimeoutError:
            self.logger.debug('TIMEOUT HIT')
            raise StopAsyncIteration
        except discord.Forbidden as ex:
            # noinspection PyBroadException
            try:
                await self.clear_stack()
                await self.channel.send(
                    'I am missing permissions to display this correctly...\n\n'
                    'If you are the server owner, make sure that I can:\n'
                    ' - React to messages (`ADD_REACTIONS`)\n'
                    ' - Manage other users messages (`MANAGE_MESSAGES`)\n'
                    ' - Use external emojis (`USE_EXTERNAL_EMOJIS`).')
            except BaseException:
                traceback.print_exc()
            finally:
                raise StopAsyncIteration(ex)

    def start(self) -> typing.Awaitable:
        """
        Ensures a future that iterates across this object until it is
        exhausted. This can be awaited, or ignored to run concurrently. If
        awaited, then it will not return until the loop finishes.
        """

        async def runner():
            # Invoke initial sending
            await self.root_resp
            async with self:
                async for _ in self:
                    pass

        return in_future(runner())

    @abc.abstractmethod
    async def sync(self) -> typing.Optional[typing.Any]:
        """
        Synchronises this state with Discord.

        This has the following expectations:
        - This first calls `_sync_message`
        - If a message does not exist, we create it.
        - Any message that is created is pushed onto the stack.
        - Any message that is deleted is popped from the stack.
        - If a message is not found, we clear all buttons and de-init this
            paginator. If that fails, we ignore it. An AsyncStopIteration is
            raised regardless of the outcome.
        - If an operation is forbidden by Discord, we clear all buttons and
            de-init this paginator. If that fails, we die silently. An
            AsyncStopIteration is raised regardless of the outcome.
        - Any other error is allowed to propagate out of this co-routine.
        - Setting the page index, page number, or offset will eventually call
            this method.
        - This will decorate any messages being sent if appropriate. For
            example, by adding the page number to the message, etc. This is only
            done if there is space to do so.
        - This method validates the page content length before sending. A
            ValueError signifies that a page is invalid.
        - This can return something, but that is up to the implementation.
        """
        raise NotImplementedError


class StringBooklet(AbstractBooklet, typing.Generic[typing.AnyStr]):
    """
    A booklet that contains raw strings for each page.

    :param buttons: the buttons to show. There must be at least one.
    :param ctx: the context to respond to. Pass a tuple of Message, TextChannel,
            and discord.Client or discord.ext.commands.Bot if for any reason
            you cannot pass an actual Context object (e.g. are using this
            in some event handler rather than a command).
    :param timeout: the timeout in seconds to wait for during inactivity before
            destroying the pagination. Defaults to 300s (5 mins).
    :param only_author: defaults to true. If true, then the pagination
            only responds to the author. If false, the pagination responds
            to any user who interacts with it.
    :param pages: the pages to show in the book.
    :param start_page: the page index to start on. Defaults to 0.
    :param formatter: a unary function that takes `self` as a parameter and
            outputs the string representing the current page number string
            to prepend to the page body. If this will not fit in a single
            Discord message neatly due to lack of space, it is omitted for
            pages on an individually assessed basis.
            Defaults to a unary function returning `Page x of y`

    Attributes
    ----------
    timeout: float
        The timeout to wait for a positive event before closing the book.
    channel: discord.TextChannel
        The channel to send output to.
    initial_message: discord.Message
        The message the user sent that triggered this book to be output.
    only_author: bool
        True if only the initial author can manipulate this object's state.
        False otherwise.
    buttons: OrderedDict[str, Button]
        An ordered dictionary mapping reaction emojis to button callback objects
        to call when their respective event is invoked.
    response_stk: Stack[discord.Message]
        A stack of responses this class has sent to the user. A stack is used
        to ensure the most recent item maintains focus.
    pages: Tuple[PageType]
        A tuple of the pages to access.
    page_number: int
        The current page number. This is 1-indexed.
    page_index: int
        The current page index. This is 0-indexed.
    client: discord.Client
        The bot client that generated this object. This determines which bot
        instance, if multiple exist, we listen to events on.
    iterations: int
        The number of iterations that have been performed.
    formatter: Callable[[AbstractBooklet], str]
        The current page number formatter.
    """

    def __init__(self,
                 *,
                 buttons: typing.List[Button] = default_buttons(),
                 pages: PagesType,
                 ctx: typing.Union[
                     discord_cmds.Context,
                     typing.Tuple[
                         discord.Message,
                         discord.TextChannel,
                         discord.Client
                     ]],
                 timeout: float = 300,
                 start_page: int = 0,
                 only_author: bool = True,
                 formatter: FormatterType = default_formatter) -> None:
        super().__init__(buttons=buttons,
                         pages=pages,
                         ctx=ctx,
                         timeout=timeout,
                         start_page=start_page,
                         only_author=only_author,
                         formatter=formatter)

    async def sync(self):
        """
        Synchronises this state with Discord.

        This has the following expectations:
        - This first calls `_sync_message`
        - If a message does not exist, we create it.
        - Any message that is created is pushed onto the stack.
        - Any message that is deleted is popped from the stack.
        - If a message is not found, we clear all buttons and de-init this
            paginator. If that fails, we ignore it. An AsyncStopIteration is
            raised regardless of the outcome.
        - If an operation is forbidden by Discord, we clear all buttons and
            de-init this paginator. If that fails, we die silently. An
            AsyncStopIteration is raised regardless of the outcome.
        - Any other error is allowed to propagate out of this co-routine.
        - Setting the page index, page number, or offset will eventually call
            this method.
        - This will decorate any messages being sent if appropriate. For
            example, by adding the page number to the message, etc. This is only
            done if there is space to do so.
        - This method validates the page content length before sending. A
            ValueError signifies that a page is invalid.
        - This can return something, but that is up to the implementation.
        """
        # print('Syncing')
        current_page = self.current_page

        # Generate the page numbering string. Then we know whether we have
        # enough space.
        page_indicator = self.formatter(self)
        curr_pg_with_number = page_indicator + current_page
        if len(curr_pg_with_number) < 2000:
            current_page = curr_pg_with_number
        del curr_pg_with_number

        validate.validate_message(current_page)

        validate.validate_message(current_page)

        root = await self.root_resp
        in_future(root.edit(content=current_page))


class EmbedBooklet(AbstractBooklet):
    """
    A booklet that contains an embed for each page.

    NOTE:
        As of 17th March 2018, desktop Discord clients have a bug where
        updating an embed value on Discord's side can lead to embed contents
        appearing corrupted with data from the previous string. This is nothing
        to do with this code, as far as I know, as the embed can be fixed by
        simply changing out of the channel and changing back in.

    :param buttons: the buttons to show. There must be at least one.
    :param ctx: the context to respond to. Pass a tuple of Message, TextChannel,
            and discord.Client or discord.ext.commands.Bot if for any reason
            you cannot pass an actual Context object (e.g. are using this
            in some event handler rather than a command).
    :param timeout: the timeout in seconds to wait for during inactivity before
            destroying the pagination. Defaults to 300s (5 mins).
    :param only_author: defaults to true. If true, then the pagination
            only responds to the author. If false, the pagination responds
            to any user who interacts with it.
    :param pages: the pages to show in the book.
    :param start_page: the page index to start on. Defaults to 0.
    :param formatter: a unary function that takes `self` as a parameter and
            outputs the string representing the current page number string
            to prepend to the page body. If this will not fit in a single
            Discord message neatly due to lack of space, it is omitted for
            pages on an individually assessed basis.
            Defaults to a unary function returning `Page x of y`

    Attributes
    ----------
    timeout: float
        The timeout to wait for a positive event before closing the book.
    channel: discord.TextChannel
        The channel to send output to.
    initial_message: discord.Message
        The message the user sent that triggered this book to be output.
    only_author: bool
        True if only the initial author can manipulate this object's state.
        False otherwise.
    buttons: OrderedDict[str, Button]
        An ordered dictionary mapping reaction emojis to button callback objects
        to call when their respective event is invoked.
    response_stk: Stack[discord.Message]
        A stack of responses this class has sent to the user. A stack is used
        to ensure the most recent item maintains focus.
    pages: Tuple[PageType]
        A tuple of the pages to access.
    page_number: int
        The current page number. This is 1-indexed.
    page_index: int
        The current page index. This is 0-indexed.
    client: discord.Client
        The bot client that generated this object. This determines which bot
        instance, if multiple exist, we listen to events on.
    iterations: int
        The number of iterations that have been performed.
    formatter: Callable[[AbstractBooklet], str]
        The current page number formatter.
    """

    def __init__(self,
                 *,
                 buttons: typing.List[Button] = default_buttons(),
                 pages: PagesType,
                 ctx: typing.Union[
                     discord_cmds.Context,
                     typing.Tuple[
                         discord.Message,
                         discord.TextChannel,
                         discord.Client
                     ]],
                 timeout: float = 300,
                 start_page: int = 0,
                 only_author: bool = True,
                 formatter: FormatterType = default_formatter) -> None:
        super().__init__(buttons=buttons,
                         pages=pages,
                         ctx=ctx,
                         timeout=timeout,
                         start_page=start_page,
                         only_author=only_author,
                         formatter=formatter)

    @property
    def loading_message(self):
        """
        Embeds have to be sent differently to messages, which breaks
        stuff. For now, let's just send a silly message.
        """
        return random.choice((
            'Reticulating splines',
            'Shrinking BIG DATA',
            'Waiting for Discord to unfreeze',
            'Waiting for Danny to release rewrite',
            'Phubbing bot accounts',
            'Separating reality from Wikiality',
            'Undatafying intrusive datafication',
            'Unemptying empty embeds automagically',
            'Executing fast-fourier transforms in the complex plane',
            'Updating Windows 10',
            'Still updating Windows 10',
            'Is Windows 10 even responding?',
            'Leaking tokens',
            'Leaking memory',
            'Ensuring substitution failure is not an error',
            'Deallocating allocators',
            'The neutrinos coming from the sun have mutating!',
            'Mogrifying SQL queries',
            'Downloading 12GB of TeXLive packages',
            'Ensuring futures',
            'Awaiting coroutines',
            'Some Java updater shit',
            'Activating Adobe CS5.5',
            'Atomically operating atomic operations',
            'Randomly generating pseudo random number generators',
            'Playing a game of ~~mersenne~~ twister with the bois',
            'Compiling Boost',
            'Looking for ways to use jQuery',
            'Propagating properties'
        ))

    async def sync(self) -> None:
        """
        Synchronises this state with Discord.

        This has the following expectations:
        - This first calls `_sync_message`
        - If a message does not exist, we create it.
        - Any message that is created is pushed onto the stack.
        - Any message that is deleted is popped from the stack.
        - If a message is not found, we clear all buttons and de-init this
            paginator. If that fails, we ignore it. An AsyncStopIteration is
            raised regardless of the outcome.
        - If an operation is forbidden by Discord, we clear all buttons and
            de-init this paginator. If that fails, we die silently. An
            AsyncStopIteration is raised regardless of the outcome.
        - Any other error is allowed to propagate out of this co-routine.
        - Setting the page index, page number, or offset will eventually call
            this method.
        - This will decorate any messages being sent if appropriate. For
            example, by adding the page number to the message, etc. This is only
            done if there is space to do so.
        - This method validates the page content length before sending. A
            ValueError signifies that a page is invalid.
        - This can return something, but that is up to the implementation.
        """
        # print('Syncing')
        current_page = self.current_page

        # Generate the page numbering string. Then we know whether we have
        # enough space.
        page_indicator = self.formatter(self)

        validate.validate_embed(current_page)
        root = await self.root_resp
        in_future(root.edit(content=page_indicator, embed=current_page))
