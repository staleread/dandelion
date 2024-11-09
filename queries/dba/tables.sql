-- :name all_table_names :many
select table_name 
from information_schema.tables 
where table_schema = 'public' and table_type = 'BASE TABLE'
order by table_name;
