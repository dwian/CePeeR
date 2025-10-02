import discord
import random
import math
import csv
import os

from discord.ext import commands
from discord.commands import slash_command, Option
### from discord.commands import slash_command, Option


class Hustle(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="Einkommen für deine Wochenaufgaben", name="einkommen")
    @commands.has_role("Crew")
    #@commands.cooldown(1, 60, commands.BucketType.user)
    async def hustle(
        self,
        ctx, #discord.ApplicationContext 
        level: Option(int, min_value=1, max_value=10)
        ):
        occs = ("Solo",'Netrunner','Fixer',"Tech","MediTech","Corp","Rockerboy","Media","Lawman") ## Alle Charakterklassen
        occ = "" ## Zielklasse
        desc = "" ## Wochenbeschreibung
        amount = 0 ## Verdienst

        spieler = ctx.user
        mitglied = ctx.guild.get_member(spieler.id)
        rollenliste = mitglied.roles

        for x in rollenliste:
            for y in occs:
                if x.name == y:
                    occ = x.name
        ##print(f"{ctx.author.display_name} ist {occ}")
        incomeLevel = (math.ceil((level-1)/3))
        ##print(f"Level: {level} :::: Einkommensstufe: {incomeLevel}")
        roll = random.randint(1,6)    

        with open(r'materials/hustle.csv') as file:
            hustleLists = csv.reader(file, delimiter=';')
            for row in hustleLists:
                if row[0].replace("'", "") == occ and int(row[1]) == roll:
                    desc = row[2]
                    amount = row[incomeLevel+2]
                    print(f"Level{level} ({incomeLevel}): {desc}")

        embed = discord.Embed(
            title=f"Wocheneinkommen für {ctx.user.display_name}",
            description=f"Deine Woche:\n{desc}",
            color=discord.Color.orange()
        )
        embed.add_field(name="Verdienst", value=f"{amount} Eddies")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)

        await ctx.respond(embed=embed)

        @staticmethod
        def convert_time(seconds):
            if seconds < 60:
                return f"{seconds} Sekunden"
            minutes = math.floor(seconds / 60)
            seconds = seconds % 60
            if minutes < 60:
                return f"{minutes} Minuten und {seconds} Sekunden"
            hours = math.floor(minutes / 60)
            minutes = minutes % 60
            return f"{hours} Stunden und {minutes} Minuten"


        @commands.Cog.listener()
        async def on_application_command_error(self, ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                seconds = ctx.command.get_cooldown_retry_after(ctx)
                final_time = self.convert_time(seconds)

                await ctx.respond(f"Du musst noch {final_time} auf das Ende des Cooldown warten", ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(Hustle(bot))
