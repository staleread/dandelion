-- :name get_role_permissions :many
select p.name from "role" r
join "role_permission" rp on rp."role_id" = r.id
join "permission" p on p.id = rp."permission_id"
where r.id = :role_id
