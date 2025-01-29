# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class JsonWriterPipeline:
    def process_item(self, item, spider):
        
        # strip all whitespaces from strings
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()
        
        #wirite to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.strip()
        
        #write price to float
        price_keys = ['price_excl_tax', 'price_incl_tax', 'price', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£','')
            adapter[price_key] = float(value)
        
        #availability to boolean
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array)<2:
            adapter['availability'] = 0
        else:
            availabity_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availabity_array[0])
        
        #reviest string to number
        num_reviews = adapter.get('num_reviews')    
        adapter['num_reviews'] = int(num_reviews)
        
        #stars text to number
        stars = adapter.get('stars')
        split_stars_array = stars.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5
        
        
        return item