-- Metadata tables
insert into metadata.data_type (name) values
    ('integer'),
    ('varchar'),
    ('date'),
    ('text'),
    ('serial'),
    ('time'),
    ('timestamp'),
    ('boolean');

insert into metadata.fk_behavior (name) values
    ('cascade'),
    ('restrict'),
    ('set null'),
    ('set default'),
    ('no action');

-- DBA tables
insert into role (name) values
    ('guest'),
    ('operator'),
    ('admin'),
    ('owner');

insert into permission (name) values
    ('can_connect'),
    ('can_read_public'),
    ('can_modify_records'),
    ('can_modify_attributes'),
    ('can_add_user'),
    ('can_add_operator'),
    ('can_read_private'),
    ('can_modify_tables'),
    ('can_add_admin');

insert into role_permission (role_id, permission_id) 
select r.id, p.id
from role r, permission p
where 
    (r.name = 'guest' and p.name in ('can_connect', 'can_read_public'))
    or (r.name = 'operator' and p.name in ('can_connect', 'can_read_public', 'can_modify_records'))
    or (r.name = 'admin' and p.name in ('can_connect', 'can_read_public', 'can_modify_records', 
        'can_modify_attributes', 'can_add_user', 'can_add_operator'))
    OR (r.name = 'owner' AND p.name IN ('can_connect', 'can_read_public', 'can_modify_records',
        'can_modify_attributes', 'can_add_user', 'can_add_operator', 'can_read_private',
        'can_modify_tables', 'can_add_admin'));

insert into metadata.table (title, is_private, is_protected) values
    ('role', true, true),
    ('permission', true, true),
    ('role_permission', true, true),
    ('user', true, true);

insert into metadata.attribute 
    (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) 
select 
    t.id,
    a.name,
    a.ukr_name,
    dt.id,
    a.is_unique,
    a.is_nullable,
    a.is_primary
from metadata.table t
cross join (values
    -- Role attributes
    ('role', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('role', 'name', 'Назва', 'varchar', true, false, false),
    -- Permission attributes
    ('permission', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('permission', 'name', 'Назва', 'varchar', true, false, false),
    -- Role permission attributes
    ('role_permission', 'role_id', 'Роль', 'integer', false, false, true),
    ('role_permission', 'permission_id', 'Дозвіл', 'integer', false, false, true),
    -- User attributes
    ('user', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('user', 'username', 'Логін', 'varchar', true, false, false),
    ('user', 'hashed_password', 'Пароль', 'varchar', false, false, false),
    ('user', 'role_id', 'Роль', 'integer', false, false, false)
) as a(table_name, name, ukr_name, data_type_name, is_unique, is_nullable, is_primary)
join metadata.data_type dt on dt.name = a.data_type_name
where t.title = a.table_name;

-- Foreign keys
insert into metadata.foreign_key 
    (attribute_id, referenced_attribute_id, update_behavior_id, delete_behavior_id)
select 
    a.id as attribute_id,
    ra.id as referenced_attribute_id,
    ub.id as update_behavior_id,
    db.id as delete_behavior_id
from metadata.attribute a
join metadata.table t on t.id = a.table_id
join metadata.attribute ra on ra.is_primary
join metadata.table rt on rt.id = ra.table_id
cross join metadata.fk_behavior ub
cross join metadata.fk_behavior db
where 
    -- Role permission foreign keys
    (t.title = 'role_permission' and a.name = 'role_id' and rt.title = 'role'
        and ub.name = 'cascade' and db.name = 'cascade')
    or (t.title = 'role_permission' and a.name = 'permission_id' and rt.title = 'permission'
        and ub.name = 'cascade' and db.name = 'cascade')
    
    -- User foreign keys
    or (t.title = 'user' and a.name = 'role_id' and rt.title = 'role'
        and ub.name = 'cascade' and db.name = 'restrict');