-- :name table_columns :many
select column_name
from information_schema.columns
where table_name = :table_name