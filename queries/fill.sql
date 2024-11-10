insert into role (name) values ('guest');
insert into role (name) values ('operator');
insert into role (name) values ('admin');
insert into role (name) values ('owner');

insert into permission (name) values ('can_connect');
insert into permission (name) values ('can_read_public');
insert into permission (name) values ('can_modify_records');
insert into permission (name) values ('can_modify_attributes');
insert into permission (name) values ('can_add_user');
insert into permission (name) values ('can_add_operator');
insert into permission (name) values ('can_read_private');
insert into permission (name) values ('can_modify_tables');
insert into permission (name) values ('can_add_admin');

-- guest permissions
insert into role_permission (role_id, permission_id)
select r.id, p.id
from role r
join permission p on p.name in
  ('can_connect', 'can_read_public')
where r.name = 'guest';

-- operator permissions
insert into role_permission (role_id, permission_id)
select r.id, p.id
from role r
join permission p on p.name in ('can_connect', 'can_read_public', 'can_modify_records')
where r.name = 'operator';

-- admin permissions
insert into role_permission (role_id, permission_id)
select r.id, p.id
from role r
join permission p on p.name in ('can_connect', 'can_read_public', 'can_modify_records', 'can_modify_attributes', 'can_add_user', 'can_add_operator')
where r.name = 'admin';

-- owner permissions
insert into role_permission (role_id, permission_id)
select r.id, p.id
from role r
join permission p on p.name in ('can_connect', 'can_read_public', 'can_modify_records', 'can_modify_attributes', 'can_add_user', 'can_add_operator', 'can_read_private', 'can_modify_tables', 'can_add_admin')
where r.name = 'owner';

insert into metadata.table (title, is_private, is_protected) values 
    ('user', true, true),
    ('role', false, true),
    ('permission', false, true);

insert into metadata.attribute (table_id, name, ukr_name, type, is_primary) values 
    (1, 'id', 'ідентифікатор', 'serial', true),
    (1, 'username', 'ім''я користувача', 'varchar(30)', false),
    (1, 'hashed_password', 'хешований пароль', 'varchar(72)', false),
    (1, 'role_id', 'ідентифікатор ролі', 'integer', false),
    (2, 'id', 'ідентифікатор', 'serial', true),
    (2, 'name', 'назва', 'varchar(30)', false),
    (3, 'id', 'ідентифікатор', 'serial', true),
    (3, 'name', 'назва', 'varchar(50)', false);

update metadata.attribute set name = 'hashed_password' where name = 'password';
update metadata.attribute set ukr_name = 'хешований пароль' where name = 'hashed_password';

insert into metadata.table (title, is_private, is_protected) values 
    ('role_permission', false, true);

insert into metadata.attribute (table_id, name, ukr_name, type, is_primary) values 
    (4, 'role_id', 'ідентифікатор ролі', 'integer', true),
    (4, 'permission_id', 'ідентифікатор дозволу', 'integer', true);