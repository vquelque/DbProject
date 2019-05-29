def queries():
    queries_list= [
        {
        "id": 1,
        "name": "Assigment1-Q1",
        "text":"Find the average price for a listing with 8 bedrooms. ",
        "query":"SELECT AVG(price.price) "
                "FROM Prices price "
                "WHERE price.listing_id IN ( "
                "    SELECT property.listing_id "
                "    FROM Property property "
                "    WHERE property.bedrooms = 8 "
                ") "

        },
        {
        "id": 2,
        "name": "Assigment1-Q2",
        "text":"Find the average cleaning review score for listings with TV.",
        "query":"SELECT AVG(s.review_scores_cleanliness) "
                "FROM Scores s, Property p "
                "WHERE (p.listing_id = s.listing_id) AND p.PROPERTY_ID IN ( "
                "    SELECT h.PROPERTY_ID "
                "    FROM HAS_AMENITIES h, AMENITY a "
                "    WHERE (h.AMENITY_ID = a.AMENITY_ID) AND (a.AMENITY = 'TV') "
                ") "
        },
        {
        "id": 3,
        "name": "Assigment1-Q3",
        "text":"Print all the hosts who have an available property between date 03.2019 and 09.2019.",
        "query":"SELECT DISTINCT h.HOST_ID, h.HOST_NAME "
                "FROM HOST h "
                "WHERE h.HOST_ID IN ( "
                "	SELECT o.HOST_ID "
                "    FROM OFFER o "
                "    WHERE o.LISTING_ID IN ( "
                "        SELECT c.LISTING_ID "
                "        FROM CALENDAR c "
                "        WHERE c.DATE_ >= TO_DATE('2019-03-01','YYYY-MM-DD') AND c.DATE_ <= TO_DATE('2019-09-01', 'YYYY-MM-DD') AND (c.AVAILABLE = 't') "
                "    ) "
                ") "
        },
        {
        "id": 4,
        "name": "Assigment1-Q4",
        "text":"Print how many listing items exist that are posted by two different hosts but the hosts have the same name.",
        "query":"SELECT COUNT(o.listing_id) "
                "FROM Offer o "
                "WHERE o.host_id IN ( "
                "	SELECT h1.host_id "
                "	FROM Host h1, Host h2 "
                "	WHERE (h1.host_id <> h2.host_id) AND (h1.host_name = h2.host_name) AND (h1.HOST_NAME IS NOT NULL) AND (h2.HOST_NAME IS NOT NULL) "
                ") "
        },
        {
        "id": 5,
        "name": "Assigment1-Q5",
        "text":"Print all the dates that 'Viajes Eco' has available accommodations for rent.",
        "query":"SELECT DISTINCT c.DATE_ "
                "FROM Calendar c "
                "WHERE c.AVAILABLE = 't' AND c.LISTING_ID IN ( "
                    "SELECT o.LISTING_ID "
                    "FROM OFFER o, HOST h "
                    "WHERE (o.HOST_ID = h.HOST_ID) AND (h.HOST_NAME = 'Viajes Eco') "
                ");"
        },
        {
        "id": 6,
        "name": "Assigment1-Q6",
        "text":"Find all the hosts (host_ids, host_names) that have only one listing.",
        "query":"SELECT h.HOST_ID, h.HOST_NAME "
                "FROM HOST h, OFFER o "
                "WHERE (h.HOST_ID = o.HOST_ID) "
                "GROUP BY h.HOST_ID, h.HOST_NAME "
                "HAVING COUNT(o.LISTING_ID) = 1 "
        },
        {
        "id": 7,
        "name": "Assigment1-Q7",
        "text":"Find the difference in the average price of listings with and without WIFI.",
        "query":"SELECT (SELECT AVG(p.price) "
                "FROM Prices p "
                "WHERE p.listing_id IN ( "
                	"SELECT property.listing_id "
                	"FROM Property property "
                	"WHERE property.PROPERTY_ID IN ( "
                	    "SELECT h.PROPERTY_ID "
                	    "FROM HAS_AMENITIES h, AMENITY a "
                	    "WHERE (h.AMENITY_ID = a.AMENITY_ID) "
                	        "AND (a.AMENITY = 'WIFI') "

                    ") "
                ")) - (SELECT AVG(p2.price) "
                "FROM Prices p2 "
                "WHERE p2.listing_id IN ( "
                    "SELECT property2.listing_id "
                	"FROM Property property2 "
                	"WHERE property2.PROPERTY_ID IN ( "
                	    "SELECT h2.PROPERTY_ID "
                	    "FROM HAS_AMENITIES h2, AMENITY a2 "
                	    "WHERE h2.AMENITY_ID = a2.AMENITY_ID "
                	        "AND NOT a2.AMENITY = 'WIFI' "
                    ") "
                ")) from dual "
        },
        {
        "id": 8,
        "name": "Assigment1-Q8",
        "text":"How much more (or less) costly to rent a room with 8 beds in Berlin compared to Madrid on average?",
        "query":"SELECT( SELECT AVG(p.price) "
                "FROM Prices p "
                "WHERE p.listing_id IN ( "
                "	SELECT DISTINCT property2.listing_id "
                "	FROM Property property2 "
                "	WHERE (property2.beds = 8) AND property2.property_id IN ( "
                "		SELECT a2.property_id "
                "		FROM Address a2, City c2 "
                "		WHERE a2.NEIGHBOURHOOD_ID IN ( "
                "		    SELECT n2.NEIGHBOURHOOD_ID "
                "		    FROM NEIGHBOURHOOD n2, CITY c2 "
                "		    WHERE (n2.CITY_ID = c2.CITY_ID) AND (c2.city = 'Madrid') "
                "        ) "
                "    ) "
                ")) - "
                "(SELECT AVG(p.PRICE) "
                "FROM Prices p "
                "WHERE p.listing_id IN ( "
                "	SELECT DISTINCT property.listing_id "
                "	FROM Property property "
                "	WHERE (property.BEDS = 8) AND property.property_id IN ( "
                "		SELECT a.property_id "
                "		FROM Address a "
                "		WHERE a.NEIGHBOURHOOD_ID IN ( "
                "		    SELECT n.NEIGHBOURHOOD_ID "
                "		    FROM NEIGHBOURHOOD n, CITY c "
                "		    WHERE (n.CITY_ID = c.CITY_ID) AND (c.city = 'Berlin') "
                "        ) "
                "    ) "
                ") ) from dual "
        },
        {
        "id": 9,
        "name": "Assigment1-Q9",
        "text":"Find the top-10	(in terms of the	number of listings) hosts (host_ids, host_names) in Spain.",
        "query":"SELECT h.host_id, h.host_name "
                "FROM Host h "
                "WHERE h.host_id IN ( "
                "    SELECT HOST_ID "
                "    FROM ( "
                "         SELECT o.HOST_ID, COUNT(o.HOST_ID) as cnt "
                "         FROM OFFER o "
                "         WHERE o.LISTING_ID IN ( "
                "             SELECT p.LISTING_ID "
                "             FROM PROPERTY p, ADDRESS a "
                "             WHERE (a.PROPERTY_ID = p.PROPERTY_ID) AND a.NEIGHBOURHOOD_ID IN ( "
                "                SELECT n.NEIGHBOURHOOD_ID "
                "                FROM NEIGHBOURHOOD n, CITY city, COUNTRY country "
                "                WHERE (n.CITY_ID = city.CITY_ID) "
                "                 AND (city.COUNTRY_ID = country.COUNTRY_ID) "
                "                 AND (country.COUNTRY = 'Spain') "
                "             ) "
                "         ) "
                "         GROUP BY o.HOST_ID "
                "         ORDER BY cnt DESC "
                "         FETCH FIRST 10 ROWS ONLY "
                "    ) "
                ") "
        },
        {
        "id": 10,
        "name": "Assigment1-Q10",
        "text":"Find the top-10	rated (review_score_rating) apartments	(id,name) in Barcelona.",
        "query":"SELECT o.listing_id, o.name "
                "FROM Offer o, Scores s "
                "WHERE o.listing_id = s.listing_id AND (s.REVIEW_SCORES_RATING IS NOT NULL) AND o.listing_id IN ( "
                "    SELECT p.listing_id "
                "    FROM Property p, Property_type pt "
                "    WHERE (p.property_type_id = pt.property_type_id) AND (pt.property_type = 'Apartment') AND p.property_id IN ( "
                "        SELECT a.property_id "
                "        FROM Address a "
                "        WHERE a.NEIGHBOURHOOD_ID IN ( "
                "            SELECT n.NEIGHBOURHOOD_ID "
                "            FROM NEIGHBOURHOOD n, CITY c "
                "            WHERE (n.CITY_ID = c.CITY_ID) AND (c.city = 'Barcelona') "
                "        ) "
                "    ) "
                ") "
                "ORDER BY s.REVIEW_SCORES_RATING DESC "
                "FETCH FIRST 10 ROWS ONLY "
        },
        {
        "id": 11,
        "name": "Assigment2-Q1",
        "text":"Print how many hosts in each city have declared the area of their property in square meters. Sort the output based on the city name in ascending order.",
        "query":"SELECT c.CITY, COUNT(DISTINCT o.HOST_ID) as cnt_host "
                "FROM OFFER o, PROPERTY p, ADDRESS a, CITY c, NEIGHBOURHOOD n "
                "WHERE p.SQUARE_FEET IS NOT NULL AND p.PROPERTY_ID = a.PROPERTY_ID "
                "  AND a.NEIGHBOURHOOD_ID = n.NEIGHBOURHOOD_ID AND o.LISTING_ID = p.LISTING_ID "
                "  AND n.CITY_ID = c.CITY_ID "
                "GROUP BY c.CITY "
                "ORDER BY cnt_host "
        },
        {
        "id": 12,
        "name": "Assigment2-Q2",
        "text":"The quality of a neighborhood is defined based on the number of listings and the review score of these listings, one way for computing that is using the median of the review scores, as medians are more robust to outliers. Find the top-5 neighborhoods using median review scores of listings in Madrid. Note: Implement the median operator on your own, and do not use the available built-in operator.",
        "query":"WITH BASE AS "
                "( "
                "    SELECT n.NEIGHBOURHOOD_ID, n.NEIGHBOURHOOD, s.REVIEW_SCORES_RATING, s.LISTING_ID "
                "    FROM NEIGHBOURHOOD n, ADDRESS a, PROPERTY p, SCORES s, CITY c "
                "    WHERE n.NEIGHBOURHOOD_ID = a.NEIGHBOURHOOD_ID and "
                "       a.PROPERTY_ID = p.PROPERTY_ID and "
                "       s.LISTING_ID = p.LISTING_ID and "
                "       s.REVIEW_SCORES_RATING > 0 and "
                "       n.CITY_ID = c.CITY_ID and "
                "       c.CITY = 'Madrid' "
                "       and s.REVIEW_SCORES_RATING IS NOT NULL "
                ") "
                "SELECT "
                "   NEIGHBOURHOOD_ID, NEIGHBOURHOOD "
                "FROM "
                "( "
                "   SELECT "
                "      NEIGHBOURHOOD_ID, NEIGHBOURHOOD, "
                "      REVIEW_SCORES_RATING, "
                "      ROW_NUMBER() OVER ( "
                "         PARTITION BY base.NEIGHBOURHOOD_ID "
                "         ORDER BY base.REVIEW_SCORES_RATING ASC, base.LISTING_ID ASC) AS RowAsc, "
                "      ROW_NUMBER() OVER ( "
                "         PARTITION BY base.NEIGHBOURHOOD_ID "
                "         ORDER BY base.REVIEW_SCORES_RATING DESC, base.LISTING_ID DESC) AS RowDesc "
                "   FROM BASE base "
                ") x "
                "WHERE "
                "   RowAsc IN (RowDesc, RowDesc - 1, RowDesc + 1) "
                "GROUP BY NEIGHBOURHOOD_ID, NEIGHBOURHOOD "
                "ORDER BY AVG(REVIEW_SCORES_RATING) DESC "
                "FETCH FIRST 5 ROWS ONLY "
        },
        {
        "id": 13,
        "name": "Assigment2-Q3",
        "text":"Find all the hosts (host_ids, host_names) with the highest number of listings.",
        "query":"SELECT h.HOST_ID, h.HOST_NAME "
                "FROM HOST h, OFFER o "
                "WHERE (h.HOST_ID = o.HOST_ID) "
                "GROUP BY h.HOST_ID, h.HOST_NAME "
                "HAVING COUNT(h.HOST_ID) = "
                "      (SELECT MAX(cnt.nb_listing) "
                "       FROM ( "
                "               SELECT h.HOST_ID, h.HOST_NAME, COUNT(h.HOST_ID) AS nb_listing "
                "               FROM HOST h, "
                "                    OFFER o "
                "               WHERE (h.HOST_ID = o.HOST_ID) "
                "               GROUP BY h.HOST_ID, h.HOST_NAME "
                "           ) cnt "
                "      ) "
        },
        {
        "id": 14,
        "name": "Assigment2-Q4",
        "text":"Find the 5 most cheapest Apartments (based on average price within the available dates) in Berlin available between 01-03-2019 and 30-04-2019 having at least 2 beds, a location review score of at least 8, flexible cancellation, and listed by a host with a verifiable government id.",
        "query":"SELECT o.LISTING_ID, o.NAME"
                "FROM PROPERTY p, OFFER o, SCORES sc, CALENDAR cal, CANCELLATION_POLICY cp "
                "WHERE (p.BEDS >= 2) "
                "    AND (p.PROPERTY_ID IN ( "
                "            SELECT address.PROPERTY_ID "
                "            FROM ADDRESS address "
                "            WHERE address.NEIGHBOURHOOD_ID IN ( "
                "                SELECT n.NEIGHBOURHOOD_ID "
                "                FROM NEIGHBOURHOOD n, CITY c "
                "                WHERE (n.CITY_ID = c.CITY_ID) AND (c.city = 'Barcelona') "
                "            ) "
                "        ) "
                "    ) "
                "    AND (p.PROPERTY_TYPE_ID IN ( "
                "        SELECT pt.PROPERTY_TYPE_ID "
                "        FROM PROPERTY_TYPE pt "
                "        WHERE (pt.PROPERTY_TYPE = 'Apartment') "
                "        ) "
                "    ) "
                "    AND (o.HOST_ID IN ( "
                "        SELECT h.HOST_ID "
                "        FROM HOST h "
                "        WHERE h.HOST_ID IN ( "
                "            SELECT has_h.HOST_ID "
                "            FROM HAS_HOST_VERIFICATION has_h "
                "            WHERE has_h.HOST_VERIFICATION_ID IN ( "
                "                SELECT host_v.HOST_VERIFICATION_ID "
                "                FROM HOST_VERIFICATION host_v "
                "                WHERE host_v.HOST_VERIFICATION = 'GOVERNMENT_ID' "
                "            ) "
                "        ) "
                "    )) "
                "    AND (cp.CANCELLATION_POLICY = 'flexible') "
                "    AND (sc.REVIEW_SCORES_LOCATION >= 8) "
                "    AND (cal.DATE_ >= TO_DATE('2019-03-01', 'YYYY-MM-DD')) "
                "    AND (cal.DATE_ <= TO_DATE('2019-04-30', 'YYYY-MM-DD')) "
                "    AND (cal.AVAILABLE = 't') "
                "    AND (o.LISTING_ID = sc.LISTING_ID) "
                "    AND (o.LISTING_ID = p.LISTING_ID) "
                "    AND (o.LISTING_ID = cal.LISTING_ID) "
                "    AND (cp.CANCELLATION_POLICY_ID = o.CANCELLATION_POLICY_ID) "
                "GROUP BY o.LISTING_ID, o.NAME "
                "ORDER BY AVG(cal.PRICE) "
                "FETCH FIRST 5 ROWS ONLY "
        },
        {
        "id": 15,
        "name": "Assigment2-Q5",
        "text":"Each property can accommodate different number of people (1 to 16). Find the top-5 rated (review_score_rating) listings for each distinct category based on number of accommodated guests with at least two of these facilities: Wifi, Internet, TV, and Free street parking.",
        "query":"SELECT cnt.ACCOMMODATES, cnt.listing_id, cnt.NAME "
                "FROM "
                "( "
                    "SELECT p.ACCOMMODATES, o.LISTING_ID, o.NAME, s.REVIEW_SCORES_RATING, ROW_NUMBER() over (partition by p.ACCOMMODATES ORDER BY s.REVIEW_SCORES_RATING DESC ) AS rk "
                    "FROM PROPERTY p, SCORES s, OFFER o "
                    "WHERE (p.ACCOMMODATES >= 1) AND (p.ACCOMMODATES <= 16) "
                      "AND (o.LISTING_ID = s.LISTING_ID) "
                      "AND (s.REVIEW_SCORES_RATING IS NOT NULL) "
                      "AND (p.LISTING_ID = o.LISTING_ID) "
                      "AND p.PROPERTY_ID IN ( "
                        "SELECT has_a.PROPERTY_ID "
                        "FROM HAS_AMENITIES has_a, AMENITY amenity "
                        "WHERE (has_a.AMENITY_ID = amenity.AMENITY_ID) "
                          "AND (amenity.AMENITY IN ('WIFI', 'Internet', 'TV', 'Free street parking')) "
                        "GROUP BY has_a.PROPERTY_ID "
                        "HAVING COUNT(DISTINCT amenity.AMENITY) >= 2 "
                      ") "
                ") cnt WHERE cnt.rk <= 5 "
        },
        {
        "id": 16,
        "name": "Assigment2-Q6",
        "text":"What are top three busiest listings per host? The more reviews a listing has, the busier the listing is.",
        "query":"SELECT rk_tab.HOST_ID, rk_tab.HOST_NAME, rk_tab.LISTING_ID "
                "FROM ( "
                    "SELECT dmp.LISTING_ID, dmp.HOST_ID, dmp.HOST_NAME, dmp.cnt, ROW_NUMBER() OVER ( partition by dmp.HOST_ID ORDER BY dmp.cnt DESC ) AS rk "
                    "FROM ( "
                        "SELECT o.LISTING_ID, o.HOST_ID, h.HOST_NAME, COUNT(o.LISTING_ID) AS cnt "
                        "FROM  HOST h, OFFER o, REVIEW r "
                        "WHERE (h.HOST_ID = o.HOST_ID) AND (o.LISTING_ID = r.LISTING_ID) "
                        "GROUP BY o.HOST_ID, o.LISTING_ID, h.HOST_NAME "
                    ") dmp "
                ") rk_tab WHERE rk <= 3" "
        },
        {
        "id": 17,
        "name": "Assigment2-Q7",
        "text":"What are the three most frequently used amenities at each neighborhood in Berlin for the listings with “Private Room” room type?",
        "query":"SELECT rk_tab.NEIGHBOURHOOD_ID, rk_tab.AMENITY "
                "FROM "
                "( "
                    "SELECT dmp.NEIGHBOURHOOD_ID, dmp.AMENITY, DMP.cnt, ROW_NUMBER() over ( partition by dmp.NEIGHBOURHOOD_ID ORDER BY dmp.cnt DESC ) AS rk "
                    "FROM "
                    "( "
                        "SELECT n.NEIGHBOURHOOD_ID, amenity.AMENITY, COUNT(amenity.AMENITY) AS cnt "
                        "FROM PROPERTY p, ROOM_TYPE r, HAS_AMENITIES has_a, AMENITY amenity, ADDRESS a, NEIGHBOURHOOD n, CITY c "
                        "WHERE (r.ROOM_TYPE = 'Private room') "
                            "AND (p.ROOM_TYPE_ID = r.ROOM_TYPE_ID) "
                            "AND (has_a.PROPERTY_ID = p.PROPERTY_ID) "
                            "AND (has_a.AMENITY_ID = amenity.AMENITY_ID) "
                            "AND (a.PROPERTY_ID = p.PROPERTY_ID) "
                            "AND (a.NEIGHBOURHOOD_ID = n.NEIGHBOURHOOD_ID) "
                            "AND (n.CITY_ID = c.CITY_ID) "
                            "AND (c.CITY = 'Berlin') "
                        "GROUP BY n.NEIGHBOURHOOD_ID, amenity.AMENITY "
                    ") dmp "
                ") rk_tab WHERE rk <= 3 "
        },
        {
        "id": 18,
        "name": "Assigment2-Q8",
        "text":"What is the difference in the average communication review score of the host who has the most diverse way of verifications and of the host who has the least diverse way of verifications. In case of a multiple number of the most or the least diverse verifying hosts, pick a host one from the most and one from the least verifying hosts.",
        "query":"WITH BASE AS "
                "( "
                    "SELECT h.HOST_ID, AVG(s.REVIEW_SCORES_COMMUNICATION) avg_s, COUNT(DISTINCT has_v.HOST_VERIFICATION_ID) AS cnt "
                    "FROM OFFER o, "
                         "SCORES s, "
                         "HOST h LEFT JOIN HAS_HOST_VERIFICATION has_v ON h.HOST_ID = has_v.HOST_ID "
                    "WHERE (s.LISTING_ID = o.LISTING_ID) "
                       "AND (o.HOST_ID = h.HOST_ID) "
                       "AND (s.REVIEW_SCORES_COMMUNICATION IS NOT NULL) "
                    "GROUP BY h.HOST_ID "
                ") "
                "SELECT least.avg_s - high.avg_s "
                "FROM (SELECT base.avg_s "
                      "FROM BASE base "
                      "ORDER BY base.cnt "
                      "FETCH FIRST ROW ONLY "
                   ") least, "
                   "( "
                       "SELECT base.avg_s "
                       "FROM BASE base "
                       "ORDER BY base.cnt DESC "
                       "FETCH FIRST ROW ONLY "
                   ") high "
        },
        {
        "id": 19,
        "name": "Assigment2-Q9",
        "text":"What is the city who has the highest number of reviews for the room types whose average number of accommodates are greater than 3.",
        "query":"SELECT rk_tab.CITY, rk_tab.ROOM_TYPE "
                "FROM "
                "( "
                    "SELECT dmp.CITY, dmp.ROOM_TYPE, RANK() over ( partition by dmp.ROOM_TYPE_ID ORDER BY dmp.cnt DESC ) AS rk "
                    "FROM "
                    "( "
                        "SELECT c.CITY_ID, c.CITY, rt.ROOM_TYPE_ID, rt.ROOM_TYPE, COUNT(DISTINCT r.REVIEW_ID) AS cnt "
                        "FROM CITY c, REVIEW r, ROOM_TYPE rt, PROPERTY p, ADDRESS a, NEIGHBOURHOOD n "
                        "WHERE (p.LISTING_ID = r.LISTING_ID) "
                            "AND (p.ROOM_TYPE_ID = rt.ROOM_TYPE_ID) "
                            "AND (p.PROPERTY_ID = a.PROPERTY_ID) "
                            "AND (a.NEIGHBOURHOOD_ID = n.NEIGHBOURHOOD_ID) "
                            "AND (n.NEIGHBOURHOOD_ID = c.CITY_ID) "
                        "GROUP BY RT.ROOM_TYPE_ID, rt.ROOM_TYPE, c.CITY_ID, c.CITY "
                        "HAVING AVG(p.ACCOMMODATES) > 3 "
                    ") dmp "
                ") rk_tab WHERE rk <= 1 "
        },
        {
        "id": 20,
        "name": "Assigment2-Q10",
        "text":"Print all the neighbourhouds in Madrid which had at least 50 percent of their listings occupied in 2019 and their host has joined airbnb no later than 01.06.2017.",
        "query":"WITH BASE AS ( "
                "SELECT n.NEIGHBOURHOOD_ID, p.LISTING_ID, n.NEIGHBOURHOOD, c.AVAILABLE "
                "FROM NEIGHBOURHOOD n, "
                     "ADDRESS a, "
                     "PROPERTY p, "
                     "CITY city, "
                     "HOST h, "
                     "OFFER o, "
                     "CALENDAR c "
                "WHERE (city.CITY = 'Madrid') "
                  "AND (h.HOST_SINCE <= TO_DATE('2017-06-01', 'YYYY-MM-DD')) "
                  "AND (a.PROPERTY_ID = p.PROPERTY_ID) "
                  "AND (a.NEIGHBOURHOOD_ID = n.NEIGHBOURHOOD_ID) "
                  "AND (city.CITY_ID = n.CITY_ID) "
                  "AND (p.LISTING_ID = p.LISTING_ID) "
                  "AND (o.HOST_ID = h.HOST_ID) "
                  "AND (o.LISTING_ID = p.LISTING_ID) "
                  "AND (c.DATE_ >= TO_DATE('2019-01-01', 'YYYY-MM-DD')) "
                  "AND (c.DATE_ <= TO_DATE('2019-12-31', 'YYYY-MM-DD')) "
                  "AND (o.LISTING_ID = c.LISTING_ID) "
            ") "
            "SELECT partial.NEIGHBOURHOOD_ID, partial.NEIGHBOURHOOD "
            "FROM (SELECT b.NEIGHBOURHOOD_ID, b.NEIGHBOURHOOD, COUNT(DISTINCT b.LISTING_ID) as cnt_partial "
                "FROM BASE b "
                "WHERE (b.AVAILABLE = 'f') "
                "GROUP BY b.NEIGHBOURHOOD_ID, b.NEIGHBOURHOOD "
               ") partial, "
               "( "
                   "SELECT b.NEIGHBOURHOOD_ID, b.NEIGHBOURHOOD, COUNT(DISTINCT b.LISTING_ID) as cnt_total "
                   "FROM BASE b "
                   "GROUP BY b.NEIGHBOURHOOD_ID, b.NEIGHBOURHOOD "
               ") total "
                "WHERE (partial.NEIGHBOURHOOD_ID = total.NEIGHBOURHOOD_ID) "
                    "AND ((partial.cnt_partial/total.cnt_total) >= 0.5) "
        },
        {
        "id": 21,
        "name": "Assigment2-Q11",
        "text":"Print all the countries that had at least 20% of their listings available at some date in year 2018",
        "query":"WITH BASE AS ( "
                "SELECT country.COUNTRY_ID, COUNTRY.COUNTRY, p.LISTING_ID, c.AVAILABLE "
                   "FROM NEIGHBOURHOOD n, "
                     "ADDRESS a, "
                     "PROPERTY p, "
                     "CITY city, "
                     "COUNTRY country, "
                     "CALENDAR c "
                   "WHERE (a.PROPERTY_ID = p.PROPERTY_ID) "
                     "AND (a.NEIGHBOURHOOD_ID = n.NEIGHBOURHOOD_ID) "
                     "AND (city.CITY_ID = n.CITY_ID) "
                     "AND (city.COUNTRY_ID = country.COUNTRY_ID) "
                     "AND (c.LISTING_ID = p.LISTING_ID) "
                     "AND (c.DATE_ >= TO_DATE('2018-01-01', 'YYYY-MM-DD')) "
                     "AND (c.DATE_ <= TO_DATE('2018-12-31', 'YYYY-MM-DD')) "
            ") "
            "SELECT partial.COUNTRY_ID, partial.COUNTRY "
            "FROM (SELECT base.COUNTRY_ID, base.COUNTRY, COUNT(DISTINCT base.LISTING_ID) as cnt_partial "
                "FROM BASE base "
                "WHERE (base.AVAILABLE = 't') "
                  "AND (base.LISTING_ID = base.LISTING_ID) "
                "GROUP BY base.COUNTRY_ID, base.COUNTRY "
               ") partial, "
               "( "
                   "SELECT base.COUNTRY_ID, base.COUNTRY, COUNT(DISTINCT base.LISTING_ID) as cnt_total "
                   "FROM BASE base "
                   "WHERE (base.LISTING_ID = base.LISTING_ID) "
                   "GROUP BY base.COUNTRY_ID, base.COUNTRY "
               ") total "
                "WHERE (partial.COUNTRY_ID = total.COUNTRY_ID) "
                    "AND ((partial.cnt_partial/total.cnt_total) >= 0.2) "
        },
        {
        "id": 22,
        "name": "Assigment2-Q12",
        "text":"Print all the neighborhoods in Barcelona where more than 5 percent of their accommodation’s cancelation policy is strict with grace period.",
        "query":"WITH BASE AS ( "
                "SELECT n.NEIGHBOURHOOD_ID, n.NEIGHBOURHOOD, o.CANCELLATION_POLICY_ID, o.LISTING_ID, cp.CANCELLATION_POLICY "
                "FROM NEIGHBOURHOOD n, "
                     "ADDRESS a, "
                     "PROPERTY p, "
                     "CITY city, "
                     "OFFER o, "
                     "CANCELLATION_POLICY cp "
                "WHERE (city.CITY = 'Barcelona') "
                  "AND (a.PROPERTY_ID = p.PROPERTY_ID) "
                  "AND (a.NEIGHBOURHOOD_ID = n.NEIGHBOURHOOD_ID) "
                  "AND (city.CITY_ID = n.CITY_ID) "
                  "AND (p.LISTING_ID = o.LISTING_ID) "
            ") "
            "SELECT partial.NEIGHBOURHOOD_ID, partial.NEIGHBOURHOOD "
            "FROM (SELECT base.NEIGHBOURHOOD_ID, base.NEIGHBOURHOOD, COUNT(DISTINCT base.LISTING_ID) as cnt_partial "
                "FROM BASE base "
                "WHERE (base.CANCELLATION_POLICY = 'strict_14_with_grace_period') "
                "GROUP BY base.NEIGHBOURHOOD_ID, base.NEIGHBOURHOOD "
               ") partial, "
               "( "
                   "SELECT base.NEIGHBOURHOOD_ID, base.NEIGHBOURHOOD, COUNT(DISTINCT base.LISTING_ID) as cnt_total "
                   "FROM BASE base "
                   "GROUP BY base.NEIGHBOURHOOD_ID, base.NEIGHBOURHOOD "
               ") total "
                "WHERE (partial.NEIGHBOURHOOD_ID = total.NEIGHBOURHOOD_ID) "
                    "AND ((partial.cnt_partial/total.cnt_total) >= 0.05) "
        }
    ]
    return queries_list
