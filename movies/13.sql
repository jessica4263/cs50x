SELECT name
FROM people
WHERE name != 'Kevin Bacon'
AND id IN(
    SELECT person_id
    FROM stars
    WHERE movie_id IN(
        SELECT id
        FROM movies
        WHERE id IN(
            SELECT movie_id
            FROM stars
            WHERE person_id IN(
                SELECT id
                FROM people
                WHERE birth = 1958 AND name = 'Kevin Bacon'
            )
        )
    )
);
