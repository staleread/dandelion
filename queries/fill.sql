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
