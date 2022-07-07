#!/usr/bin/env python3
"""
Filename: minion_meister.py
Authors:  Yoshi Fu
Project:  Minion Meister Discord Bot
Date:     July 24th 2022

Summary:
- MinionMeister class that handles database calls.
- Add and remove users from the database.
- Select a random winner from the participands of a server.
- Show how many times every participant has become Minion Meister.
- [TODO]
"""

import error
import tools


class MinionMeister:
    """ Create a Minion Meister Object that handles database calls.

        [TODO]
    """
    def __init__(self, database_filename: str) -> None:
        """ Initialise the database to connect to. """
        self.database = database_filename

    async def add_user(self, server_id: int, user_id: int,
                       display_name: str) -> None:
        """ Add user to the database.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.
                :display_name: str, required
                    display name of the user.

            Returns:
                None

            Raises:
                InsertError, if record already exists.
        """
        if await self._in_users_(server_id, user_id):
            raise error.InsertError(f'User {display_name} is already participating.')
        await self._insert_user_(server_id, user_id, display_name)
        await self._initialise_count_(server_id, user_id)

    async def remove_user(self, server_id: int, user_id: int,
                          display_name: str) -> None:
        """ Remove user from the database.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.
                :display_name: str, required
                    display name of the user.

            Returns:
                None

            Raises:
                DeleteError, if record does not exist.
        """
        if not await self._in_users_(server_id, user_id):
            raise error.DeleteError(f'User {display_name} is not participating.')
        await self._delete_user_(server_id, user_id)

    async def select_winner(self, server_id: int) -> int:
        """ Select a random user in the participants list.

            Parameters:
                :server_id: int, required
                    unique id of the server.

            Returns:
                :user_id:
                    unique id of the user.

            Raises:
                NoParticipantsError, if there are no participants.
        """
        user_id = await self._select_winner_(server_id)
        await self._update_history_(server_id, user_id)
        await self._update_count_(server_id, user_id)
        return user_id

    async def show_participants(self, server_id: int) -> list:
        """ List all participants in the server.

            Parameters:
                :server_id: int, required
                    unique id of the server.

            Returns:
                :names:
                    list with the names of all participants.

            Raises:
                NoParticipantsError, if there are no participants.
        """
        names = await self._list_participants_(server_id)
        names = [str(name[0]) for name in names]
        return names

    async def show_history(self, server_id: int, limit: int) -> tuple:
        """ Show the previous Minion Meisters of the server.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :limit: int, required
                    amount of history records to show (default: 5)

            Returns:
                :names:
                    list of previous Minion Meister names.
                :dates:
                    dates previous Minion Meister got chosen.

            Raises:
                NoMinionMeisterError, if there are no previous Minion Meisters.
        """
        if limit is None:
            limit = 5
        history = await self._list_history(server_id, limit)
        names, dates = zip(*history)
        return names, dates

    async def show_count(self, server_id: int) -> tuple:
        """ Show how many times the participants became Minion Meister.

            Parameters:
                :server_id: int, required
                    unique id of the server.

            Returns:
                :names:
                    list of previous Minion Meister names.
                :count:
                    amount of times the user got chosen as Minion Meister.

            Raises:
                NoMinionMeisterError, if there are no previous Minion Meisters.
        """
        result = await self._list_counts_(server_id)
        names, count = zip(*result)
        return names, count

    async def insert_history(self, server_id: int, user_id: int,
                             date: str) -> None:
        """ Insert a record with custom date into the history table.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.
                :date: str, required
                    date the user became Minion Meister.

            Returns:
                None
        """
        await self._insert_history_(server_id, user_id, date)
        await self._update_count_(server_id, user_id)

    async def delete_history(self, server_id: int, user_id: int,
                             date: str) -> None:
        """ Delete a record with date from the history table.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.
                :date: str, required
                    date the user became Minion Meister.

            Returns:
                None
        """
        await self._delete_history_(server_id, user_id, date)
        await self._update_count_(server_id, user_id, delete=True)

    async def is_user(self, server_id: int, user_id: int) -> bool:
        """ Check if a user is in the database for the given server.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.

            Returns:
                bool
        """
        return await self._in_users_(server_id, user_id)

    async def show_admins(self, server_id):
        """ List all admins in the server.

            Parameters:
                :server_id: int, required
                    unique id of the server.

            Returns:
                :names:
                    list with the names of all admins.

            Raises:
                NoParticipantsError, if there are no admins.
        """
        names = await self._list_admins_(server_id)
        names = [str(name[0]) for name in names]
        return names

    async def is_admin(self, server_id: int, user_id: int) -> bool:
        """ Check if the user is an admin of server with server_id.
            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.
            Returns:
                bool
        """
        return await self._in_admins_(server_id, user_id)

    async def admin_user(self, server_id: int, user_id: int,
                         display_name: str) -> None:
        """ Add user to admins of server with server_id.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.
                :display_name: str, required
                    display name of the user.

            Returns:
                None
        """
        if await self._in_admins_(server_id, user_id):
            raise error.InsertError(f'User {display_name} is already admin.')
        await self._insert_admin_(server_id, user_id)

    async def unadmin_user(self, server_id: int, user_id: int,
                           display_name: str) -> None:
        """ Remove user from admins of server with server_id.

            Parameters:
                :server_id: int, required
                    unique id of the server.
                :user_id: int, required
                    unique id of the user.
                :display_name: str, required
                    display name of the user.

            Returns:
                None
        """
        if not await self._in_admins_(server_id, user_id):
            raise error.DeleteError(f'User {display_name} is not an admin.')
        await self._delete_admin_(server_id, user_id)

    async def _insert_user_(self, server_id: int, user_id: int,
                            display_name: str) -> None:
        sql = (
            "INSERT INTO users (id, server, name) "
            "VALUES (?, ?, ?)"
        )
        values = (user_id, server_id, display_name)
        await tools.push_to_db(self.database, sql, values)

    async def _delete_user_(self, server_id: int, user_id: int) -> None:
        sql = (
            "DELETE FROM users "
            "WHERE server = (?) "
            "AND id = (?)"
        )
        values = (server_id, user_id)
        await tools.push_to_db(self.database, sql, values)

    async def _in_users_(self, server_id: int, user_id: int) -> bool:
        sql = (
            "SELECT EXISTS("
            "SELECT 1 "
            "FROM users "
            "WHERE server = (?) "
            "AND id = (?) "
            "LIMIT 1"
            ")"
        )
        values = (server_id, user_id)
        result = await tools.read_from_db(self.database, sql, values)
        return bool(result[0][0])

    async def _select_winner_(self, server_id: int) -> int:
        sql = (
            "SELECT id "
            "FROM users "
            "WHERE server = (?) "
            "ORDER BY RANDOM() "
            "LIMIT 1"
        )
        values = (server_id,)
        user_id = await tools.read_from_db(self.database, sql, values)
        if not user_id:
            raise error.NoParticipantsError
        return user_id[0][0]

    async def _list_participants_(self, server_id: int) -> list:
        sql = (
            "SELECT name "
            "FROM users "
            "WHERE server = (?) "
            "ORDER BY name ASC"
        )
        values = (server_id,)
        names = await tools.read_from_db(self.database, sql, values)
        if not names:
            raise error.NoParticipantsError
        return names

    async def _update_history_(self, server_id: int, user_id: int) -> None:
        sql = (
            "INSERT INTO history (server, user, date) "
            "VALUES (?, ?, DATE())"
        )
        values = (server_id, user_id)
        await tools.push_to_db(self.database, sql, values)

    async def _insert_history_(self, server_id: int, user_id: int,
                               date: str) -> None:
        sql = (
            "INSERT INTO history (server, user, date) "
            "VALUES (?, ?, ?)"
        )
        values = (server_id, user_id, date)
        await tools.push_to_db(self.database, sql, values)

    async def _delete_history_(self, server_id: int, user_id: int,
                               date: str) -> None:
        sql = (
            "DELETE FROM history "
            "WHERE server = (?) "
            "AND user = (?) "
            "AND date = (?)"
        )
        values = (server_id, user_id, date)
        await tools.push_to_db(self.database, sql, values)

    async def _list_history(self, server_id: int, limit: int) -> list:
        sql = (
            "SELECT users.name, history.date "
            "FROM history "
            "INNER JOIN users ON history.user = users.id "
            "WHERE history.server = (?) "
            "ORDER BY date DESC "
            "LIMIT (?)"
        )
        values = (server_id, limit)
        history = await tools.read_from_db(self.database, sql, values)
        if not history:
            raise error.NoMinionMeisterError
        return history

    async def _initialise_count_(self, server_id: int, user_id: int) -> None:
        sql = (
            "INSERT OR IGNORE INTO counts (server, user, count) "
            "VALUES (?, ?, ?)"
        )
        values = (server_id, user_id, 0)
        await tools.push_to_db(self.database, sql, values)

    async def _update_count_(self, server_id: int, user_id: int,
                             delete: bool = False) -> None:
        sql = (
            "UPDATE counts "
            "SET count = count + 1 "
            "WHERE server = (?) "
            "AND user = (?)"
        )
        if delete:
            sql = (
                "UPDATE counts "
                "SET count = count - 1 "
                "WHERE server = (?) "
                "AND user = (?)"
            )
        values = (server_id, user_id)
        await tools.push_to_db(self.database, sql, values)

    async def _list_counts_(self, server_id: int) -> list:
        sql = (
            "SELECT users.name, counts.count "
            "FROM counts "
            "INNER JOIN users ON counts.user = users.id "
            "AND counts.server = users.server "
            "WHERE counts.server = (?) "
            "ORDER BY counts.count DESC"
        )
        values = (server_id,)
        counts = await tools.read_from_db(self.database, sql, values)
        if not counts:
            raise error.NoMinionMeisterError
        return counts

    async def _list_admins_(self, server_id):
        sql = (
            "SELECT users.name "
            "FROM users "
            "INNER JOIN admins ON users.id = admins.user "
            "AND users.server = admins.server "
            "WHERE users.server = (?) "
            "ORDER BY name ASC"
        )
        values = (server_id,)
        names = await tools.read_from_db(self.database, sql, values)
        if not names:
            raise error.NoAdminsError
        return names

    async def _insert_admin_(self, server_id: int, user_id: int) -> None:
        sql = (
            "INSERT INTO admins (server, user) "
            "VALUES (?, ?)"
        )
        values = (server_id, user_id)
        await tools.push_to_db(self.database, sql, values)

    async def _delete_admin_(self, server_id: int, user_id: int) -> None:
        sql = (
            "DELETE FROM admins "
            "WHERE server = (?) "
            "AND user = (?)"
        )
        values = (server_id, user_id)
        await tools.push_to_db(self.database, sql, values)

    async def _in_admins_(self, server_id: int, user_id: int) -> bool:
        sql = (
            "SELECT EXISTS("
            "SELECT 1 "
            "FROM admins "
            "WHERE server = (?) "
            "AND user = (?) "
            "LIMIT 1"
            ")"
        )
        values = (server_id, user_id)
        result = await tools.read_from_db(self.database, sql, values)
        return bool(result[0][0])
