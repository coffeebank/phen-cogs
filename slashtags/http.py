import logging
from typing import List

import discord
from redbot.core.bot import Red

log = logging.getLogger("red.phenom4n4n.slashtags.http")


class Route(discord.http.Route):
    BASE = "https://discord.com/api/v8"


class SlashHTTP:
    def __init__(self, cog):
        self.cog = cog
        self.bot = cog.bot
        self.request = cog.bot.http.request

    @property
    def application_id(self):
        return self.cog.application_id

    def add_slash_command(self, command: dict):
        route = Route(
            "POST", "/applications/{application_id}/commands", application_id=self.application_id
        )
        return self.request(route, json=command)

    def edit_slash_command(self, command_id: int, command: dict):
        route = Route(
            "PATCH",
            "/applications/{application_id}/commands/{command_id}",
            application_id=self.application_id,
            command_id=command_id,
        )
        return self.request(route, json=command)

    def remove_slash_command(self, command_id: int):
        route = Route(
            "DELETE",
            "/applications/{application_id}/commands/{command_id}",
            application_id=self.application_id,
            command_id=command_id,
        )
        return self.request(route)

    def get_slash_commands(self):
        route = Route(
            "GET", "/applications/{application_id}/commands", application_id=self.application_id
        )
        return self.request(route)

    def put_slash_commands(self, commands: list):
        route = Route(
            "PUT", "/applications/{application_id}/commands", application_id=self.application_id
        )
        return self.request(route, json=commands)

    def add_guild_slash_command(self, guild_id: int, command: dict):
        route = Route(
            "POST",
            "/applications/{application_id}/guilds/{guild_id}/commands",
            application_id=self.application_id,
            guild_id=guild_id,
        )
        return self.request(route, json=command)

    def edit_guild_slash_command(self, guild_id: int, command_id: int, command: dict):
        route = Route(
            "PATCH",
            "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            application_id=self.application_id,
            guild_id=guild_id,
            command_id=command_id,
        )
        return self.request(route, json=command)

    def remove_guild_slash_command(self, guild_id: int, command_id: int):
        route = Route(
            "DELETE",
            "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            application_id=self.application_id,
            guild_id=guild_id,
            command_id=command_id,
        )
        return self.request(route)

    def get_guild_slash_commands(self, guild_id: int):
        route = Route(
            "GET",
            "/applications/{application_id}/guilds/{guild_id}/commands",
            application_id=self.application_id,
            guild_id=guild_id,
        )
        return self.request(route)

    def put_guild_slash_commands(self, guild_id: int, commands: list):
        route = Route(
            "PUT",
            "/applications/{application_id}/guilds/{guild_id}/commands",
            application_id=self.application_id,
            guild_id=guild_id,
        )
        return self.request(route, json=commands)

    def send_message(
        self,
        token: str,
        interaction_id: int,
        *,
        type: int,
        initial_response: bool,
        content: str = None,
        embed: discord.Embed = None,
        embeds: List[discord.Embed] = [],
        tts: bool = False,
        allowed_mentions: discord.AllowedMentions = None,
        flags: int = None,
    ):
        payload = {"type": type}

        if embed is not None:
            embeds = [embed]
        if allowed_mentions is None:
            allowed_mentions = self.bot.allowed_mentions

        data = {}
        if content:
            data["content"] = content
        if tts:
            data["tts"] = True
        if embeds:
            data["embeds"] = [e.to_dict() for e in embeds]
        if allowed_mentions:
            data["allowed_mentions"] = allowed_mentions.to_dict()
        if flags:
            data["flags"] = flags
        if embeds:
            data["embeds"] = [e.to_dict() for e in embeds]
        if flags:
            data["flags"] = flags
        if data:
            data["allowed_mentions"] = allowed_mentions.to_dict()
            payload["data"] = data

        if initial_response:
            url = "/interactions/{interaction_id}/{token}/callback"
            send_data = payload
        else:
            url = "/webhooks/{application_id}/{token}"
            send_data = data
        route = Route(
            "POST",
            url,
            interaction_id=interaction_id,
            token=token,
            application_id=self.application_id,
        )

        log.debug(f"sending response, initial = {initial_response}: {send_data}")
        return self.request(route, json=send_data)

    def edit_message(
        self,
        token: str,
        message_id: int,
        *,
        content: str = None,
        embed: discord.Embed = None,
        embeds: List[discord.Embed] = None,
        allowed_mentions: discord.AllowedMentions = None,
    ):
        route = Route(
            "PATCH",
            "/webhooks/{application_id}/{token}/messages/{message_id}",
            application_id=self.application_id,
            token=token,
            message_id=message_id,
        )
        if embed is not None:
            embeds = [embed]
        if allowed_mentions is None:
            allowed_mentions = self.bot.allowed_mentions

        payload = {}
        if content:
            payload["content"] = content
        if embeds:
            payload["embeds"] = [e.to_dict() for e in embeds]
        payload["allowed_mentions"] = allowed_mentions.to_dict()

        return self.request(route, json=payload)

    def delete_message(self, token: str, message_id: str):
        route = Route(
            "DELETE",
            "/webhooks/{application_id}/{token}/messages/{message_id}",
            application_id=self.application_id,
            token=token,
            message_id=message_id,
        )
        return self.request(route)
