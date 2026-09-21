
-- Use the `ref` function to select from other models

select *
from {{ source('destination_db', 'film_actors') }}
