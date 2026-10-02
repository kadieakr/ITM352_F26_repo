celebs = ("Taylor Swift", "Justin Bieber", "Beyonce", "Kim Kardashian", "Tyla")
ages = (36, 32, 44, 37, 23)

celeb_list = []
for celeb in celebs:
    celeb_list.append(celeb)

ages_list= [age for age in ages]

celebs_dict = {"celebs": celeb_list, "ages": ages_list}
print(celebs_dict)

