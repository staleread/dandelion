-- :name get_table_attributes :many
select * from metadata.attribute
where table_id = :table_id
