from flask import Flask, render_template, request, jsonify
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITY_FACTS = {
    "tokyo": [
        "Tokyo is the capital city of Japan.",
        "It is the largest metropolitan area in the world by population.",
        "Tokyo hosted the Summer Olympics in 1964 and 2021."
    ],
    "delhi": [
        "Delhi is the capital territory of India.",
        "It is home to the Red Fort, a UNESCO World Heritage site.",
        "Delhi has a rich history dating back to ancient times."
    ],
    "shanghai": [
        "Shanghai is the largest city in China by population.",
        "It is known as a global financial hub and major shipping port.",
        "The city is famous for its modern skyline including the Oriental Pearl Tower."
    ],
    "sao_paulo": [
        "São Paulo is the largest city in Brazil and the Southern Hemisphere.",
        "It is an important financial center in Latin America.",
        "The city hosts one of the largest carnivals outside of Rio de Janeiro."
    ],
    "mexico_city": [
        "Mexico City is the capital and largest city of Mexico.",
        "It was built on the ruins of the Aztec city Tenochtitlan.",
        "The city is known for its rich cultural heritage and cuisine."
    ],
    "cairo": [
        "Cairo is the capital city of Egypt and the largest city in the Arab world.",
        "It is near the ancient pyramids of Giza, one of the Seven Wonders of the Ancient World.",
        "The Nile River runs through Cairo, shaping its history and culture."
    ],
    "mumbai": [
        "Mumbai is the financial capital of India.",
        "It is home to Bollywood, India’s Hindi-language film industry.",
        "The city has the famous Gateway of India monument."
    ],
    "beijing": [
        "Beijing is the capital of China.",
        "It is home to the Forbidden City and the Great Wall nearby.",
        "The city hosted the Summer Olympics in 2008."
    ],
    "dhaka": [
        "Dhaka is the capital and largest city of Bangladesh.",
        "It is known as the 'City of Mosques' for its many Islamic places of worship.",
        "The city is a major center for trade and culture in Bangladesh."
    ],
    "osaka": [
        "Osaka is a large port city in Japan.",
        "It is famous for its modern architecture and street food culture.",
        "Osaka is home to one of Japan’s busiest airports, Kansai International Airport."
    ],
    "new_york_city": [
        "New York City is the largest city in the United States.",
        "It is known as 'The Big Apple' and a global financial hub.",
        "The city is home to landmarks like Times Square, Central Park, and the Statue of Liberty."
    ],
    "karachi": [
        "Karachi is the largest city in Pakistan.",
        "It serves as the country’s main seaport and financial center.",
        "The city has a diverse population and rich cultural heritage."
    ],
    "buenos_aires": [
        "Buenos Aires is the capital of Argentina.",
        "It is known for tango music and dance.",
        "The city features European-style architecture and vibrant nightlife."
    ],
    "chongqing": [
        "Chongqing is a major city in southwest China.",
        "It is known for its spicy cuisine, especially hot pot.",
        "Chongqing is an important industrial and transportation hub."
    ],
    "istanbul": [
        "Istanbul straddles Europe and Asia across the Bosphorus Strait.",
        "It was historically known as Byzantium and Constantinople.",
        "The city is famous for landmarks like Hagia Sophia and the Blue Mosque."
    ],
    "kolkata": [
        "Kolkata is a cultural and educational hub in eastern India.",
        "It was the capital of British India until 1911.",
        "The city is known for its colonial architecture and literary heritage."
    ],
    "manila": [
        "Manila is the capital of the Philippines.",
        "It is part of the larger Metro Manila region, one of the most populous urban areas in the world.",
        "The city has a rich history influenced by Spanish colonial rule."
    ],
    "lagos": [
        "Lagos is the largest city in Nigeria.",
        "It is a major financial center in Africa.",
        "The city is known for its vibrant music and arts scene."
    ],
    "rio_de_janeiro": [
        "Rio de Janeiro is famous for its Carnival festival.",
        "It is home to the iconic Christ the Redeemer statue.",
        "The city features beautiful beaches like Copacabana and Ipanema."
    ],
    "tianjin": [
        "Tianjin is a major port city in northern China.",
        "It has a rich colonial history with European architectural influences.",
        "The city is an important industrial and economic center."
    ],
    "guangzhou": [
        "Guangzhou is a key port city in southern China.",
        "It hosts the Canton Fair, one of the largest trade fairs in the world.",
        "The city is known for its Cantonese cuisine."
    ],
    "los_angeles": [
        "Los Angeles is the entertainment capital of the world, home to Hollywood.",
        "It has a diverse population and sprawling metropolitan area.",
        "The city is known for its beaches, like Santa Monica and Venice Beach."
    ],
    "moscow": [
        "Moscow is the capital and largest city of Russia.",
        "It is known for the Kremlin and Red Square.",
        "The city is a major political, economic, and cultural center."
    ],
    "shenzhen": [
        "Shenzhen is a major tech hub in southern China.",
        "It was one of China’s first Special Economic Zones.",
        "The city has rapidly transformed from a fishing village to a metropolis."
    ],
    "lahore": [
        "Lahore is a cultural and historical city in Pakistan.",
        "It is known for its Mughal-era architecture, including the Lahore Fort and Badshahi Mosque.",
        "The city is famous for its cuisine and vibrant arts scene."
    ],
    "chennai": [
        "Chennai is the capital of Tamil Nadu, India.",
        "It is known for its classical music and dance traditions.",
        "The city has one of the largest seaports in India."
    ],
    "lima": [
        "Lima is the capital of Peru.",
        "It is known for its rich colonial history and architecture.",
        "The city is famous for its culinary scene, especially ceviche."
    ],
    "bangkok": [
        "Bangkok is the capital of Thailand.",
        "It is famous for ornate temples like Wat Arun and Wat Phra Kaew.",
        "The city is known for its vibrant street life and markets."
    ],
    "seoul": [
        "Seoul is the capital of South Korea.",
        "It blends modern skyscrapers with historic palaces like Gyeongbokgung.",
        "The city is a global tech and pop culture hub."
    ],
    "nagoya": [
        "Nagoya is an industrial and shipping hub in Japan.",
        "It is famous for Nagoya Castle and automotive industries.",
        "The city is a key center for manufacturing and commerce."
    ],
    "hyderabad": [
        "Hyderabad is known as the 'City of Pearls' in India.",
        "It is famous for its historic Charminar monument.",
        "The city is a major center for the IT and pharmaceutical industries."
    ],
    "london": [
        "London is the capital of the United Kingdom.",
        "It has iconic landmarks like the Tower of London and Buckingham Palace.",
        "The city is a major financial and cultural center globally."
    ],
    "tehran": [
        "Tehran is the capital of Iran.",
        "It features a mix of modern and historic architecture.",
        "The city is Iran’s political and economic hub."
    ],
    "chicago": [
        "Chicago is known as the 'Windy City' in the USA.",
        "It is famous for its architecture, including the Willis Tower.",
        "The city has a rich jazz and blues music history."
    ],
    "chengdu": [
        "Chengdu is the capital of Sichuan Province, China.",
        "It is famous for its spicy cuisine and panda research centers.",
        "The city is a cultural and economic hub in southwest China."
    ],
    "nanjing": [
        "Nanjing is a historic city in eastern China.",
        "It was the capital of several Chinese dynasties.",
        "The city has many important cultural landmarks and museums."
    ],
    "wuhan": [
        "Wuhan is a major transportation hub in central China.",
        "It is known for its universities and lakes.",
        "The city played a significant role in Chinese history."
    ],
    "ho_chi_minh_city": [
        "Ho Chi Minh City is the largest city in Vietnam.",
        "It was formerly known as Saigon.",
        "The city is a center of commerce and culture."
    ],
    "luanda": [
        "Luanda is the capital of Angola.",
        "It is one of Africa’s most important ports.",
        "The city has a vibrant music and cultural scene."
    ],
    "ahmedabad": [
        "Ahmedabad is a major city in the Indian state of Gujarat.",
        "It is known for its textile industry and historic architecture.",
        "The city was founded by Sultan Ahmed Shah in the 15th century."
    ],
    "kuala_lumpur": [
        "Kuala Lumpur is the capital of Malaysia.",
        "It is famous for the Petronas Twin Towers.",
        "The city is a cultural melting pot with Malay, Chinese, and Indian influences."
    ],
    "xian": [
        "Xi'an is an ancient city in China, famous for the Terracotta Army.",
        "It was the starting point of the Silk Road.",
        "The city has many historic sites and old city walls."
    ],
    "hong_kong": [
        "Hong Kong is a major financial center and port city.",
        "It is known for its impressive skyline and harbor views.",
        "The city blends Eastern and Western cultural influences."
    ],
    "hangzhou": [
        "Hangzhou is famous for its scenic West Lake.",
        "It was the southern terminus of the Grand Canal.",
        "The city has a rich history of silk production."
    ],
    "riyadh": [
        "Riyadh is the capital of Saudi Arabia.",
        "It is the political and administrative center of the country.",
        "The city is rapidly modernizing while preserving its cultural heritage."
    ],
    "santiago": [
        "Santiago is the capital of Chile.",
        "It is nestled between the Andes and Chilean Coastal Range.",
        "The city is the cultural, political, and financial center of Chile."
    ],
    "madrid": [
        "Madrid is the capital of Spain.",
        "It is famous for its art museums like the Prado.",
        "The city has a lively nightlife and historic plazas."
    ],
    "dallas": [
        "Dallas is a major city in Texas, USA.",
        "It is known for its role in the oil and cotton industries.",
        "The city has a strong cultural scene including museums and theaters."
    ],
    "toronto": [
        "Toronto is the largest city in Canada.",
        "It is known for its multicultural population.",
        "The CN Tower is one of the city’s iconic landmarks."
    ],
    "miami": [
        "Miami is famous for its beaches and nightlife.",
        "It is a major center for finance, commerce, and culture in Florida.",
        "The city has a strong Latin American influence."
    ],
    "pune": [
        "Pune is a major city in Maharashtra, India.",
        "It is known as the 'Oxford of the East' for its educational institutions.",
        "The city has a growing IT and manufacturing industry."
    ],
    "houston": [
        "Houston is the largest city in Texas.",
        "It is home to NASA’s Johnson Space Center.",
        "The city has a diverse economy including energy, manufacturing, and aeronautics."
    ],
    "philadelphia": [
        "Philadelphia is known as the 'City of Brotherly Love'.",
        "It played a key role in American history and independence.",
        "The Liberty Bell and Independence Hall are major landmarks."
    ],
    "atlanta": [
        "Atlanta is the capital of Georgia, USA.",
        "It is a major transportation hub with one of the busiest airports.",
        "The city played an important role in the civil rights movement."
    ],
    "washington_dc": [
        "Washington, D.C. is the capital of the United States.",
        "It hosts major national monuments and museums.",
        "The White House and Capitol Building are located here."
    ],
    "barcelona": [
        "Barcelona is known for its unique architecture by Antoni Gaudí.",
        "It is a cultural and economic center in Spain.",
        "The city hosted the 1992 Summer Olympics."
    ],
    "melbourne": [
        "Melbourne is known as Australia’s cultural capital.",
        "It has a vibrant arts, music, and sports scene.",
        "The city hosts the Australian Open tennis tournament."
    ],
    "sydney": [
        "Sydney is famous for its Opera House and Harbour Bridge.",
        "It is the largest city in Australia.",
        "The city has beautiful beaches and a diverse cultural scene."
    ],
    "san_francisco": [
        "San Francisco is known for the Golden Gate Bridge.",
        "It has a historic Chinatown and vibrant tech industry.",
        "The city is famous for its steep hills and cable cars."
    ],
    "boston": [
        "Boston is one of the oldest cities in the USA.",
        "It played a key role in the American Revolution.",
        "The city is known for its prestigious universities like Harvard and MIT."
    ],
    "montreal": [
        "Montreal is the largest city in Quebec, Canada.",
        "It is known for its French heritage and festivals.",
        "The city has a vibrant arts and culinary scene."
    ],
    "berlin": [
        "Berlin is the capital of Germany.",
        "It is famous for the Berlin Wall and Brandenburg Gate.",
        "The city has a diverse cultural scene and history."
    ],
    "rome": [
        "Rome is the capital of Italy and known as the 'Eternal City'.",
        "It has ancient landmarks like the Colosseum and Vatican City.",
        "The city is a center of art, history, and religion."
    ],
    "munich": [
        "Munich is the capital of Bavaria, Germany.",
        "It is famous for Oktoberfest and beer culture.",
        "The city has many historic buildings and museums."
    ],
    "vienna": [
        "Vienna is the capital of Austria.",
        "It is known for its classical music heritage and opera.",
        "The city has stunning baroque architecture and coffeehouse culture."
    ],
    "johannesburg": [
        "Johannesburg is the largest city in South Africa.",
        "It is the economic hub of the country.",
        "The city played a significant role in the apartheid history."
    ],
    "nairobi": [
        "Nairobi is the capital of Kenya.",
        "It is famous for Nairobi National Park, located within the city.",
        "The city is a major financial and communication center in East Africa."
    ],
    "addis_ababa": [
        "Addis Ababa is the capital of Ethiopia.",
        "It hosts the headquarters of the African Union.",
        "The city is an important diplomatic hub."
    ],
    "algiers": [
        "Algiers is the capital of Algeria.",
        "It has a rich Ottoman and French colonial history.",
        "The city is known for its white buildings along the Mediterranean coast."
    ],
    "casablanca": [
        "Casablanca is the largest city in Morocco.",
        "It is an important economic and business center.",
        "The Hassan II Mosque is a famous landmark here."
    ],
    "accra": [
        "Accra is the capital of Ghana.",
        "It is known for its vibrant culture and coastal beaches.",
        "The city is a key economic and administrative center."
    ],
    "dakar": [
        "Dakar is the capital of Senegal.",
        "It is known for its music scene and Dakar Rally motorsport event.",
        "The city is a major port and cultural center."
    ],
    "abidjan": [
        "Abidjan is the economic capital of Côte d'Ivoire.",
        "It is known for its skyscrapers and vibrant culture.",
        "The city lies on the Ébrié Lagoon."
    ],
    "dar_es_salaam": [
        "Dar es Salaam is the largest city in Tanzania.",
        "It is an important port city on the Indian Ocean.",
        "The city has a rich mix of cultures and historical sites."
    ],
    "harare": [
        "Harare is the capital of Zimbabwe.",
        "It is known for its gardens and cultural landmarks.",
        "The city is the economic and political center of Zimbabwe."
    ],
    "kampala": [
        "Kampala is the capital of Uganda.",
        "It is known for its hills and vibrant markets.",
        "The city is a major commercial and cultural hub."
    ],
    "lusaka": [
        "Lusaka is the capital of Zambia.",
        "It is an important center for trade and transportation.",
        "The city has rapidly expanded in recent decades."
    ],
    "maputo": [
        "Maputo is the capital of Mozambique.",
        "It is known for its Portuguese colonial architecture.",
        "The city is a major port on the Indian Ocean."
    ],
    "windhoek": [
        "Windhoek is the capital of Namibia.",
        "It has a blend of German colonial and African architecture.",
        "The city serves as the country’s political and economic center."
    ],
    "gaborone": [
        "Gaborone is the capital of Botswana.",
        "It is one of the fastest-growing cities in Africa.",
        "The city is near the border with South Africa."
    ],
    "kigali": [
        "Kigali is the capital of Rwanda.",
        "It is known for its cleanliness and orderliness.",
        "The city is a center of economic growth in the region."
    ],
    "bujumbura": [
        "Bujumbura is the largest city and former capital of Burundi.",
        "It is located on the northeastern shore of Lake Tanganyika.",
        "The city is an important economic and transport hub."
    ],
    "juba": [
        "Juba is the capital of South Sudan.",
        "It is located on the White Nile River.",
        "The city is the administrative and commercial center of the country."
    ],
    "mogadishu": [
        "Mogadishu is the capital of Somalia.",
        "It is a historic port city on the Indian Ocean.",
        "The city has faced significant challenges but is rebuilding."
    ],
    "khartoum": [
        "Khartoum is the capital of Sudan.",
        "It lies at the confluence of the Blue and White Nile rivers.",
        "The city is a political and cultural center."
    ],
    "baghdad": [
        "Baghdad is the capital of Iraq.",
        "It has a rich history as a center of learning and culture.",
        "The city was a key hub during the Islamic Golden Age."
    ],
    "damascus": [
        "Damascus is the capital of Syria.",
        "It is one of the oldest continuously inhabited cities in the world.",
        "The city has significant religious and historic landmarks."
    ],
    "amman": [
        "Amman is the capital of Jordan.",
        "It blends ancient ruins with modern development.",
        "The city is known for its hospitable culture."
    ],
    "beirut": [
        "Beirut is the capital of Lebanon.",
        "It is known for its vibrant nightlife and cultural diversity.",
        "The city has been rebuilt several times due to conflicts."
    ],
    "jerusalem": [
        "Jerusalem is a city sacred to Judaism, Christianity, and Islam.",
        "It features important religious sites like the Western Wall and Dome of the Rock.",
        "The city has a complex political and cultural history."
    ],
    "ankara": [
        "Ankara is the capital of Turkey.",
        "It became the capital in 1923, replacing Istanbul.",
        "The city is an administrative and commercial center."
    ],
    "athens": [
        "Athens is the capital of Greece and the birthplace of democracy.",
        "It is famous for ancient landmarks like the Acropolis.",
        "The city blends classical history with a vibrant modern culture."
    ],
    "bucharest": [
        "Bucharest is the capital of Romania.",
        "It has a mix of historic and communist-era architecture.",
        "The Palace of the Parliament is one of the largest buildings in the world."
    ],
    "budapest": [
        "Budapest is the capital of Hungary, known as the 'Pearl of the Danube'.",
        "It is famous for its thermal baths and historic castles.",
        "The Chain Bridge connects the Buda and Pest sides of the city."
    ],
    "warsaw": [
        "Warsaw is the capital of Poland.",
        "It was extensively rebuilt after WWII.",
        "The city has a UNESCO World Heritage-listed Old Town."
    ],
    "prague": [
        "Prague is the capital of the Czech Republic.",
        "It is known for its medieval architecture and Prague Castle.",
        "The city played a key role in European history."
    ],
    "ljubljana": [
        "Ljubljana is the capital of Slovenia.",
        "It is known for its green spaces and pedestrian-friendly center.",
        "The Ljubljanica River runs through the city."
    ],
    "Ljubljana": [
    "Ljubljana is the capital and largest city of Slovenia.",
    "It is known for its green spaces and environmental sustainability initiatives.",
    "The city features a charming old town with a medieval castle overlooking the Ljubljanica River."
  ],
  "Bangalore": [
    "Bangalore, also known as Bengaluru, is the IT hub of India.",
    "It is famous for its pleasant climate and numerous parks, earning the nickname 'Garden City'.",
    "Bangalore hosts many multinational technology companies and startups."
  ],
  "Paris": [
    "Paris is the capital city of France, famous for its art, fashion, and culture.",
    "The Eiffel Tower and the Louvre Museum are two of its iconic landmarks.",
    "Paris is often called 'The City of Light' due to its historical role in the Age of Enlightenment."
  ],
  "Bogotá": [
    "Bogotá is the capital city of Colombia, located high in the Andes mountains.",
    "It has a vibrant cultural scene with numerous museums, theaters, and festivals.",
    "The historic La Candelaria district is known for its colonial architecture."
  ],
  "Jakarta": [
    "Jakarta is the capital and largest city of Indonesia.",
    "It is a bustling metropolis known for its diverse culture and economic significance.",
    "Jakarta faces challenges like traffic congestion and flooding due to its rapid growth."
  ],
  "Chennai": [
    "Chennai is a major cultural and economic center in southern India.",
    "It is famous for its classical music and dance traditions, including Bharatanatyam.",
    "Marina Beach in Chennai is one of the longest urban beaches in the world."
  ],
  "Lima": [
    "Lima is the capital and largest city of Peru.",
    "It was founded by Spanish conquistador Francisco Pizarro in 1535.",
    "Lima is known for its rich history and world-renowned cuisine."
  ],
  "Bangkok": [
    "Bangkok is the capital of Thailand and a major tourist destination.",
    "The city is famous for its vibrant street life and ornate temples.",
    "Bangkok is a key financial and cultural center in Southeast Asia."
  ],
  "Seoul": [
    "Seoul is the capital and largest city of South Korea.",
    "It is known for its modern skyscrapers, high-tech subways, and pop culture.",
    "Seoul has a history dating back over 2,000 years and is home to several historic palaces."
  ],
  "Nagoya": [
    "Nagoya is a major port and industrial hub in Japan’s Aichi Prefecture.",
    "It is famous for its automotive industry, housing Toyota’s headquarters.",
    "Nagoya Castle is a notable historical site and tourist attraction."
  ],
  "Hyderabad": [
    "Hyderabad is a major city in southern India, known for its IT industry and historical sites.",
    "The Charminar monument is a famous landmark in the old city.",
    "Hyderabad is also renowned for its unique cuisine, including the famous Hyderabadi biryani."
  ],
  "London": [
    "London is the capital of the United Kingdom and a global financial center.",
    "It boasts landmarks such as the Tower of London, Buckingham Palace, and the British Museum.",
    "London is known for its diverse population and rich cultural heritage."
  ],
  "Tehran": [
    "Tehran is the capital and largest city of Iran.",
    "It is a major political, cultural, and economic center in the country.",
    "The city is situated at the foot of the Alborz mountain range."
  ],
  "Chicago": [
    "Chicago is a major city in the United States, known for its architecture and cultural institutions.",
    "The city sits on the southwestern shore of Lake Michigan.",
    "Chicago is famous for its deep-dish pizza and blues music scene."
  ],
  "Chengdu": [
    "Chengdu is the capital of Sichuan Province in China, famous for its spicy cuisine.",
    "It is home to the Chengdu Research Base of Giant Panda Breeding.",
    "Chengdu is a key economic and transportation hub in western China."
  ],
  "Nanjing": [
    "Nanjing is a historic city in eastern China with a rich cultural heritage.",
    "It served as the capital of several Chinese dynasties.",
    "The city is known for landmarks like the Sun Yat-sen Mausoleum and the Nanjing Massacre Memorial."
  ],
  "Wuhan": [
    "Wuhan is a major city in central China and the capital of Hubei Province.",
    "It is an important transportation hub, located at the confluence of the Yangtze and Han rivers.",
    "Wuhan is known for its universities and vibrant student population."
  ],
  "Ho Chi Minh City": [
    "Ho Chi Minh City, formerly Saigon, is the largest city in Vietnam.",
    "It is the economic center of the country with a bustling urban landscape.",
    "The city is known for its French colonial architecture and vibrant street markets."
  ],
  "Luanda": [
    "Luanda is the capital and largest city of Angola.",
    "It is an important port city on the Atlantic coast.",
    "Luanda has rapidly grown due to oil wealth but faces urban infrastructure challenges."
  ],
  "Ahmedabad": [
    "Ahmedabad is a major city in the Indian state of Gujarat.",
    "It is known for its textile industry and historic architecture.",
    "The city is home to the Sabarmati Ashram, associated with Mahatma Gandhi."
  ],
   "Kuala Lumpur": [
    "Kuala Lumpur is the capital city of Malaysia.",
    "It is known for the iconic Petronas Twin Towers, once the tallest buildings in the world.",
    "The city is a cultural melting pot with Malay, Chinese, and Indian influences."
  ],
  "Xi'an": [
    "Xi'an is one of the oldest cities in China and was the starting point of the Silk Road.",
    "It is famous for the Terracotta Army of Emperor Qin Shi Huang.",
    "Xi'an served as the capital for several ancient Chinese dynasties."
  ],
  "Hong Kong": [
    "Hong Kong is a Special Administrative Region of China known for its skyline and deep natural harbor.",
    "It is a major global financial center and trading hub.",
    "Hong Kong blends Chinese culture with Western influences due to its colonial history."
  ],
  "Hangzhou": [
    "Hangzhou is famous for West Lake, a UNESCO World Heritage site.",
    "It was historically an important city for silk production in China.",
    "Hangzhou is also the headquarters of the e-commerce giant Alibaba."
  ],
  "Riyadh": [
    "Riyadh is the capital city of Saudi Arabia.",
    "It is a political and administrative center for the Kingdom.",
    "The city has experienced rapid modernization and urban development in recent decades."
  ],
  "Santiago": [
    "Santiago is the capital and largest city of Chile.",
    "It is nestled in a valley surrounded by the Andes and Chilean Coast Range mountains.",
    "Santiago is the financial and cultural hub of Chile."
  ],
  "Madrid": [
    "Madrid is the capital and largest city of Spain.",
    "It is famous for its Royal Palace, art museums, and lively nightlife.",
    "Madrid is located near the geographical center of the Iberian Peninsula."
  ],
  "Dallas": [
    "Dallas is a major city in the U.S. state of Texas.",
    "It is known for its role in the oil and cotton industries and as a commercial hub.",
    "Dallas has a strong cultural scene, including museums and performing arts venues."
  ],
  "Toronto": [
    "Toronto is the largest city in Canada and a major multicultural center.",
    "The CN Tower is one of the tallest free-standing structures in the world.",
    "Toronto is known for its vibrant arts, theatre, and music scenes."
  ],
  "Miami": [
    "Miami is a major city in Florida known for its beaches and nightlife.",
    "It is a significant center for finance, commerce, culture, and international trade.",
    "Miami has a large Latin American and Caribbean cultural influence."
  ],
  "Pune": [
    "Pune is a major city in the Indian state of Maharashtra.",
    "It is known for its educational institutions and growing IT industry.",
    "Pune has a rich cultural heritage with many historical landmarks."
  ],
  "Houston": [
    "Houston is the largest city in Texas and the fourth largest in the U.S.",
    "It is a global leader in the energy industry, particularly oil and gas.",
    "Houston is home to NASA's Johnson Space Center."
  ],
  "Philadelphia": [
    "Philadelphia is one of the oldest cities in the United States.",
    "It played a crucial role in the American Revolution and houses the Liberty Bell.",
    "The city has a strong cultural scene with museums, music, and cuisine."
  ],
  "Atlanta": [
    "Atlanta is the capital of Georgia, USA, and a major economic center in the Southeast.",
    "It hosted the 1996 Summer Olympics.",
    "Atlanta is known for its influential music industry, particularly hip hop and R&B."
  ],
  "Washington, D.C.": [
    "Washington, D.C. is the capital of the United States.",
    "It is home to many national monuments, museums, and the federal government.",
    "The city was founded in 1790 and named after George Washington."
  ],
  "Barcelona": [
    "Barcelona is the capital of Catalonia, Spain.",
    "It is famous for its unique architecture by Antoni Gaudí, including the Sagrada Família.",
    "Barcelona is a major cultural and economic hub on the Mediterranean coast."
  ],
  "Melbourne": [
    "Melbourne is the capital of the Australian state of Victoria.",
    "It is known for its arts, music, and coffee culture.",
    "Melbourne frequently ranks as one of the world's most livable cities."
  ],
  "Sydney": [
    "Sydney is the largest city in Australia and the capital of New South Wales.",
    "It is famous for the Sydney Opera House and Harbour Bridge.",
    "Sydney is a major global city with diverse cultural and economic activities."
  ],
  "San Francisco": [
    "San Francisco is a major city in California known for the Golden Gate Bridge.",
    "It is the birthplace of the 1960s counterculture movement.",
    "San Francisco is a technology and innovation hub near Silicon Valley."
  ],
  "Boston": [
    "Boston is the capital of Massachusetts and one of the oldest cities in the USA.",
    "It played a key role in the American Revolution.",
    "Boston is home to several prestigious universities including Harvard and MIT nearby."
  ],
  "Montreal": [
    "Montreal is the largest city in Quebec, Canada.",
    "It is known for its French heritage and vibrant arts scene.",
    "Montreal hosts the world-famous Jazz Festival every summer."
  ],
  "Berlin": [
    "Berlin is the capital and largest city of Germany.",
    "It is known for its history, including the Berlin Wall and Brandenburg Gate.",
    "Berlin has a rich cultural scene with many museums, galleries, and music venues."
  ],
  "Rome": [
    "Rome is the capital city of Italy and known as the 'Eternal City.'",
    "It is home to ancient landmarks such as the Colosseum and the Vatican.",
    "Rome has been a center of culture and politics for over two millennia."
  ],
  "Munich": [
    "Munich is the capital of Bavaria, Germany.",
    "It is famous for Oktoberfest, the world's largest beer festival.",
    "Munich is a major center for art, technology, and finance."
  ],
  "Vienna": [
    "Vienna is the capital and largest city of Austria.",
    "It is known for its classical music heritage and imperial history.",
    "The city has many grand palaces and museums."
  ],
  "Johannesburg": [
    "Johannesburg is the largest city in South Africa.",
    "It is the economic heart of the country and a major hub for finance and industry.",
    "Johannesburg played a key role in the history of apartheid and its end."
  ],
  "Nairobi": [
    "Nairobi is the capital and largest city of Kenya.",
    "It is known as the 'Green City in the Sun' due to its natural parks.",
    "Nairobi National Park, located near the city, hosts diverse wildlife including lions and rhinos."
  ],
  "Addis Ababa": [
    "Addis Ababa is the capital city of Ethiopia.",
    "It hosts the headquarters of the African Union.",
    "The city is a diplomatic hub and cultural center of Ethiopia."
  ],
  "Algiers": [
    "Algiers is the capital and largest city of Algeria.",
    "It is located on the Mediterranean coast and known for its white buildings.",
    "Algiers has a rich history influenced by Ottoman and French rule."
  ],
  "Casablanca": [
    "Casablanca is the largest city in Morocco and its economic hub.",
    "It is famous for the Hassan II Mosque, one of the largest mosques in the world.",
    "Casablanca is known for its art deco architecture and vibrant port."
  ],
  "Accra": [
    "Accra is the capital city of Ghana.",
    "It is known for its vibrant culture and historic sites like Jamestown.",
    "Accra is a key economic and administrative center in West Africa."
  ],
  "Dakar": [
    "Dakar is the capital and largest city of Senegal.",
    "It is located on the Cape Verde Peninsula on the Atlantic coast.",
    "Dakar is famous for its music, arts scene, and the Dakar Rally."
  ],
  "Abidjan": [
    "Abidjan is the economic capital of Côte d'Ivoire.",
    "It is one of the largest French-speaking cities in Africa.",
    "The city is located on the Ébrié Lagoon and has a major port."
  ],
  "Dar es Salaam": [
    "Dar es Salaam is the largest city in Tanzania and its economic hub.",
    "It is located along the Indian Ocean coast.",
    "The city has a mix of modern architecture and traditional markets."
  ],
  "Harare": [
    "Harare is the capital of Zimbabwe.",
    "It is known for its parks and gardens, including the Harare Botanical Gardens.",
    "Harare is a commercial and communications center for Zimbabwe."
  ],
  "Kampala": [
    "Kampala is the capital and largest city of Uganda.",
    "The city is located near Lake Victoria and is built on several hills.",
    "Kampala is the political and economic heart of Uganda."
  ],
  "Lusaka": [
    "Lusaka is the capital city of Zambia.",
    "It is a rapidly growing city and a commercial center.",
    "Lusaka has a tropical climate and serves as a transport hub."
  ],
  "Maputo": [
    "Maputo is the capital and largest city of Mozambique.",
    "It is known for its Portuguese colonial architecture.",
    "The city has a bustling port and vibrant cultural scene."
  ],
  "Windhoek": [
    "Windhoek is the capital of Namibia.",
    "It is situated in a valley surrounded by hills.",
    "Windhoek is known for its German colonial architecture."
  ],
  "Gaborone": [
    "Gaborone is the capital of Botswana.",
    "It is located near the South African border.",
    "Gaborone is one of the fastest-growing cities in Africa."
  ],
  "Kigali": [
    "Kigali is the capital and largest city of Rwanda.",
    "The city is known for its cleanliness and safety.",
    "Kigali is an important commercial and cultural center."
  ],
  "Bujumbura": [
    "Bujumbura is the largest city and former capital of Burundi.",
    "It is located on the northeastern shore of Lake Tanganyika.",
    "The city serves as Burundi's economic and transport center."
  ],
  "Juba": [
    "Juba is the capital and largest city of South Sudan.",
    "It is located on the White Nile river.",
    "Juba is a developing city and administrative center."
  ],
  "Mogadishu": [
    "Mogadishu is the capital of Somalia.",
    "It is located on the Indian Ocean coast.",
    "The city has a long history as a port and trading center."
  ],
  "Khartoum": [
    "Khartoum is the capital of Sudan.",
    "It lies at the confluence of the Blue Nile and White Nile rivers.",
    "Khartoum is the political, cultural, and commercial center of Sudan."
  ],
  "Baghdad": [
    "Baghdad is the capital city of Iraq.",
    "It has a rich history dating back over 1,200 years as a center of learning and culture.",
    "The city is located along the Tigris River."
  ],
  "Tehran": [
    "Tehran is the capital of Iran and its largest city.",
    "It is a major cultural and economic hub in the Middle East.",
    "The city is surrounded by the Alborz mountains."
  ],
  "Damascus": [
    "Damascus is the capital city of Syria and one of the oldest continuously inhabited cities in the world.",
    "It has a rich historical and religious heritage.",
    "Damascus is known for its ancient architecture and old city markets."
  ],
  "Amman": [
    "Amman is the capital and largest city of Jordan.",
    "The city features ancient ruins alongside modern buildings.",
    "Amman serves as the political, cultural, and economic center of Jordan."
  ],
  "Beirut": [
    "Beirut is the capital and largest city of Lebanon.",
    "It is located on the Mediterranean coast.",
    "Beirut is known for its vibrant nightlife and rich history."
  ],
  "Jerusalem": [
    "Jerusalem is a city of great religious significance for Judaism, Christianity, and Islam.",
    "It is the capital of Israel.",
    "The city contains many important religious landmarks like the Western Wall and the Church of the Holy Sepulchre."
  ],
  "Ankara": [
    "Ankara is the capital city of Turkey.",
    "It became the capital in 1923, replacing Istanbul.",
    "Ankara is an important political and cultural center."
  ],
  "Athens": [
    "Athens is the capital and largest city of Greece.",
    "It is famous for its ancient history and landmarks like the Acropolis.",
    "Athens is considered the birthplace of democracy."
  ],
  "Bucharest": [
    "Bucharest is the capital and largest city of Romania.",
    "It is known for its wide boulevards and architecture blending neoclassical and communist styles.",
    "The Palace of the Parliament in Bucharest is one of the largest buildings in the world."
  ],
  "Budapest": [
    "Budapest is the capital of Hungary and known as the 'Pearl of the Danube.'",
    "It consists of Buda and Pest, two cities separated by the Danube River.",
    "Budapest is famous for its thermal baths and historic architecture."
  ],
  "Warsaw": [
    "Warsaw is the capital and largest city of Poland.",
    "The city was extensively rebuilt after being destroyed in World War II.",
    "Warsaw has a vibrant cultural life with many theaters, museums, and parks."
  ],
  "Prague": [
    "Prague is the capital city of the Czech Republic.",
    "It is known for its well-preserved medieval architecture and the Charles Bridge.",
    "Prague is a major political, cultural, and economic center in Central Europe."
  ],
  "Sofia": [
    "Sofia is the capital and largest city of Bulgaria.",
    "The city has a history spanning over 2,000 years.",
    "Sofia is surrounded by mountains and is known for its diverse architecture."
  ],
  "Belgrade": [
    "Belgrade is the capital of Serbia.",
    "It is located at the confluence of the River Sava and Danube.",
    "Belgrade has a rich history as a strategic military and trading center."
  ],
  "Zagreb": [
    "Zagreb is the capital and largest city of Croatia.",
    "It has a mix of 18th and 19th-century architecture and vibrant cultural scenes.",
    "Zagreb is known for its museums, galleries, and medieval old town."
  ],
   "Ljubljana": [
    "Ljubljana is the capital and largest city of Slovenia.",
    "It is known for its green spaces and pedestrian-friendly old town.",
    "The Ljubljanica River runs through the city, with many charming bridges."
  ],
  "Skopje": [
    "Skopje is the capital and largest city of North Macedonia.",
    "It features a blend of historic Ottoman and modern architecture.",
    "The city is famous for its statues and monuments along the Vardar River."
  ],
  "Vilnius": [
    "Vilnius is the capital of Lithuania.",
    "It has one of the largest surviving medieval old towns in Europe.",
    "Vilnius is known for its Baroque architecture and vibrant arts scene."
  ],
  "Riga": [
    "Riga is the capital and largest city of Latvia.",
    "It has a UNESCO-listed historic center with Art Nouveau architecture.",
    "Riga is a major cultural, educational, and financial center in the Baltics."
  ],
  "Tallinn": [
    "Tallinn is the capital of Estonia.",
    "Its medieval old town is one of the best preserved in Europe.",
    "Tallinn is an important hub for technology and innovation."
  ],
  "Valletta": [
    "Valletta is the capital city of Malta.",
    "It is a fortified city founded in the 16th century by the Knights of St. John.",
    "Valletta is a UNESCO World Heritage Site known for its historic buildings."
  ],
  "Monaco": [
    "Monaco is a tiny independent city-state on the French Riviera.",
    "It is famous for its luxury casinos and the Monaco Grand Prix.",
    "Monaco is the second smallest country in the world after the Vatican."
  ],
  "Vaduz": [
    "Vaduz is the capital of Liechtenstein.",
    "It is known for the Vaduz Castle, home to the Prince of Liechtenstein.",
    "Vaduz is a small city famous for its banking and finance sector."
  ],
  "San Marino": [
    "San Marino is one of the world's smallest countries, entirely surrounded by Italy.",
    "Its capital city is also called San Marino.",
    "It is one of the oldest republics in the world, founded in 301 AD."
  ],
  "Andorra la Vella": [
    "Andorra la Vella is the capital of Andorra.",
    "It is located in the Pyrenees mountains between France and Spain.",
    "The city is known for its ski resorts and tax-free shopping."
  ],
  "Tbilisi": [
    "Tbilisi is the capital and largest city of Georgia.",
    "It is known for its diverse architecture and historic old town.",
    "Tbilisi sits on the banks of the Kura River and is a cultural hub."
  ],
  "Yerevan": [
    "Yerevan is the capital of Armenia.",
    "It is one of the world's oldest continuously inhabited cities.",
    "Yerevan is famous for its pink volcanic stone architecture."
  ],
  "Baku": [
    "Baku is the capital of Azerbaijan.",
    "It is located on the Caspian Sea and known for its modern skyline.",
    "The city has a historic old town, Icherisheher, that is UNESCO-listed."
  ],
  "Nur-Sultan": [
    "Nur-Sultan (formerly Astana) is the capital of Kazakhstan.",
    "It became the capital in 1997, replacing Almaty.",
    "The city is known for its futuristic architecture."
  ],
  "Ulaanbaatar": [
    "Ulaanbaatar is the capital and largest city of Mongolia.",
    "It is located in a valley surrounded by mountains.",
    "The city is the cultural, industrial, and financial heart of Mongolia."
  ],
  "Dhaka": [
    "Dhaka is the capital and largest city of Bangladesh.",
    "It is one of the most densely populated cities in the world.",
    "Dhaka is known as the 'City of Mosques' due to its many historic mosques."
  ],
  "Hanoi": [
    "Hanoi is the capital of Vietnam.",
    "It is famous for its centuries-old architecture and rich culture.",
    "The city sits on the banks of the Red River."
  ],
  "Jakarta": [
    "Jakarta is the capital and largest city of Indonesia.",
    "It is located on the northwest coast of Java.",
    "Jakarta is the economic, cultural, and political center of Indonesia."
  ],
  "Bangkok": [
    "Bangkok is the capital of Thailand.",
    "It is known for its ornate temples and vibrant street life.",
    "The city sits on the Chao Phraya River."
  ],
  "Kuala Lumpur": [
    "Kuala Lumpur is the capital of Malaysia.",
    "It is famous for the Petronas Twin Towers, once the tallest buildings in the world.",
    "Kuala Lumpur is a major financial and cultural center in Southeast Asia."
  ],
  "Singapore": [
    "Singapore is a city-state and island country in Southeast Asia.",
    "It is one of the world's busiest ports and financial hubs.",
    "Singapore is known for its strict laws and cleanliness."
  ],
  "Manila": [
    "Manila is the capital of the Philippines.",
    "It is known for its historic sites including Intramuros, a walled city.",
    "Manila is a densely populated bayside city on the island of Luzon."
  ],
  "Seoul": [
    "Seoul is the capital of South Korea.",
    "It is known for its technology industry and modern skyscrapers.",
    "The city has a rich history dating back over 2,000 years."
  ],
  "Tokyo": [
    "Tokyo is the capital of Japan and one of the largest metropolitan areas in the world.",
    "It is famous for its mix of traditional and ultramodern architecture.",
    "Tokyo hosted the 2020 Summer Olympics."
  ],
  "Osaka": [
    "Osaka is a large port city in Japan's Kansai region.",
    "It is known for its modern architecture, nightlife, and street food.",
    "Osaka Castle is one of Japan's most famous landmarks."
  ],
  "Nagoya": [
    "Nagoya is the fourth-largest city in Japan.",
    "It is an important industrial and shipping center.",
    "Nagoya Castle is a notable historic site."
  ],
  "Fukuoka": [
    "Fukuoka is the largest city on the island of Kyushu in Japan.",
    "It is known for its ancient temples and modern shopping malls.",
    "Fukuoka hosts the annual Hakata Gion Yamakasa festival."
  ],
  "Sapporo": [
    "Sapporo is the largest city on Japan's northern island, Hokkaido.",
    "It is famous for its annual snow festival featuring ice sculptures.",
    "Sapporo is a popular winter sports destination."
  ],
  "Kyoto": [
    "Kyoto was the former capital of Japan for over a thousand years.",
    "It is known for its classical Buddhist temples and gardens.",
    "Kyoto is famous for traditional tea ceremonies and geisha culture."
  ],
  "Changsha": [
    "Changsha is the capital of Hunan Province in China.",
    "It is known for its rich history dating back over 3,000 years.",
    "The city is famous for the Yuelu Academy, one of the oldest academies in China."
  ],
  "Ningbo": [
    "Ningbo is a major port city in Zhejiang Province, China.",
    "It has been a significant trading hub since the Tang Dynasty.",
    "Ningbo is famous for its historic Tianyi Pavilion, one of the oldest private libraries in Asia."
  ],
  "Qingdao": [
    "Qingdao is a coastal city in Shandong Province, China.",
    "It is known for its German colonial architecture and the Tsingtao Brewery.",
    "Qingdao hosts the annual Qingdao International Beer Festival."
  ],
  "Dalian": [
    "Dalian is a major port and industrial city in Liaoning Province, China.",
    "It is known for its beaches and modern architecture.",
    "Dalian has a large software and IT industry."
  ],
  "Zhengzhou": [
    "Zhengzhou is the capital of Henan Province, China.",
    "It is a major transportation hub with one of China's largest railway stations.",
    "Zhengzhou is near the ancient city of Shangqiu, rich in archaeological sites."
  ],
  "Shenyang": [
    "Shenyang is the largest city in Northeast China.",
    "It served as the capital of the Qing Dynasty before Beijing.",
    "Shenyang is known for the Imperial Palace, a UNESCO World Heritage site."
  ],
  "Jinan": [
    "Jinan is the capital of Shandong Province, China.",
    "It is famous for its numerous natural springs.",
    "The Baotu Spring Park is a popular tourist attraction in Jinan."
  ],
  "Harbin": [
    "Harbin is the capital of Heilongjiang Province, China.",
    "It hosts the world-famous Harbin International Ice and Snow Sculpture Festival.",
    "Harbin has a strong Russian influence in its architecture and culture."
  ],
  "Taiyuan": [
    "Taiyuan is the capital of Shanxi Province, China.",
    "It is an important industrial city with a history dating back over 2,500 years.",
    "Taiyuan is known for its coal mining industry."
  ],
  "Kunming": [
    "Kunming is the capital of Yunnan Province, China.",
    "It is called the 'Spring City' due to its mild climate.",
    "Kunming is a gateway to Southeast Asia and known for its diverse ethnic cultures."
  ],
  "Urumqi": [
    "Urumqi is the capital of Xinjiang Uyghur Autonomous Region, China.",
    "It is one of the most remote cities from any ocean in the world.",
    "Urumqi is a cultural melting pot of many ethnic groups."
  ],
  "Shijiazhuang": [
    "Shijiazhuang is the capital of Hebei Province, China.",
    "It developed rapidly as a transportation and industrial center.",
    "The city has seen significant urban growth in recent decades."
  ],
  "Fuzhou": [
    "Fuzhou is the capital of Fujian Province, China.",
    "It is known for its traditional architecture and mountainous landscape.",
    "Fuzhou has a rich history of maritime trade."
  ],
  "Xiamen": [
    "Xiamen is a coastal city in Fujian Province, China.",
    "It is famous for its colonial architecture and Gulangyu Island.",
    "Xiamen is an important port and trade city."
  ],
  "Hefei": [
    "Hefei is the capital of Anhui Province, China.",
    "It is known for its scientific research institutions and universities.",
    "Hefei has a history that dates back over 2,000 years."
  ],
  "Nanchang": [
    "Nanchang is the capital of Jiangxi Province, China.",
    "It played a significant role in the Chinese communist revolution.",
    "The city is known for its Tengwang Pavilion, a famous ancient building."
  ],
  "Changchun": [
    "Changchun is the capital of Jilin Province, China.",
    "It is a major center for the automotive industry.",
    "The city has a cold continental climate with snowy winters."
  ],
  "Hohhot": [
    "Hohhot is the capital of Inner Mongolia Autonomous Region, China.",
    "It is known as the 'Blue City' due to its numerous temples.",
    "Hohhot has a strong Mongolian cultural influence."
  ],
  "Nanning": [
    "Nanning is the capital of Guangxi Zhuang Autonomous Region, China.",
    "It is known as the 'Green City' for its lush tropical plants.",
    "Nanning hosts the annual China-ASEAN Expo."
  ],
  "Lanzhou": [
    "Lanzhou is the capital of Gansu Province, China.",
    "It is located on the banks of the Yellow River.",
    "Lanzhou is famous for its hand-pulled noodles."
  ],
  "Taipei": [
    "Taipei is the capital of Taiwan.",
    "It is famous for Taipei 101, one of the world's tallest skyscrapers.",
    "Taipei is a major cultural and economic center in East Asia."
  ],
  "Hong Kong": [
    "Hong Kong is a Special Administrative Region of China.",
    "It is a major global financial hub with a busy harbor.",
    "Hong Kong is known for its skyline and vibrant nightlife."
  ],
  "Macau": [
    "Macau is a Special Administrative Region of China known for its casinos.",
    "It was a Portuguese colony until 1999.",
    "Macau has a unique blend of Chinese and Portuguese cultures."
  ],
  "Sydney": [
    "Sydney is the largest city in Australia.",
    "It is famous for the Sydney Opera House and Harbour Bridge.",
    "Sydney has beautiful beaches like Bondi Beach."
  ],
  "Melbourne": [
    "Melbourne is the capital of Victoria, Australia.",
    "It is known for its arts scene, coffee culture, and sports events.",
    "Melbourne hosts the Australian Open tennis tournament."
  ],
  "Brisbane": [
    "Brisbane is the capital of Queensland, Australia.",
    "It is known for its subtropical climate and outdoor lifestyle.",
    "The city lies on the Brisbane River."
  ],
  "Perth": [
    "Perth is the capital of Western Australia.",
    "It is one of the most isolated major cities in the world.",
    "Perth is known for its beaches and vibrant arts scene."
  ],
  "Adelaide": [
    "Adelaide is the capital of South Australia.",
    "It is famous for its festivals and food and wine culture.",
    "Adelaide is surrounded by renowned wine regions."
  ],
  "Auckland": [
    "Auckland is the largest city in New Zealand.",
    "It is known as the 'City of Sails' due to its boating culture.",
    "Auckland sits between two harbors on a narrow isthmus."
  ],
  "Wellington": [
    "Wellington is the capital of New Zealand.",
    "It is known for its vibrant arts scene and harbor views.",
    "Wellington hosts the New Zealand Film Festival."
  ],
  "Christchurch": [
    "Christchurch is the largest city on New Zealand's South Island.",
    "It is known as the 'Garden City' for its parks and gardens.",
    "The city has been rebuilding after major earthquakes in 2010 and 2011."
  ],
  "Toronto": [
    "Toronto is the largest city in Canada.",
    "It is a multicultural hub with over half its residents born outside Canada.",
    "The CN Tower is a famous landmark in Toronto."
  ],
  "Montreal": [
    "Montreal is the largest city in Quebec, Canada.",
    "It is known for its French heritage and vibrant cultural scene.",
    "Montreal hosts the annual Jazz Festival, one of the largest in the world."
  ],
  "Vancouver": [
    "Vancouver is a major city in British Columbia, Canada.",
    "It is surrounded by mountains and the Pacific Ocean.",
    "Vancouver is known for its outdoor recreational opportunities."
  ],
  "Calgary": [
    "Calgary is a city in Alberta, Canada.",
    "It hosts the annual Calgary Stampede, a large rodeo festival.",
    "Calgary is known for its proximity to the Rocky Mountains."
  ],
  "Edmonton": [
    "Edmonton is the capital of Alberta, Canada.",
    "It has one of the largest urban park systems in North America.",
    "Edmonton is known for its oil and gas industry."
  ],
  "Ottawa": [
    "Ottawa is the capital city of Canada.",
    "It is home to Parliament Hill and many national museums.",
    "The city hosts Winterlude, a popular winter festival."
  ],
  "Abidjan": [
    "Abidjan is the economic capital of Côte d'Ivoire.",
    "It is known for its modern skyline and lagoon location.",
    "Abidjan is a major port city in West Africa."
  ],
  "Dar es Salaam": [
    "Dar es Salaam is the largest city in Tanzania.",
    "It was the former capital before Dodoma.",
    "The city is an important trade and transportation hub."
  ],
  "Harare": [
    "Harare is the capital of Zimbabwe.",
    "It is known for its beautiful parks and gardens.",
    "Harare is a center of commerce and government in Zimbabwe."
  ],
  "Kampala": [
    "Kampala is the capital of Uganda.",
    "It is located near Lake Victoria.",
    "Kampala is built on seven hills, giving it a unique landscape."
  ],
  "Lusaka": [
    "Lusaka is the capital of Zambia.",
    "It is known for its vibrant markets and cultural diversity.",
    "Lusaka has experienced rapid urban growth over recent decades."
  ],
  "Maputo": [
    "Maputo is the capital of Mozambique.",
    "It is famous for its colonial Portuguese architecture.",
    "Maputo is an important port city on the Indian Ocean."
  ],
  "Windhoek": [
    "Windhoek is the capital of Namibia.",
    "It combines German colonial heritage with African traditions.",
    "Windhoek is surrounded by desert landscapes."
  ],
  "Gaborone": [
    "Gaborone is the capital of Botswana.",
    "It is one of the fastest-growing cities in Africa.",
    "Gaborone is known for its modern infrastructure and wildlife nearby."
  ],
  "Kigali": [
    "Kigali is the capital of Rwanda.",
    "It is renowned for its cleanliness and safety.",
    "Kigali is a center for business and culture in Rwanda."
  ],
  "Bujumbura": [
    "Bujumbura is the former capital of Burundi.",
    "It lies on the northeastern shore of Lake Tanganyika.",
    "The city is the main port and economic center of Burundi."
  ],
  "Juba": [
    "Juba is the capital of South Sudan.",
    "It is situated on the White Nile River.",
    "Juba has grown rapidly since South Sudan's independence in 2011."
  ],
  "Mogadishu": [
    "Mogadishu is the capital of Somalia.",
    "It has a long history as an important port on the Indian Ocean.",
    "The city has faced challenges but remains culturally significant."
  ],
  "Khartoum": [
    "Khartoum is the capital of Sudan.",
    "It is located at the confluence of the Blue and White Nile rivers.",
    "Khartoum is a major political and cultural center in Sudan."
  ],
  "Baghdad": [
    "Baghdad is the capital of Iraq.",
    "It has been a center of learning and culture since medieval times.",
    "The city is located on the Tigris River."
  ],
  "Tehran": [
    "Tehran is the capital of Iran.",
    "It is the largest city in the Middle East.",
    "Tehran is a major cultural and economic center."
  ],
  "Damascus": [
    "Damascus is the capital of Syria.",
    "It is one of the oldest continuously inhabited cities in the world.",
    "Damascus has rich cultural and religious heritage."
  ],
  "Amman": [
    "Amman is the capital of Jordan.",
    "It is known for its ancient ruins and modern urban life.",
    "Amman is a cultural and political hub in the Middle East."
  ],
  "Beirut": [
    "Beirut is the capital of Lebanon.",
    "It has a history dating back more than 5,000 years.",
    "Beirut is known for its vibrant nightlife and diverse culture."
  ],
  "Jerusalem": [
    "Jerusalem is a city of major religious significance to Judaism, Christianity, and Islam.",
    "It is located in the Middle East between the Mediterranean and the Dead Sea.",
    "Jerusalem is home to important religious sites like the Western Wall and the Church of the Holy Sepulchre."
  ],
  "Ankara": [
    "Ankara is the capital of Turkey.",
    "It became the capital in 1923, replacing Istanbul.",
    "Ankara is a major administrative and commercial city."
  ],
  "Athens": [
    "Athens is the capital of Greece.",
    "It is known as the cradle of Western civilization and democracy.",
    "Athens is famous for ancient landmarks such as the Acropolis."
  ],
  "Bucharest": [
    "Bucharest is the capital of Romania.",
    "It is known for its wide avenues and historic architecture.",
    "The Palace of the Parliament is one of the largest administrative buildings in the world."
  ],
  "Budapest": [
    "Budapest is the capital of Hungary.",
    "The city is famous for its thermal baths and historic castles.",
    "Budapest is divided by the Danube River into Buda and Pest."
  ],
  "Warsaw": [
    "Warsaw is the capital of Poland.",
    "It was extensively rebuilt after World War II destruction.",
    "Warsaw is a vibrant cultural and economic center."
  ],
  "Prague": [
    "Prague is the capital of the Czech Republic.",
    "It is known for its well-preserved medieval architecture.",
    "The Charles Bridge and Prague Castle are major tourist attractions."
  ],
  "Sofia": [
    "Sofia is the capital of Bulgaria.",
    "It is one of the oldest cities in Europe with thousands of years of history.",
    "Sofia is surrounded by mountains, offering many outdoor activities."
  ],
  "Belgrade": [
    "Belgrade is the capital of Serbia.",
    "It is located at the confluence of the Sava and Danube rivers.",
    "Belgrade has a vibrant nightlife and cultural scene."
  ],
  "Zagreb": [
    "Zagreb is the capital of Croatia.",
    "It features Austro-Hungarian architecture and many museums.",
    "Zagreb is known for its medieval old town and vibrant street life."
  ],
  "Ljubljana": [
    "Ljubljana is the capital of Slovenia.",
    "The city is known for its green spaces and pedestrian-friendly center.",
    "Ljubljana Castle overlooks the city from a hilltop."
  ],
  "Kharkiv": [
    "Kharkiv is the second-largest city in Ukraine.",
    "It is an important industrial, cultural, and educational center.",
    "Kharkiv is known for its beautiful parks and Soviet-era architecture."
  ],
  "Donetsk": [
    "Donetsk is a major city in eastern Ukraine.",
    "It is known for its coal mining and heavy industry.",
    "The city has faced conflict-related challenges in recent years."
  ],
  "Nizhny Novgorod": [
    "Nizhny Novgorod is a key economic and cultural center in Russia.",
    "It sits at the confluence of the Volga and Oka rivers.",
    "The city is famous for its historic kremlin and trade fairs."
  ],
  "Ufa": [
    "Ufa is the capital of Bashkortostan, Russia.",
    "It is a major industrial and cultural hub.",
    "Ufa is known for its diverse population and oil refining industry."
  ],
  "Riyadh": [
    "Riyadh is the capital of Saudi Arabia.",
    "It is the political and administrative center of the kingdom.",
    "Riyadh has seen rapid modernization and urban development."
  ],
  "Volgograd": [
    "Volgograd is known for the pivotal Battle of Stalingrad during WWII.",
    "It is situated on the western bank of the Volga River.",
    "The city features a large memorial complex, Mamayev Kurgan."
  ],
  "Perm": [
    "Perm is an important industrial city in western Russia.",
    "It is located near the Ural Mountains.",
    "Perm is known for its cultural institutions and museums."
  ],
  "Krasnoyarsk": [
    "Krasnoyarsk lies along the Yenisei River in Siberia.",
    "It is a major center for mining and hydroelectric power.",
    "The city is famous for its natural beauty and Stolby Nature Sanctuary."
  ],
  "Voronezh": [
    "Voronezh is a key city in southwestern Russia.",
    "It has significant shipbuilding and aerospace industries.",
    "Voronezh played an important role in WWII."
  ],
  "Saratov": [
    "Saratov is located on the Volga River in Russia.",
    "It is known for its universities and cultural scene.",
    "The city has a strong industrial base."
  ],
  "Krasnodar": [
    "Krasnodar is a major city in southern Russia.",
    "It serves as a cultural and economic hub of the region.",
    "The city has a mild climate and vibrant agriculture sector."
  ],
  "Tolyatti": [
    "Tolyatti is known as the center of the Russian automotive industry.",
    "It houses the headquarters of AvtoVAZ, Russia's largest car manufacturer.",
    "The city is located along the Volga River."
  ],
  "Izhevsk": [
    "Izhevsk is the capital of Udmurtia, Russia.",
    "It is famous for manufacturing firearms and military equipment.",
    "The city has a rich cultural scene with theaters and museums."
  ],
  "Barnaul": [
    "Barnaul is a city in Siberia, Russia.",
    "It is known for its industrial economy and mineral resources.",
    "Barnaul has a scenic location along the Ob River."
  ],
  "Ulyanovsk": [
    "Ulyanovsk is the birthplace of Vladimir Lenin.",
    "It lies on the Volga River in Russia.",
    "The city has a strong aerospace and automotive industry."
  ],
  "Irkutsk": [
    "Irkutsk is near Lake Baikal, the world's deepest freshwater lake.",
    "It is a cultural and historical center of eastern Siberia.",
    "The city is known for its wooden architecture and museums."
  ],
  "Kemerovo": [
    "Kemerovo is a key city in the Kuzbass coal mining region.",
    "It is located in southwestern Siberia.",
    "The city has industries focused on coal mining and processing."
  ],
  "Novokuznetsk": [
    "Novokuznetsk is an industrial city in southwestern Siberia.",
    "It is a major steel-producing center in Russia.",
    "The city is located near the Kuznetsk Alatau mountains."
  ],
  "Ryazan": [
    "Ryazan is a historic city southeast of Moscow.",
    "It is known for its kremlin and ancient churches.",
    "Ryazan has industries including engineering and food processing."
  ],
  "Astrakhan": [
    "Astrakhan is situated near the Caspian Sea in southern Russia.",
    "It is famous for its fishing industry and caviar production.",
    "The city has a diverse cultural heritage influenced by many ethnic groups."
  ],
  "Penza": [
    "Penza is located in western Russia.",
    "It has a strong education and manufacturing sector.",
    "Penza is known for its theaters and art museums."
  ],
  "Lipetsk": [
    "Lipetsk is an industrial city in western Russia.",
    "It has significant iron and steel production.",
    "The city also hosts a number of research institutes."
  ],
  "Kirov": [
    "Kirov is located in western Russia along the Vyatka River.",
    "It is known for its timber and manufacturing industries.",
    "Kirov has many historical buildings and museums."
  ],
  "Chelyabinsk": [
    "Chelyabinsk is a major industrial city near the Ural Mountains.",
    "It is known for heavy machinery and metallurgy industries.",
    "The city experienced a meteor explosion in 2013."
  ],
  "Kaliningrad": [
    "Kaliningrad is a Russian exclave between Poland and Lithuania.",
    "It was formerly known as Königsberg before WWII.",
    "The city is a strategic port on the Baltic Sea."
  ],
  "Tula": [
    "Tula is famous for its samovars and weapons manufacturing.",
    "It is located south of Moscow, Russia.",
    "The city has a rich history in metallurgy and crafts."
  ],
  "Khabarovsk": [
    "Khabarovsk lies near the Russian-Chinese border.",
    "It is a key administrative and cultural center in the Russian Far East.",
    "The city is located on the Amur River."
  ],
  "Murmansk": [
    "Murmansk is the largest city north of the Arctic Circle.",
    "It is an important port and naval base on the Barents Sea.",
    "Murmansk experiences polar nights and midnight sun."
  ],
  "Orenburg": [
    "Orenburg is located on the Ural River in Russia.",
    "It serves as a gateway between Europe and Asia.",
    "The city has a diverse cultural heritage and industries."
  ],
  "Novosibirsk": [
    "Novosibirsk is the third-largest city in Russia.",
    "It is a major cultural and industrial center in Siberia.",
    "The city lies along the Ob River."
  ],
  "Tomsk": [
    "Tomsk is one of the oldest towns in Siberia.",
    "It is known for its universities and wooden architecture.",
    "Tomsk is a major scientific and educational center."
  ],
  "Omsk": [
    "Omsk is located in southwestern Siberia.",
    "It has a strong industrial and cultural presence.",
    "Omsk is famous for its theaters and museums."
  ],
  "Samara": [
    "Samara is situated on the Volga River in Russia.",
    "It is a key aerospace and manufacturing hub.",
    "The city hosted matches during the 2018 FIFA World Cup."
  ],
  "Kazan": [
    "Kazan is the capital of Tatarstan, Russia.",
    "It is known for its diverse culture and historic kremlin.",
    "Kazan hosted the 2013 Summer Universiade and 2015 World Aquatics Championships."
  ],
  "Tbilisi": [
    "Tbilisi is the capital and largest city of Georgia.",
    "It lies on the banks of the Kura River.",
    "The city has a rich history influenced by various empires."
  ],
  "Yekaterinburg": [
    "Yekaterinburg is a major city in the Ural region of Russia.",
    "It is the fourth-largest city in Russia.",
    "The city played a key role in the Russian Revolution."
  ],
  "Nizhny Tagil": [
    "Nizhny Tagil is an industrial city in the Ural Mountains.",
    "It is known for its steel production and heavy machinery.",
    "The city has a significant metallurgical complex."
  ],
  "Magnitogorsk": [
    "Magnitogorsk is famous for its huge steel plant.",
    "It is one of the main centers of Russian metallurgy.",
    "The city was built during the Soviet industrialization drive."
  ],
  "Vladivostok": [
    "Vladivostok is a major Pacific port city in Russia.",
    "It serves as the eastern terminus of the Trans-Siberian Railway.",
    "The city has a unique blend of Russian and Asian cultures."
  ],
  "Irbit": [
    "Irbit is known for its motorcycle manufacturing industry.",
    "It is located in Sverdlovsk Oblast, Russia.",
    "The city hosts the annual Irbit Motorcycle Festival."
  ],
  "Kursk": [
    "Kursk is famous for the largest tank battle in WWII.",
    "It is a key agricultural and industrial center in Russia.",
    "The city has a rich historical heritage."
  ],
  "Bryansk": [
    "Bryansk is a city in western Russia near the border with Belarus.",
    "It played a significant role during WWII.",
    "Bryansk has a strong timber and machinery industry."
  ],
  "Sochi": [
    "Sochi is a resort city on the Black Sea coast of Russia.",
    "It hosted the 2014 Winter Olympics.",
    "The city is known for its beaches and mild climate."
  ],
  "Saransk": [
    "Saransk is the capital of the Republic of Mordovia, Russia.",
    "It has a growing industrial and cultural presence.",
    "The city was a host for the 2018 FIFA World Cup."
  ],
  "Sterlitamak": [
    "Sterlitamak is a city in Bashkortostan, Russia.",
    "It is known for its chemical industry.",
    "The city is located near the Belaya River."
  ],
  "Kaluga": [
    "Kaluga is known as the cradle of Russian space exploration.",
    "It is the birthplace of Konstantin Tsiolkovsky.",
    "The city has a strong automotive and machinery industry."
  ],
  "Petrozavodsk": [
    "Petrozavodsk is the capital of the Republic of Karelia, Russia.",
    "It lies on the western shore of Lake Onega.",
    "The city has a rich cultural and architectural heritage."
  ],
  "Smolensk": [
    "Smolensk is a historic city in western Russia.",
    "It played a key role in Russian defense during various wars.",
    "The city has ancient fortifications and churches."
  ],
  "Komsomolsk-on-Amur": [
    "Komsomolsk-on-Amur is an industrial city in the Russian Far East.",
    "It is known for shipbuilding and aircraft manufacturing.",
    "The city is located on the Amur River."
  ],
  "Naberezhnye Chelny": [
    "Naberezhnye Chelny is known for being the home of the KamAZ truck plant.",
    "It is a major industrial city in Tatarstan, Russia.",
    "The city was developed rapidly during Soviet times."
  ],
  "Balashikha": [
    "Balashikha is a suburb of Moscow.",
    "It has developed as an industrial and residential area.",
    "The city has many parks and green spaces."
  ],
  "Novocherkassk": [
    "Novocherkassk is the cultural center of the Don Cossacks.",
    "It is located in southwestern Russia.",
    "The city features classic Cossack architecture."
  ],
  "Magnitogorsk": [
    "Magnitogorsk is famous for its steel production industry.",
    "It is one of Russia's largest industrial cities.",
    "The city was built around the massive Magnitogorsk Iron and Steel Works."
  ],
  "Nizhnekamsk": [
    "Nizhnekamsk is an industrial city in Tatarstan, Russia.",
    "It is known for its petrochemical industry.",
    "The city has modern infrastructure and cultural facilities."
  ],
  "Vladimir": [
    "Vladimir is a historic city east of Moscow.",
    "It was once a medieval capital of Russia.",
    "The city features many ancient churches and UNESCO sites."
  ],
  "Cherepovets": [
    "Cherepovets is a major industrial city in Russia.",
    "It hosts one of the largest steel plants in the country.",
    "The city is located on the Sheksna River."
  ],
  "Artem": [
    "Artem is located in Primorsky Krai, Russia.",
    "It is part of the Vladivostok metropolitan area.",
    "The city has industries related to fishing and manufacturing."
  ],
  "Arkhangelsk": [
    "Arkhangelsk is a port city on the White Sea in northern Russia.",
    "It was an important gateway for Russian trade.",
    "The city has a rich maritime history."
  ],
  "Volzhsky": [
    "Volzhsky is a city in Volgograd Oblast, Russia.",
    "It is located near the Volga River.",
    "The city is known for its chemical and energy industries."
  ],
  "Nizhny Novgorod": [
    "Nizhny Novgorod is an important economic center in Russia.",
    "It sits at the confluence of the Volga and Oka rivers.",
    "The city is famous for its Kremlin and historical architecture."
  ],
  "Sterlitamak": [
    "Sterlitamak is an industrial city in Bashkortostan.",
    "It has significant chemical manufacturing.",
    "The city is located near the Belaya River."
  ],
  "Pskov": [
    "Pskov is one of the oldest cities in Russia.",
    "It has a well-preserved medieval Kremlin.",
    "The city was an important trade and cultural center in medieval times."
  ],
  "Kaliningrad": [
    "Kaliningrad is a Russian exclave on the Baltic Sea.",
    "Formerly known as Königsberg, it has a unique history.",
    "The city is a key naval base for Russia."
  ],
  "Dzerzhinsk": [
    "Dzerzhinsk is a major chemical industry center in Russia.",
    "It is located near Nizhny Novgorod.",
    "The city was founded in the early 20th century."
  ],
  "Kurgan": [
    "Kurgan is located in southwestern Siberia.",
    "It has a strong agricultural and industrial base.",
    "The city serves as an administrative center for the region."
  ],
  "Novoaltaysk": [
    "Novoaltaysk is a city in Altai Krai, Russia.",
    "It is an industrial and transportation hub.",
    "The city is located near the Ob River."
  ],
  "Almetyevsk": [
    "Almetyevsk is a city in Tatarstan, Russia.",
    "It is a center for the oil industry.",
    "The city has modern infrastructure and cultural institutions."
  ],
  "Nakhodka": [
    "Nakhodka is a port city in Primorsky Krai, Russia.",
    "It is an important trade and shipping center on the Pacific coast.",
    "The city has a large fishing industry."
  ],
  "Kirov": [
    "Kirov is located on the Vyatka River in western Russia.",
    "It is known for its timber and manufacturing industries.",
    "The city has many historic sites and museums."
  ],
  "Taganrog": [
    "Taganrog is a port city on the Sea of Azov.",
    "It is the birthplace of the playwright Anton Chekhov.",
    "The city has a rich maritime and cultural history."
  ],
  "Nizhnekamsk": [
    "Nizhnekamsk is known for its large petrochemical complex.",
    "It is located in Tatarstan, Russia.",
    "The city has a well-developed infrastructure."
  ],
  "Bratsk": [
    "Bratsk is located in Irkutsk Oblast, Russia.",
    "It is known for the Bratsk Hydroelectric Power Station.",
    "The city is a center of timber and aluminum industries."
  ],
  "Yoshkar-Ola": [
    "Yoshkar-Ola is the capital of the Mari El Republic, Russia.",
    "The city is known for its unique architecture and cultural festivals.",
    "It lies along the Malaya Kokshaga River."
  ],
  "Novomoskovsk": [
    "Novomoskovsk is located in Tula Oblast, Russia.",
    "It has chemical and manufacturing industries.",
    "The city has parks and historical monuments."
  ],
  "Murom": [
    "Murom is one of the oldest cities in Russia.",
    "It is located on the Oka River.",
    "The city is famous for its medieval churches and legends."
  ],
  "Komsomolsk-on-Amur": [
    "Komsomolsk-on-Amur is an industrial city on the Amur River.",
    "It is known for aircraft and shipbuilding industries.",
    "The city was founded in the 1930s during Soviet industrialization."
  ],
    "Blagoveshchensk": [
    "Blagoveshchensk is a city on the border of Russia and China.",
    "It lies along the Amur River.",
    "The city is an important trade hub between the two countries."
  ],
  "Novokuznetsk": [
    "Novokuznetsk is a major industrial city in southwestern Siberia.",
    "It is known for coal mining and steel production.",
    "The city has a rich history dating back to the 17th century."
  ],
  "Arzamas": [
    "Arzamas is a historic city in Nizhny Novgorod Oblast, Russia.",
    "It is known for its architectural monuments.",
    "The city played a role in Russia’s literary and cultural history."
  ],
  "Veliky Novgorod": [
    "Veliky Novgorod is one of Russia's oldest cities.",
    "It was a major trade center in medieval times.",
    "The city has a well-preserved Kremlin and ancient churches."
  ],
  "Kamensk-Uralsky": [
    "Kamensk-Uralsky is an industrial city in the Ural Mountains.",
    "It specializes in metallurgy and machinery manufacturing.",
    "The city was founded in the 17th century."
  ],
  "Nefteyugansk": [
    "Nefteyugansk is a city in the Khanty-Mansi Autonomous Okrug.",
    "It is known for oil extraction and refining.",
    "The city was established during Soviet oil development."
  ],
  "Volgograd": [
    "Volgograd was formerly known as Stalingrad.",
    "It was the site of the pivotal WWII Battle of Stalingrad.",
    "The city lies on the Volga River."
  ],
  "Novorossiysk": [
    "Novorossiysk is a major port city on the Black Sea.",
    "It is one of Russia's largest seaports.",
    "The city played a key role in Russian naval history."
  ],
  "Vologda": [
    "Vologda is known for its historic wooden architecture.",
    "It is a cultural center in northwestern Russia.",
    "The city is famous for Vologda lace craftsmanship."
  ],
  "Kostroma": [
    "Kostroma is part of Russia's Golden Ring of historic cities.",
    "It is located at the confluence of the Volga and Kostroma Rivers.",
    "The city is known for its architectural heritage and monasteries."
  ],
  "Novocheboksarsk": [
    "Novocheboksarsk is a city in the Chuvash Republic.",
    "It has a significant manufacturing industry.",
    "The city was founded in the 1960s during Soviet industrial expansion."
  ],
  "Penza": [
    "Penza is a city in western Russia with rich cultural traditions.",
    "It is known for its theaters and museums.",
    "The city has a strong educational sector."
  ],
  "Yaroslavl": [
    "Yaroslavl is a UNESCO World Heritage city in Russia.",
    "It lies at the confluence of the Volga and Kotorosl Rivers.",
    "The city has well-preserved medieval architecture."
  ],
  "Kemerovo": [
    "Kemerovo is an industrial city in southwestern Siberia.",
    "It is a center for coal mining.",
    "The city is part of the Kuzbass coal basin."
  ],
  "Shakhty": [
    "Shakhty is known for its coal mining industry.",
    "It is located in Rostov Oblast, Russia.",
    "The city developed rapidly in the early 20th century."
  ],
  "Nizhnevartovsk": [
    "Nizhnevartovsk is a key city in Russia’s oil industry.",
    "It is located in the Khanty-Mansi Autonomous Okrug.",
    "The city developed around oil field exploration."
  ],
  "Taganrog": [
    "Taganrog is a port city on the Sea of Azov.",
    "It is the birthplace of playwright Anton Chekhov.",
    "The city has rich maritime traditions."
  ],
  "Sterlitamak": [
    "Sterlitamak is an industrial city in Bashkortostan.",
    "It has chemical production facilities.",
    "The city lies along the Belaya River."
  ],
  "Grozny": [
    "Grozny is the capital of the Chechen Republic.",
    "It has undergone significant reconstruction after conflicts.",
    "The city is an important cultural and economic center in the North Caucasus."
  ],
  "Makhachkala": [
    "Makhachkala is the capital of Dagestan.",
    "It lies on the Caspian Sea coast.",
    "The city is a diverse cultural melting pot."
  ],
  "Saransk": [
    "Saransk is the capital of the Republic of Mordovia.",
    "It was a host city for the 2018 FIFA World Cup.",
    "The city has a growing industrial base."
  ],
  "Kazan": [
    "Kazan is the capital of Tatarstan and a major cultural center.",
    "It has a rich mix of Russian and Tatar cultures.",
    "The city is famous for the Kazan Kremlin."
  ],
  "Ufa": [
    "Ufa is the capital of Bashkortostan.",
    "It is an industrial and cultural hub in the Urals region.",
    "The city hosts various ethnic groups and festivals."
  ],
  "Chelyabinsk": [
    "Chelyabinsk is a major industrial city in the Urals.",
    "It was impacted by a meteor explosion in 2013.",
    "The city is known for heavy machinery production."
  ],
  "Omsk": [
    "Omsk is one of Siberia's largest cities.",
    "It lies along the Irtysh River.",
    "The city has a strong cultural and educational presence."
  ],
  "Tomsk": [
    "Tomsk is one of the oldest towns in Siberia.",
    "It is a major educational center with several universities.",
    "The city is known for its wooden architecture."
  ],
  "Barnaul": [
    "Barnaul is the administrative center of Altai Krai.",
    "It lies on the Ob River.",
    "The city is a key industrial and cultural center."
  ],
  "Irkutsk": [
    "Irkutsk is near the famous Lake Baikal.",
    "It has a rich history linked to Siberian exploration.",
    "The city is a gateway for tourists to Lake Baikal."
  ],
  "Krasnoyarsk": [
    "Krasnoyarsk is a major city in Siberia.",
    "It is located along the Yenisei River.",
    "The city is known for its natural beauty and industry."
  ],
  "Vladikavkaz": [
    "Vladikavkaz is the capital of North Ossetia-Alania.",
    "It lies in the Caucasus Mountains.",
    "The city has a diverse cultural heritage."
  ],
  "Murmansk": [
    "Murmansk is the largest city north of the Arctic Circle.",
    "It is an important port on the Barents Sea.",
    "The city plays a key role in Arctic shipping and fishing."
  ],
  "Krasnodar": [
    "Krasnodar is a city in southern Russia near the Black Sea.",
    "It is an agricultural and cultural center.",
    "The city has a warm climate and vibrant economy."
  ],
  "Sochi": [
    "Sochi hosted the 2014 Winter Olympics.",
    "It is a popular Black Sea resort city.",
    "The city is known for its subtropical climate."
  ],
  "Sevastopol": [
    "Sevastopol is a port city on the Crimean Peninsula.",
    "It has a long naval history.",
    "The city is strategically important for Russia's Black Sea Fleet."
  ],
  "Simferopol": [
    "Simferopol is the administrative center of Crimea.",
    "It is a key transportation hub on the peninsula.",
    "The city has rich cultural and historical sites."
  ],
  "Khabarovsk": [
    "Khabarovsk is a major city in Russia's Far East.",
    "It lies on the Amur River near the Chinese border.",
    "The city is an important administrative and cultural center."
  ],
  "Yuzhno-Sakhalinsk": [
    "Yuzhno-Sakhalinsk is the largest city on Sakhalin Island.",
    "It is known for its oil and gas industry.",
    "The city has a unique mix of Russian and Asian influences."
  ],
  "Petropavlovsk-Kamchatsky": [
    "Petropavlovsk-Kamchatsky is a port city in the Russian Far East.",
    "It lies near active volcanoes on the Kamchatka Peninsula.",
    "The city is a center for fishing and tourism."
  ],
  "Komsomolsk-on-Amur": [
    "Komsomolsk-on-Amur is known for shipbuilding and aircraft manufacturing.",
    "It is located on the Amur River.",
    "The city was founded during Soviet industrialization."
  ],
  "Nizhny Tagil": [
    "Nizhny Tagil is an industrial city in the Ural Mountains.",
    "It is famous for metallurgy and heavy machinery.",
    "The city played a key role in Russian industrial history."
  ],
  "Orenburg": [
    "Orenburg is located near the Ural River.",
    "It serves as a gateway between Europe and Asia.",
    "The city is known for its cultural diversity."
  ],
  "Ryazan": [
    "Ryazan is one of Russia's oldest cities.",
    "It lies on the Oka River.",
    "The city has notable historical monuments and kremlin."
  ],
  "Ivanovo": [
    "Ivanovo is known as the 'City of Brides' due to its historical textile industry employing many women.",
    "It was a major center for the Russian textile industry.",
    "The city features unique constructivist architecture."
  ],
  "Magnitogorsk": [
    "Magnitogorsk is a large industrial city famous for steel production.",
    "It is located in the southern Ural Mountains.",
    "The city developed rapidly during the Soviet industrialization era."
  ],
  "Tula": [
    "Tula is renowned for its weapons manufacturing industry.",
    "It is famous for producing samovars and gingerbread.",
    "The city has a rich history dating back to the 12th century."
  ],
  "Kirov": [
    "Kirov is a historic city in western Russia, formerly known as Vyatka.",
    "It is known for its traditional Russian architecture.",
    "The city is an important cultural and administrative center."
  ],
  "Chita": [
    "Chita is located in Siberia near the border with Mongolia.",
    "It is a key transportation hub on the Trans-Siberian Railway.",
    "The city has a diverse cultural heritage influenced by Siberian and Mongolian peoples."
  ],
  "Bryansk": [
    "Bryansk is an industrial city in western Russia.",
    "It played a significant role in World War II partisan resistance.",
    "The city is surrounded by dense forests and natural reserves."
  ],
  "Belgorod": [
    "Belgorod is near the border with Ukraine and known for its agriculture.",
    "It has a history dating back to the 16th century.",
    "The city is a center for education and scientific research."
  ],
  "Vladimir": [
    "Vladimir is an ancient city, part of Russia's Golden Ring.",
    "It has famous medieval cathedrals listed as UNESCO World Heritage sites.",
    "The city was once a medieval capital of Russia."
  ],
  "Kurgan": [
    "Kurgan is an industrial city in the Urals region.",
    "It is known for machinery and metalworking industries.",
    "The city lies on the Tobol River."
  ],
  "Smolensk": [
    "Smolensk is one of the oldest cities in Russia with significant medieval fortifications.",
    "It played an important role in several historical conflicts.",
    "The city has a rich architectural and cultural heritage."
  ],
  "Vladivostok": [
    "Vladivostok is a major Pacific port and the terminus of the Trans-Siberian Railway.",
    "It is Russia's largest city on the Pacific coast.",
    "The city has strategic military importance and scenic landscapes."
  ],
  "Kostanay": [
    "Kostanay is a city in northern Kazakhstan near the Russian border.",
    "It is an important agricultural and industrial center.",
    "The city was founded during Russian expansion in the 19th century."
  ],
  "Omsk": [
    "Omsk is a key city in southwestern Siberia.",
    "It is located on the Irtysh River.",
    "The city is a cultural and economic hub with many theaters and museums."
  ],
  "Novy Urengoy": [
    "Novy Urengoy is known as the 'gas capital' of Russia.",
    "It is located in the Yamalo-Nenets Autonomous Okrug.",
    "The city developed due to large natural gas fields nearby."
  ],
  "Yakutsk": [
    "Yakutsk is the coldest city in the world with temperatures below -40°C in winter.",
    "It is the capital of the Sakha Republic (Yakutia).",
    "The city is known for its diamond mining industry."
  ],
  "Nalchik": [
    "Nalchik is the capital of the Kabardino-Balkar Republic.",
    "It is known for its mountainous scenery and mineral springs.",
    "The city is a popular resort destination in the North Caucasus."
  ],
  "Saransk": [
    "Saransk is the capital of Mordovia and hosted 2018 FIFA World Cup matches.",
    "It has a growing economy focused on machinery and food industries.",
    "The city has several cultural and sporting facilities."
  ],
  "Surgut": [
    "Surgut is one of the wealthiest cities in Russia due to oil and gas industries.",
    "It is located on the Ob River in western Siberia.",
    "The city has modern infrastructure and educational institutions."
  ],
  "Sterlitamak": [
    "Sterlitamak is an industrial city in Bashkortostan with chemical production.",
    "It is situated on the Belaya River.",
    "The city was founded in the 18th century and expanded in Soviet times."
  ],
  "Nizhnekamsk": [
    "Nizhnekamsk is a center for petrochemical industry in Tatarstan.",
    "The city was established in the 1960s near the Kama River.",
    "It hosts one of Russia's largest oil refineries."
  ],
  "Novosibirsk": [
    "Novosibirsk is the largest city in Siberia and a major scientific center.",
    "It lies on the Ob River and is a key transportation hub.",
    "The city hosts the Novosibirsk State University and many research institutes."
  ],
  "Kazan": [
    "Kazan is the capital of Tatarstan and known for its multicultural population.",
    "It features the Kazan Kremlin, a UNESCO World Heritage site.",
    "The city hosted the 2013 Summer Universiade and 2018 FIFA World Cup."
  ],
  "Chelyabinsk": [
    "Chelyabinsk is known for its heavy industry and metallurgy.",
    "It was the site of a meteor explosion in 2013.",
    "The city is an important transport and industrial hub."
  ],
  "Yekaterinburg": [
    "Yekaterinburg is the fourth-largest city in Russia.",
    "It is located on the border of Europe and Asia.",
    "The city is known for its role in Russian history and industrial development."
  ],
  "Ufa": [
    "Ufa is the capital of Bashkortostan and a cultural center.",
    "It has a diverse population including Russians, Bashkirs, and Tatars.",
    "The city is a major center for the oil refining industry."
  ],
  "Perm": [
    "Perm is located near the Ural Mountains and the Kama River.",
    "It has a strong cultural scene with theaters and museums.",
    "The city is an important industrial and scientific hub."
  ],
  "Volgograd": [
    "Volgograd was formerly known as Stalingrad.",
    "It was the site of one of the most important battles of WWII.",
    "The city lies along the Volga River."
  ],
  "Rostov-on-Don": [
    "Rostov-on-Don is a major port city near the Sea of Azov.",
    "It serves as a gateway to the Caucasus region.",
    "The city is an important cultural and economic center."
  ],
  "Krasnoyarsk": [
    "Krasnoyarsk is located on the Yenisei River in Siberia.",
    "It is known for its natural beauty and industrial economy.",
    "The city has several universities and scientific research centers."
  ],
  "Voronezh": [
    "Voronezh is a large industrial city in western Russia.",
    "It played an important role in Russian naval history.",
    "The city has a diverse economy including aerospace and machinery."
  ],
  "Irkutsk": [
    "Irkutsk is near Lake Baikal, the world's deepest freshwater lake.",
    "It has a rich history as a center of Siberian exploration.",
    "The city is a gateway for tourists visiting Lake Baikal."
  ],
  "Khabarovsk": [
    "Khabarovsk is a major city in Russia's Far East on the Amur River.",
    "It has a diverse cultural mix including Russian and Asian influences.",
    "The city serves as an administrative center of Khabarovsk Krai."
  ],
  "Yaroslavl": [
    "Yaroslavl is one of the oldest cities in Russia.",
    "It is part of the Golden Ring of historic cities.",
    "The city features well-preserved medieval architecture."
  ],
  "Tomsk": [
    "Tomsk is a historic Siberian city with a strong academic tradition.",
    "It is known for its wooden architecture.",
    "The city hosts several universities and research institutions."
  ],
  "Barnaul": [
    "Barnaul is the administrative center of Altai Krai.",
    "It lies on the Ob River.",
    "The city has a mixed economy of industry and agriculture."
  ],
  "Orenburg": [
    "Orenburg is located near the Ural River and borders Kazakhstan.",
    "It has a diverse cultural heritage blending Russian and Central Asian influences.",
    "The city was historically a frontier fortress."
  ],
  "Komsomolsk-on-Amur": [
    "Komsomolsk-on-Amur is a major industrial city on the Amur River.",
    "It is known for aircraft and shipbuilding industries.",
    "The city was founded in the 1930s as a Soviet industrial center."
  ],
  "Petropavlovsk-Kamchatsky": [
    "Petropavlovsk-Kamchatsky is located on the Kamchatka Peninsula.",
    "It is surrounded by volcanoes and rich wildlife.",
    "The city is a key base for fishing and scientific research."
  ],
  "Nizhny Novgorod": [
    "Nizhny Novgorod is a major economic and cultural center on the Volga River.",
    "It has a historic Kremlin and vibrant arts scene.",
    "The city played a key role in Russian trade history."
  ],
  "Kaliningrad": [
    "Kaliningrad is a Russian exclave between Poland and Lithuania.",
    "It was formerly the German city of Königsberg.",
    "The city is a strategic Baltic Sea port."
  ],
  "Tver": [
    "Tver is located northwest of Moscow along the Volga River.",
    "It was an important medieval trading city.",
    "The city has many historical monuments and museums."
  ],
  "Ivanovo": [
    "Ivanovo is famous for its textile industry and constructivist architecture.",
    "It is sometimes called the 'City of Brides' due to many women working in textiles.",
    "The city has several theaters and cultural institutions."
  ],
  "Magnitogorsk": [
    "Magnitogorsk is a center for steel production in Russia.",
    "It is located in the southern Ural Mountains.",
    "The city developed rapidly as part of Soviet industrialization."
  ],
   "Lucknow": [
    "Lucknow is renowned for its Nawabi-era culture and cuisine.",
    "It is famous for traditional embroidery called Chikankari.",
    "The city has many historical monuments including Bara Imambara."
  ],
   "Kanpur": [
    "Kanpur is an industrial city known historically for its leather and textile industries.",
    "It played a significant role during the Indian Rebellion of 1857.",
    "The city is situated on the banks of the Ganges River."
  ],
  "Nagpur": [
    "Nagpur is known as the 'Orange City' for its citrus farms.",
    "It is the geographical center of India, marked by the Zero Mile Stone.",
    "The city is an important commercial and political hub in central India."
  ],
  "Indore": [
    "Indore is the largest city in Madhya Pradesh and a major commercial center.",
    "It is famous for its street food and vibrant markets.",
    "The city consistently ranks high in cleanliness surveys across India."
  ],
  "Thane": [
    "Thane is part of the Mumbai Metropolitan Region and known for its lakes.",
    "It is called the 'City of Lakes' with over 30 lakes in its vicinity.",
    "The city has grown rapidly as a residential and commercial area."
  ],
  "Faridabad": [
    "Faridabad is a major industrial city in Haryana.",
    "It forms part of the National Capital Region (NCR) around Delhi.",
    "The city has seen rapid urbanization and infrastructure development."
  ],
  "Ghaziabad": [
    "Ghaziabad is an industrial city near Delhi in Uttar Pradesh.",
    "It is a key hub in the NCR and has strong connectivity to Delhi.",
    "The city is known for manufacturing and engineering industries."
  ],
  "Meerut": [
    "Meerut is one of the oldest cities in Uttar Pradesh with historical importance.",
    "It played a crucial role in the 1857 Indian Rebellion.",
    "The city is famous for its sports goods manufacturing industry."
  ],
  "Jabalpur": [
    "Jabalpur is known for its marble rocks and natural beauty.",
    "It is an important military and administrative center in Madhya Pradesh.",
    "The city lies on the banks of the Narmada River."
  ],
  "Aurangabad": [
    "Aurangabad is famous for its nearby Ajanta and Ellora Caves, UNESCO World Heritage sites.",
    "The city was named after the Mughal emperor Aurangzeb.",
    "It is a center for the automotive and manufacturing industries."
  ],
  "Ranchi": [
    "Ranchi is the capital of Jharkhand and known as the 'City of Waterfalls'.",
    "The city is surrounded by hills and has a pleasant climate.",
    "Ranchi is rich in mineral resources and tribal culture."
  ],
  "Dhanbad": [
    "Dhanbad is known as the 'Coal Capital of India'.",
    "It is a major center for coal mining and industries.",
    "The city has several educational institutions including engineering colleges."
  ],
  "Mysore": [
    "Mysore is famous for its royal heritage and the annual Dasara festival.",
    "It is known as the 'City of Palaces'.",
    "The city is a major tourist destination in Karnataka."
  ],
  "Tiruchirappalli": [
    "Also called Trichy, it is known for the ancient Rockfort Temple.",
    "The city is an important educational and industrial center.",
    "Trichy is famous for its cultural heritage and festivals."
  ],
  "Coimbatore": [
    "Coimbatore is known as the 'Manchester of South India' for its textile industry.",
    "It is a major hub for engineering and manufacturing.",
    "The city is close to scenic hill stations like Ooty."
  ],
  "gurgaon": [
    "Gurgaon is a major financial and industrial hub in the National Capital Region (NCR).",
    "It is known for its modern skyline with many high-rise buildings and corporate offices.",
    "Gurgaon has rapidly developed into a center for IT, manufacturing, and automobile industries."
]
    # Add more cities and facts here
}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        data = request.get_json()
        city = data.get('city', '').strip()

        if not city:
            return jsonify({'error': 'City name cannot be empty'}), 400

        if not API_KEY:
            return jsonify({'error': 'API key not configured on server'}), 500

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        weather_data = response.json()

        result = {
            'city': weather_data.get('name', 'N/A'),
            'country': weather_data.get('sys', {}).get('country', ''),
            'temp': round(weather_data['main']['temp']),
            'feels_like': round(weather_data['main']['feels_like']),
            'description': weather_data['weather'][0]['description'].capitalize(),
            'icon': weather_data['weather'][0]['icon'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'pressure': weather_data['main']['pressure'],
            'fact': random.choice(CITY_FACTS.get(city.lower(), ["No interesting fact available for this city."]))
        }

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Weather service error: {str(e)}"}), 502
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # use the port Render sets
    app.run(host="0.0.0.0", port=port, debug=True)
