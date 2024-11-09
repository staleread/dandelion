-- :name user_by_username :one
select id, username, password, role_id
from "user"
where username = :username;
