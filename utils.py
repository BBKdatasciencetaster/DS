import re # <- import the regular expression library for string matching.
import pandas as pd

def getProduct(df, product):
    hour_list = {}
    
    for lat, lng, hour, text, place_name in zip(df.lat, df.lng, df.date.dt.hour, df.text, df.place_name):
        
        matches = re.findall(r'"(.*?)"', text)
        
        matched_text = "".join(matches)

        if product.lower() in matched_text.lower():
            hour_list.setdefault(hour, []).append([lat, lng])
            
            continue # <- We move on to the next tweet after already finding a match

    # index containing the hours extracted from the date and timestamp
    index = [str(i) +':00' for i in range(len(hour_list.keys()))]
    
    return index, hour_list

def countProductByLocation(df, product):
    place_counts = {}
    
    for lat, lng, hour, text, place_name in zip(df.lat, df.lng, df.date.dt.hour, df.text, df.place_name):
        
        matches = re.findall(r'"(.*?)"', text)
        
        matched_text = "".join(matches)

        if product.lower() in matched_text.lower():
            place_counts.setdefault(place_name, 0)
            place_counts[place_name] += 1
            
            continue # <- We move on to the next tweet after already finding a match

    places_df = pd.DataFrame.from_dict(place_counts, orient='index')
    
    places_df.reset_index(inplace=True)
    places_df.columns=['place_name', 'count']
    return places_df
            

def countByHour(hour_list):
    temp = []
    for hour in sorted(hour_list.keys()):
        number_of_products = len(hour_list[hour])
        
        temp.append([hour, number_of_products])

    product_df = pd.DataFrame(temp, columns=['hour', 'count']).set_index('hour')
    
    return product_df
