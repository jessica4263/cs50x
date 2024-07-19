-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Start Information: Date: 07.28.2023, Street: Humphrey Street.

-- Find crime scene report description with the start information:
SELECT description
FROM crime_scene_reports
WHERE year = 2023 AND day = 28 AND street = 'Humphrey Street';
-- New Information: Time:10:15am, Place: Humphrey Street bakery Witnesses: 3 present and mention the bakery.Littering time: 16:36. No known witnesses.

-- Find the transcripts and names from the interviews of the 3 witnesses.
SELECT transcript, name, id
FROM interviews
WHERE year = 2023 AND day = 28 AND month = 07 AND transcript LIKE '%bakery%';
-- New Information:
-- Witness 1. Ruth: Within 10 min of the theft the thief got into a car in the bakery parking lot and drove away. Lead: Check security footage of parkig lot
-- Witness 2. Eugene: Saw the thief withdrawing money at the the ATM on Leggett Street. Lead: Bakery name "Emma's bakery", check ATM transactions.
-- Witness 3. Raymond: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. They were planning to take
    -- the earliest flight out of Fiftyville tomorrow. The person on the phone purchased the flight ticket. Lead: The person on the phone is the accomplice
    -- check flights, check phone calls at this time.

-- Find activity and license plate from the security footage of the parking lot of Emma's bakery after 10:20.
SELECT license_plate, activity, hour, minute
FROM bakery_security_logs
WHERE year = 2023 AND day = 28 AND month = 07 AND hour = 10 AND minute >= 15
ORDER BY minute;
-- New information: 5 possible License plates:
--| 5P2BI95       | exit     | 10   | 16     |
--| 94KL13X       | exit     | 10   | 18     |
--| 6P58WS2       | exit     | 10   | 18     |
--| 4328GD8       | exit     | 10   | 19     |
--| G412CB7       | exit     | 10   | 20     |
--| L93JTIZ       | exit     | 10   | 21     |
--| 322JW7E       | exit     | 10   | 23     |
--| 0NTHK55       | exit     | 10   | 23     |
--| 1106N58       | exit     | 10   | 35     |

-- Find people with this license plate
SELECT name, phone_number, passport_number, license_plate
FROM people
WHERE license_plate IN(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023 AND day = 28 AND month = 07 AND hour = 10 AND minute >= 15 AND minute <=35
);
-- New information:
-- Suspects: Vanessa, Barry, Iman, Sofia, Taylor, Luca, Diana, Kelsey, Bruce
-- Find atm transactions on Leggett Street that matches the ID from the suspects.
SELECT name
FROM people
WHERE id IN(
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN(
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2023 AND day = 28 AND month = 07 AND atm_location = 'Leggett Street'
    )
)
AND name IN(
    SELECT name
    FROM people
    WHERE license_plate IN(
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023 AND day = 28 AND month = 07 AND hour = 10 AND minute >= 15 AND minute <=35
    )
);
-- New information:
-- Suspect 1 : Iman
-- Suspect 2 : Taylor
-- Suspect 3 : Luca
-- Suspect 2 : Diana
-- Suspect 3 : Bruce

-- Find phone calls from that day and time from 3 suspects:
SELECT caller, receiver, duration
FROM phone_calls
WHERE year = 2023 AND day = 28 AND month = 07 AND caller
IN('(829) 555-5269', '(286) 555-6063', '(770) 555-1861', '(389) 555-5198', '(367) 555-5533')
ORDER BY duration, caller;
-- New information:
-- Suspect 1 : Taylor made a call duration: 43 to (676) 555-6554
-- Suspect 2 : Diana made a call duration: 49 to (725) 555-3243
-- Suspect 3 : Bruce made a call duration: 45 to (375) 555-8161

-- Find the name of the Accomplice Suspect with the phone number of the receiver:

-- New information:
-- Accomplice Suspect 1: James (676) 555-6554
-- Accomplice Suspect 2: Phillip (725) 555-3243
-- Accomplice Suspect 3: Robin (375) 555-8161

-- Find if the suspects are passengers on any flight:
SELECT passengers.passport_number, flight_id, name
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
WHERE phone_number IN('(286) 555-6063', '(770) 555-1861', '(676) 555-6554', '(725) 555-3243', '(375) 555-8161', '(367) 555-5533')
ORDER BY passengers.passport_number;
--New information:
-- Taylor: Flight 36
-- Jammes: Flight 10, 21, 47
-- Philip: Flight 10, 28, 47
-- Diana: Flight 18, 24, 54
-- Bruce: Flight 36

-- Find the first flights from the day after robbery with the city and names
SELECT people.name, passengers.passport_number, flights.id, airports.city, flights.hour, flights.minute, flights.origin_airport_id, flights.destination_airport_id
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE passengers.passport_number IN(1988161715, 2438825627, 3391710505, 3592750733)
AND flights.id IN(36, 10, 21, 28, 47, 18, 24, 54)
AND flights.origin_airport_id = 8
ORDER BY flights.hour, flights.minute;
-- Find the city from origin and destination of the flights: 8, 4, 5, 6, 3
SELECT city, id
FROM airports
WHERE id IN(8, 4, 5, 6, 3);
-- New information:
-- City: | Los Angeles   | 3  |
-- City: | New York City | 4  |
-- City: | Dallas        | 5  |
-- City: | Boston        | 6  |
-- City: | Fiftyville    | 8  |
-- Taylor and Bruce flew on the first flight at 8:20 am from Fiftyville to New York City i think he is the thief but James and Philip both flew at the
    -- same time so both are still accomplice suspects.

-- Find bank accounts to see if there was a transaction beetween these people
SELECT people.name, bank_accounts.account_number, atm_transactions.transaction_type, atm_transactions.amount
FROM atm_transactions
JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
JOIN people ON bank_accounts.person_id = people.id
WHERE people.passport_number IN(1988161715, 2438825627, 3391710505, 3592750733, 5773159633)
AND atm_transactions.year = 2023 AND atm_transactions.day = 28 AND atm_transactions.month = 07
AND atm_transactions.atm_location = 'Leggett Street';
-- New information
-- Taylor withdrew 60
-- Diana withdrew 35
-- Bruce withdrew 50

-- Find the day of the flights
SELECT people.name, passengers.passport_number, flights.id, airports.city, flights.hour, flights.minute, flights.origin_airport_id, flights.destination_airport_id
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE passengers.passport_number IN(1988161715, 2438825627, 3391710505, 3592750733, 5773159633)
AND flights.id IN(36, 10, 21, 28, 47, 18, 24, 54)
AND flights.origin_airport_id = 8
AND year = 2023 AND day = 29 AND month = 07
ORDER BY flights.hour, flights.minute;
-- New information: Taylor left on the flight at 8:20am to New York City on the next day and Diana left on the flight at 16:00
--Find if Diana is on the first flight to Boston and fint if Taylor is on the first flight to Newyork
SELECT people.name, passengers.passport_number, flights.id, airports.city, flights.hour, flights.minute, flights.origin_airport_id, flights.destination_airport_id
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE flights.origin_airport_id = 8
AND flights.destination_airport_id = 6
AND year = 2023 AND day = 29 AND month = 07
ORDER BY flights.hour, flights.minute
LIMIT 15;
-- Diana is on the first flight to boston
SELECT people.name, passengers.passport_number, flights.id, airports.city, flights.hour, flights.minute, flights.origin_airport_id, flights.destination_airport_id
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE flights.origin_airport_id = 8
AND flights.destination_airport_id = 4
AND year = 2023 AND day = 29 AND month = 07
ORDER BY flights.hour, flights.minute
LIMIT 15;
-- Taylor and Bruce are on the first flight to newyork
-- Find the first flight from Fiftyville
SELECT people.name, passengers.passport_number, flights.id, airports.city, flights.hour, flights.minute, flights.origin_airport_id, flights.destination_airport_id
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE flights.origin_airport_id = 8
AND year = 2023 AND day = 29 AND month = 07
ORDER BY flights.hour, flights.minute
LIMIT 15;
-- The first flight is to New york at 8:20


