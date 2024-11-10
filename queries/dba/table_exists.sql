-- :name table_exists :one
select exists(
    select 1
    from metadata.table
    where title = :table_title
)
