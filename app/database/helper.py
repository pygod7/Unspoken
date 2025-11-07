import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models import User
import string
import uuid


ADJECTIVES = [
    "Happy", "Brave", "Clever", "Silly", "Calm", "Quick", "Lucky", "Fierce",
    "Blue", "Green", "Red", "Golden", "Silent", "Loud", "Jolly", "Crazy",
    "Bright", "Shiny", "Witty", "Funny", "Curious", "Bold", "Swift", "Kind",
    "Cheerful", "Mighty", "Gentle", "Fearless", "Sneaky", "Nimble", "Cunning",
    "Friendly", "Energetic", "Lazy", "Sleepy", "Grumpy", "Tiny", "Giant",
    "Wild", "Brilliant", "Radiant", "Vivid", "Sharp", "Soft", "Braveheart",
    "Frosty", "Stormy", "Windy", "Sunny", "LuckyCharm", "Magic", "Epic",
    "Luminous", "Radiant", "BoldHeart", "Fiery", "SwiftFoot", "QuickMind",
    "Mysterious", "CuriousMind", "FearlessOne", "GentleSoul", "NimbleFingers"
]


NOUNS = [
    "Tiger", "Falcon", "Rocket", "Mountain", "River", "Cat", "Wolf", "Fox",
    "Bear", "Eagle", "Lion", "Shark", "Dragon", "Hawk", "Panther", "TigerCub",
    "Panda", "Otter", "Whale", "Rabbit", "Dolphin", "TigerClaw", "Storm", "Blade",
    "Arrow", "Comet", "Flame", "Shadow", "Knight", "Wizard", "Phoenix", "Unicorn",
    "Sphinx", "Lionheart", "Wolfpack", "Thunder", "Lightning", "Cheetah", "Jaguar",
    "FalconEye", "DragonFire", "IronFist", "Silverback", "Darkness", "Ghost",
    "TigerSoul", "Moonlight", "Sunbeam", "Starlight", "Crystal", "Shadowfax",
    "Nightfall", "Frostbite", "Blizzard", "Hurricane", "Cyclone", "Avalanche",
    "Vortex", "Tempest", "Blaze", "Inferno", "Phantom", "Obsidian"
]



async def generate_username(db: AsyncSession, max_tries:int=20): #$ avoid stack overlow thing if collides again & again.
    for _ in range(max_tries):
        username = random.choice(ADJECTIVES)+random.choice(NOUNS)+str(random.randint(1,9999))
        
        result = await db.execute(
            select(User.id).where(User.username == username)
        )
        if result.scalar() is not None:
            continue
        return username
    
    raise Exception(f"Could not generate a unique username after {max_tries} tries")

       
        
def generate_password(length: int=12):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    all_char = letters + digits + symbols
    password = ''
    for _ in range(length):
        password+=random.choice(all_char)
    return password

def generate_uuid():
    return str(uuid.uuid4())

import asyncio
from app.database.conn import async_session  # your session factory

async def test_username_generator():
    async with async_session() as db:
        username = await generate_username(db)
        print("Generated username:", username)

# Run the test
asyncio.run(test_username_generator())


