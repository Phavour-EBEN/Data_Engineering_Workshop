{% set films_title = 'Dunkirk' %}

SELECT *
FROM {{ ref('films') }}
WHERE title = '{{ films_title }}'