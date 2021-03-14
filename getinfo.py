import requests
from bs4 import BeautifulSoup
import json


class getInfo:
    def __init__(self, currency):
        self.available_currencies = [
            "czk",
            "eur",
            "usd",
        ]
        self.acceptable_chars = list("0123456789")
        self.return_dict = {}
        self.currency = currency
        if locals()["currency"] not in self.available_currencies:
            print("currency passed to this class isn't in our list of currencies please use any of these ",
                  self.available_currencies,
                  "if you don't use any of these currencies this will cause error")
        else:
            pass

        self.currencies_dict = [
            {"name": "czk", "multiplier": 0},
            {"name": "eur", "multiplier": 0},
            {"name": "usd", "multiplier": 0}
        ]

        for dict_ in self.currencies_dict:
            out = requests.get("https://api.exchangerate-api.com/v4/latest/CZK").text
            make_dict = json.loads(out)
            dict_["multiplier"] = make_dict["rates"][dict_["name"].upper()]
        for currency_in_dict in self.currencies_dict:
            if currency_in_dict["name"] == self.currency:
                self.multiplier_for_curr = currency_in_dict["multiplier"]

    def get_info(self, url):
        if "czc.cz" in url:
            # soup
            sr = requests.get(url).text
            soup = BeautifulSoup(sr, "lxml")

            # finding
            find = soup.find(class_="warehouse")
            find_price = soup.find(class_="price alone")
            thumbnail = soup.find(class_="carousel1__item pd-preview__item")
            name = soup.find(id="microdata-container")

            # converted to string
            refined = str(find)
            refined_price = str(find_price)
            refined_thumbnail = str(thumbnail)
            name = str(name)

            # slice
            c = refined_thumbnail[refined_thumbnail.find("https://"):refined_thumbnail.find("obrazek")] + "obrazek"
            b = name[name.find('itemprop="name"') + 16:name.find('itemprop="image"') - 14]

            if refined_price == "None":
                find_price_a = soup.find(class_="price action")
                refined_price_a = str(find_price_a)
                price_a = refined_price_a[refined_price_a.find("price-vatin") + 13:-15]
                price = ""
                for char in price_a:
                    if char not in self.acceptable_chars:
                        continue
                    else:
                        price += char
            else:
                price = ""
                price_b = refined_price[refined_price.find("price-vatin") + 13:-15]
                for char in price_b:
                    if char not in self.acceptable_chars:
                        continue
                    else:
                        price += char
            if price == "":
                self.return_dict["price"] = "unknown price"
            else:
                self.return_dict["price"] = str(float(price) * self.multiplier_for_curr) + f" {self.currency}"
            if "Zjistit dostupnost u dodavatele." in refined:
                self.return_dict["name"] = b
                self.return_dict["available"] = False
                self.return_dict["thumbnail"] = c
                return self.return_dict
            if "Skladem 0 kusů" in refined:
                self.return_dict["name"] = b
                self.return_dict["available"] = False
                self.return_dict["thumbnail"] = c
                return self.return_dict
            if "Skladem" in refined:
                self.return_dict["name"] = b
                self.return_dict["available"] = True
                self.return_dict["thumbnail"] = c
                return self.return_dict
            else:
                return {
                    "error": "couldn't find any value"
                }
        if "alza.cz" in url:
            # soup
            sr = requests.get(url).text
            soup = BeautifulSoup(sr, "lxml")

            # finding
            price = soup.find(class_="bigPrice price_withVat")
            name = soup.find(itemprop="name")
            avaible = soup.find(class_="commodityAvailabilityText avl")


            # converting to string
            price = str(price)
            name = str(name)
            avaible = str(avaible)

            # slice
            price_slice = price[price.find('class="bigPrice price_withVat"')+31:-9]
            name_slice = name[price.find('itemprop="name"')+28:-11]

            # getting price to str with no space for after when we will be converting this string to int
            final_price = ""
            for char in price_slice:
                if char not in self.acceptable_chars:
                    continue
                else:
                    final_price += char

            if price == "":
                self.return_dict["price"] = "unknown price"
            else:
                self.return_dict["price"] = str(float(final_price) * self.multiplier_for_curr) + f" {self.currency}"
            self.return_dict["name"] = name_slice
            return self.return_dict



        else:
            return {
                "error": "url is not right or not from czc/alza"
            }