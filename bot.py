import discord
import os
import requests
import time
from discord.ext import tasks
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

LE_TUE_RICERCHE = [
    {"name": "Ralph Lauren", "url": "https://www.vinted.it/catalog?search_text=ralph+lauren&price_to=20&order=newest_first"},
    {"name": "Levi's Jeans", "url": "https://www.vinted.it/catalog?search_text=jeans+levis&price_to=20&order=newest_first"},
    {"name": "Carhartt", "url": "https://www.vinted.it/catalog?search_text=carhartt&price_to=20&order=newest_first"},
    {"name": "Lacoste Felpe", "url": "https://www.vinted.it/catalog?search_text=felpa+lacoste&price_to=20&order=newest_first"},
    {"name": "Tommy Hilfiger Felpe", "url": "https://www.vinted.it/catalog?search_text=felpa+tommy+hilfiger&price_to=20&order=newest_first"},
    {"name": "The North Face", "url": "https://www.vinted.it/catalog?search_text=the+north+face&price_to=20&order=newest_first"},
    {"name": "Burberry Abbigliamento", "url": "https://www.vinted.it/catalog?search_text=burberry+maglia+felpa+camicia&price_to=20&order=newest_first"},
    {"name": "Stussy", "url": "https://www.vinted.it/catalog?search_text=stussy&price_to=20&order=newest_first"},
    {"name": "Supreme Abbigliamento", "url": "https://www.vinted.it/catalog?search_text=supreme+maglia+felpa+tshirt&price_to=20&order=newest_first"}
]

@tasks.loop(minutes=3)
async def check_vinted():
    print("🔄 Scansionando Vinted...")
    try:
        for ricerca in LE_TUE_RICERCHE:
            try:
                response = requests.get(ricerca["url"], headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    items = soup.find_all('div', {'class': 'feed-grid__item'})
                    if items:
                        print(f"✅ Trovati {len(items)} articoli per {ricerca['name']}")
                    else:
                        print(f"❌ Nessun articolo trovato per {ricerca['name']}")
                else:
                    print(f"❌ Errore HTTP {response.status_code} per {ricerca['name']}")
            except Exception as e:
                print(f"❌ Errore per {ricerca['name']}: {str(e)}")
            time.sleep(1)
    except Exception as e:
        print(f"❌ Errore generale: {str(e)}")

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} è online!')
    print(f'🔍 Monitoraggio di {len(LE_TUE_RICERCHE)} ricerche...')
    check_vinted.start()

@bot.slash_command(name="status", description="Controlla lo stato del bot")
async def status(ctx):
    await ctx.respond("✅ Bot online e funzionante!")

bot.run(os.getenv('DISCORD_TOKEN'))
