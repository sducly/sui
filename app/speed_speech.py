from outputs.speech import speak


async def main():
	result = await speak('Bonjour Sui va bien et toi. Si tu as besoin d aides, n hesites pas à demander à Sui. Sinon casses-toi')


# Run the async function
import asyncio
asyncio.run(main())