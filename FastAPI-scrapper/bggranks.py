import httpx
import csv
import xml.etree.ElementTree as ET
import asyncio
from sqlalchemy.orm import Session
from models import SessionLocal, Product
import os

async def fetch_data_chunk(client, url, chunk):
    params = {"id": ",".join(map(str, chunk))}
    link = f"{url}?id={params['id']}"
    print("Fetching data from:", link)

    response = await client.get(url, params=params)
    data = response.text

    # Parse XML data
    root = ET.fromstring(data)

    # Extract relevant information from each item
    game_info_list = []
    for item in root.findall('.//item'):
        game_id = item.attrib.get('id', '')
        name_primary = item.find('.//name[@type="primary"]').attrib.get('value')
        thumbnail = item.findtext('.//thumbnail')
        image = item.findtext('.//image')
        min_players = item.find('.//minplayers').attrib.get('value')
        max_players = item.find('.//maxplayers').attrib.get('value')

        # Extract all categories
        categories = [category.attrib['value'] for category in item.findall('.//link[@type="boardgamecategory"]')]

        # Extract description or provide a default value
        description = item.findtext('.//description', default='No description available')

        # Append the extracted information to the list
        game_info_list.append([game_id, name_primary, thumbnail, image, min_players, max_players, categories, description])

    write_header = not os.path.exists("RelevantParsedData.csv")
    # Save the relevant information to a CSV file
    with open('RelevantParsedData.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t')
        if write_header:
            csv_writer.writerow(["bggid", "name", "thumbnail_url", "image_url", "min_players", "max_players", "categories", "description"])
        csv_writer.writerows(game_info_list)

async def process_boardgame_data():
    async with httpx.AsyncClient() as client:
        url = "https://boardgamegeek.com/xmlapi2/thing"

        with open('boardgames_ranks.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            ids = [row['id'] for row in reader]

        chunk_size = 200
        num_chunks = 6

        # Use asyncio.gather to run the fetch tasks concurrently
   
        tasks = [fetch_data_chunk(client, url, ids[i * chunk_size: (i + 1) * chunk_size]) for i in range(num_chunks)]
        await asyncio.gather(*tasks)


def process_csv_file():
    db = SessionLocal()
    with open("RelevantParsedData.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')

        next(reader, None)
       
        for row in reader:
        
            # Extract data from the CSV row
            bggid = int(row['bggid'])
            name = row['name']
            thumbnail_url = row['thumbnail_url']
            image_url = row['image_url']
            min_players = int(row['min_players'])
            max_players = int(row['max_players'])
            description = row['description']

            # Process or print the extracted data as needed
            print(f"Game ID: {bggid}, Name: {name}, Min Players: {min_players}, Max Players: {max_players}")

        

            # Create a Product instance and add it to the database
            product = Product(
                bggid=bggid,
                name=name,
                thumbnail_url=thumbnail_url,
                image_url=image_url,
                min_players=min_players,
                max_players=max_players,               
                description=description
            )

            db.add(product)

    # Commit the changes to the database
    db.commit()

    # Close the database session
    db.close()