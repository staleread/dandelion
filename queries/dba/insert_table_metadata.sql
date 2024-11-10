-- :name insert_table_metadata :one
insert into metadata.table (title, is_private, is_protected)
values (:table_title, :is_private, :is_protected)
returning id
