-- :name get_public_table :one
select * from metadata.table
where is_private = false and id = :table_id
