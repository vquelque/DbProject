def queries():
    queries_list= [
        {
        "id": 1,
        "name": "Assigment1-Q1",
        "text":"Find the average price for a listing with 8 bedrooms.",
        "query":"SELECT AVG(price.price)"
                "FROM Prices price"
                "WHERE price.listing_id IN ("
                "    SELECT property.listing_id"
                "    FROM Property property"
                "    WHERE property.bedrooms = 8"
                ");"

        },
        {
        "id": 2,
        "name": "Assigment1-Q2",
        "text":"Find the average cleaning review score for listings with TV.",
        "query":"SELECT AVG(s.review_scores_cleanliness)"
                "FROM Scores s, Property p"
                "WHERE (p.listing_id = s.listing_id) AND p.PROPERTY_ID IN ("
                "    SELECT h.PROPERTY_ID"
                "    FROM HAS_AMENITIES h, AMENITY a"
                "    WHERE (h.AMENITY_ID = a.AMENITY_ID) AND (a.AMENITY = 'TV')"
                ");"
        },
        {
        "id": 3,
        "name": "Assigment1-Q3",
        "text":"Print all the hosts who have an available property between date 03.2019 and 09.2019.",
        "query":"SELECT DISTINCT h.HOST_ID, h.HOST_NAME"
                "FROM HOST h"
                "WHERE h.HOST_ID IN ("
                "	SELECT o.HOST_ID"
                "    FROM OFFER o"
                "    WHERE o.LISTING_ID IN ("
                "        SELECT c.LISTING_ID"
                "        FROM CALENDAR c"
                "        WHERE c.DATE_ >= TO_DATE('2019-03-01','YYYY-MM-DD') AND c.DATE_ <= TO_DATE('2019-09-01', 'YYYY-MM-DD') AND (c.AVAILABLE = 't')"
                "    )"
                ");"
        },
        {
        "id": 4,
        "name": "Assigment1-Q4",
        "text":"Print how many listing items exist that are posted by two different hosts but the hosts have the same name.",
        "query":"SELECT COUNT(o.listing_id)"
                "FROM Offer o"
                "WHERE o.host_id IN ("
                "	SELECT h1.host_id"
                "	FROM Host h1, Host h2"
                "	WHERE (h1.host_id <> h2.host_id) AND (h1.host_name = h2.host_name) AND (h1.HOST_NAME IS NOT NULL) AND (h2.HOST_NAME IS NOT NULL)"
                ");"
        },
        {
        "id": 5,
        "name": "Assigment1-Q5",
        "text":"Print all the dates that 'Viajes Eco' has available accommodations for rent.",
        "query":"SELECT DISTINCT c.DATE_"
                "FROM Calendar c"
                "WHERE c.AVAILABLE = 't' AND c.LISTING_ID IN ("
                    "SELECT o.LISTING_ID"
                    "FROM OFFER o, HOST h"
                    "WHERE (o.HOST_ID = h.HOST_ID) AND (h.HOST_NAME = 'Viajes Eco')"
                );"
        },
        {
        "id": 6,
        "name": "Assigment1-Q6",
        "text":"Find all the hosts (host_ids, host_names) that have only one listing.",
        "query":"SELECT h.HOST_ID, h.HOST_NAME"
                "FROM HOST h, OFFER o"
                "WHERE (h.HOST_ID = o.HOST_ID)"
                "GROUP BY h.HOST_ID, h.HOST_NAME"
                "HAVING COUNT(o.LISTING_ID) = 1;"
        },
        {
        "id": 7,
        "name": "Assigment1-Q7",
        "text":"Find the difference in the average price of listings with and without WIFI.",
        "query":"SELECT (SELECT AVG(p.price)"
                "FROM Prices p"
                "WHERE p.listing_id IN ("
                	"SELECT property.listing_id"
                	"FROM Property property"
                	"WHERE property.PROPERTY_ID IN ("
                	    "SELECT h.PROPERTY_ID"
                	    "FROM HAS_AMENITIES h, AMENITY a"
                	    "WHERE (h.AMENITY_ID = a.AMENITY_ID)"
                	        "AND (a.AMENITY = 'WIFI')"

                    ")"
                ")) - (SELECT AVG(p2.price)"
                "FROM Prices p2"
                "WHERE p2.listing_id IN ("
                    "SELECT property2.listing_id"
                	"FROM Property property2"
                	"WHERE property2.PROPERTY_ID IN ("
                	    "SELECT h2.PROPERTY_ID"
                	    "FROM HAS_AMENITIES h2, AMENITY a2"
                	    "WHERE h2.AMENITY_ID = a2.AMENITY_ID"
                	        "AND NOT a2.AMENITY = 'WIFI'"
                    ")"
                ")) from dual;"
        },
        {
        "id": 8,
        "name": "Assigment1-Q8",
        "text":"How much more (or less) costly to rent a room with 8 beds in Berlin compared to Madrid on average?",
        "query":"SELECT( SELECT AVG(p.price)"
                "FROM Prices p"
                "WHERE p.listing_id IN ("
                "	SELECT DISTINCT property2.listing_id"
                "	FROM Property property2"
                "	WHERE (property2.beds = 8) AND property2.property_id IN ("
                "		SELECT a2.property_id"
                "		FROM Address a2, City c2"
                "		WHERE a2.NEIGHBOURHOOD_ID IN ("
                "		    SELECT n2.NEIGHBOURHOOD_ID"
                "		    FROM NEIGHBOURHOOD n2, CITY c2"
                "		    WHERE (n2.CITY_ID = c2.CITY_ID) AND (c2.city = 'Madrid')"
                "        )"
                "    )"
                ")) -"
                "(SELECT AVG(p.PRICE)"
                "FROM Prices p"
                "WHERE p.listing_id IN ("
                "	SELECT DISTINCT property.listing_id"
                "	FROM Property property"
                "	WHERE (property.BEDS = 8) AND property.property_id IN ("
                "		SELECT a.property_id"
                "		FROM Address a"
                "		WHERE a.NEIGHBOURHOOD_ID IN ("
                "		    SELECT n.NEIGHBOURHOOD_ID"
                "		    FROM NEIGHBOURHOOD n, CITY c"
                "		    WHERE (n.CITY_ID = c.CITY_ID) AND (c.city = 'Berlin')"
                "        )"
                "    )"
                ") ) from dual;"
        },
        {
        "id": 9,
        "name": "Assigment1-Q9",
        "text":"Find the top-10	(in terms of the	number of listings) hosts (host_ids, host_names) in Spain.",
        "query":"SELECT h.host_id, h.host_name"
                "FROM Host h"
                "WHERE h.host_id IN ("
                "    SELECT HOST_ID"
                "    FROM ("
                "         SELECT o.HOST_ID, COUNT(o.HOST_ID) as cnt"
                "         FROM OFFER o"
                "         WHERE o.LISTING_ID IN ("
                "             SELECT p.LISTING_ID"
                "             FROM PROPERTY p, ADDRESS a"
                "             WHERE (a.PROPERTY_ID = p.PROPERTY_ID) AND a.NEIGHBOURHOOD_ID IN ("
                "                SELECT n.NEIGHBOURHOOD_ID"
                "                FROM NEIGHBOURHOOD n, CITY city, COUNTRY country"
                "                WHERE (n.CITY_ID = city.CITY_ID)"
                "                 AND (city.COUNTRY_ID = country.COUNTRY_ID)"
                "                 AND (country.COUNTRY = 'Spain')"
                "             )"
                "         )"
                "         GROUP BY o.HOST_ID"
                "         ORDER BY cnt DESC"
                "         FETCH FIRST 10 ROWS ONLY"
                "    )"
                ");"
        },
        {
        "id": 10,
        "name": "Assigment1-Q10",
        "text":"Find the top-10	rated (review_score_rating) apartments	(id,name) in Barcelona.",
        "query":"SELECT o.listing_id, o.name"
                "FROM Offer o, Scores s"
                "WHERE o.listing_id = s.listing_id AND (s.REVIEW_SCORES_RATING IS NOT NULL) AND o.listing_id IN ("
                "    SELECT p.listing_id"
                "    FROM Property p, Property_type pt"
                "    WHERE (p.property_type_id = pt.property_type_id) AND (pt.property_type = 'Apartment') AND p.property_id IN ("
                "        SELECT a.property_id"
                "        FROM Address a"
                "        WHERE a.NEIGHBOURHOOD_ID IN ("
                "            SELECT n.NEIGHBOURHOOD_ID"
                "            FROM NEIGHBOURHOOD n, CITY c"
                "            WHERE (n.CITY_ID = c.CITY_ID) AND (c.city = 'Barcelona')"
                "        )"
                "    )"
                ")"
                "ORDER BY s.REVIEW_SCORES_RATING DESC"
                "FETCH FIRST 10 ROWS ONLY;"
        }
    ]
    return queries_list
