-- :name permissions_by_role :many
select p.name
from permission p
join role_permission rp on p.id = rp.permission_id
join role r on rp.role_id = r.id
where r.id = :role_id;
