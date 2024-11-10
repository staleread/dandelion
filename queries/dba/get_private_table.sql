-- :name get_private_table :one
select * from metadata.table
where is_private = true and id = :table_id
