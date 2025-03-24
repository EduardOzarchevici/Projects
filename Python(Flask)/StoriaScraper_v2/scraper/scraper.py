from bs4 import BeautifulSoup
import requests
import sqlite3
import re
from website import db, create_app
from website.models import Announcement

app = create_app()  # Creează aplicația Flask
with app.app_context():
    for x in range(2):

        url = f"https://www.storia.ro/ro/rezultate/inchiriere/apartament/iasi/iasi?by=DEFAULT&direction=DESC&viewType=listing&page={x}"
        print("PROCESSING PAGE: ", x)
        header = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
        page = requests.get(url, headers=header)
        #print(page.status_code)
        page_parsed = BeautifulSoup(page.text, "html.parser")
        #print(page_parsed.prettify())
        listing_links = page_parsed.find_all("a", attrs={"class":"css-16vl3c1 e17g0c820"})
        listing_titles = page_parsed.find_all("p", attrs={"class":"css-u3orbr e1g5xnx10"})
        listing_locations = page_parsed.find_all("p", attrs={"class":"css-42r2ms eejmx80"})
        listing_nb_rooms = page_parsed.find_all("dl", attrs={"class":"css-9q2yy4 e1nke57n1"})
        listing_owner = page_parsed.find_all("div", attrs={"class":"css-zmiifc es3mydq2"})
        listing_prices = page_parsed.find_all("span", attrs={"class":"css-2bt9f1 evk7nst0"})

        print("Data insertion begins!")

        print("Links:", len(listing_links))
        print("Titles:", len(listing_titles))
        print("Locations:", len(listing_locations))
        print("Rooms:", len(listing_nb_rooms))
        print("Owners:", len(listing_owner))
        print("Prices:", len(listing_prices))

        for link, title, location, nb_room, owner, price in zip(listing_links, listing_titles, listing_locations, listing_nb_rooms, listing_owner, listing_prices):
            print("Inserting Values for link: ", link.text)

            numbers = re.findall(r'\d+', nb_room.text)

            num_rooms = numbers[0] if len(numbers) > 0 else None  #Nb_rooms
            surface = numbers[1] if len(numbers) > 1 else None  #surface
            floor = numbers[2] if len(numbers) > 2 else None    #floor

            verify = Announcement.query.filter_by(description=title.text).first()
            if not verify:
                new_announcement = Announcement(description=title.text, location=location.text, nb_rooms=num_rooms, surface=surface, floor=floor, owner=owner.text, price=price.text, link=link['href'])
                db.session.add(new_announcement)
                db.session.commit()
