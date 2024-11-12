create table role (
    id serial primary key,
    name varchar unique not null
);

create table permission (
    id serial primary key,
    name varchar unique not null
);

create table role_permission (
    role_id integer not null,
    permission_id integer not null,
    constraint fk_role foreign key (role_id) references role(id)
        on update cascade
        on delete cascade,
    constraint fk_permission foreign key (permission_id) references permission(id)
        on update cascade
        on delete cascade,
    primary key (role_id, permission_id)
);

create table "user" (
    id serial primary key,
    username varchar unique not null,
    hashed_password varchar not null,
    role_id integer not null,
    constraint fk_role foreign key (role_id) references role(id)
        on update cascade
        on delete restrict
);

-- Populate roles
insert into role (name) values
    ('guest'),
    ('operator'),
    ('admin'),
    ('owner');

-- Populate permissions
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

-- Set up role permissions
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

-- Create domain tables
create table doctor (
    id serial primary key,
    first_name varchar not null,
    last_name varchar not null,
    patronymic varchar,
    profile varchar not null,
    phone varchar not null
);

create table room_type (
    id serial primary key,
    name varchar not null unique
);

insert into room_type (name) values
    ('general'),
    ('physiotherapy');

create table room (
    id serial primary key,
    room_number varchar not null unique,
    room_type_id integer not null,
    constraint fk_room_type foreign key (room_type_id) references room_type(id)
        on update cascade
        on delete restrict
);

create table schedule (
    id serial primary key,
    doctor_id integer not null,
    room_id integer not null,
    day_of_week integer not null check (day_of_week between 1 and 7),
    shift integer not null check (shift in (1, 2)),
    start_hour time not null,
    end_hour time not null,
    constraint fk_doctor foreign key (doctor_id) references doctor(id),
    constraint fk_room foreign key (room_id) references room(id)
);

create table patient (
    id serial primary key,
    first_name varchar not null,
    last_name varchar not null,
    patronymic varchar,
    birth_date date not null,
    address varchar not null,
    phone varchar not null,
    health_status varchar not null,
    district_doctor_id integer,
    constraint fk_district_doctor foreign key (district_doctor_id) references doctor(id)
);

create table procedure_type (
    id serial primary key,
    name varchar not null,
    description text
);

create table visit (
    id serial primary key,
    patient_id integer not null,
    doctor_id integer not null,
    visit_date timestamp not null,
    diagnosis varchar,
    is_home_visit boolean not null default false,
    visit_address varchar,
    constraint fk_patient foreign key (patient_id) references patient(id),
    constraint fk_doctor foreign key (doctor_id) references doctor(id)
);

create table procedure (
    id serial primary key,
    visit_id integer not null,
    procedure_type_id integer not null,
    scheduled_date timestamp not null,
    completed_date timestamp,
    room_id integer not null,
    constraint fk_visit foreign key (visit_id) references visit(id),
    constraint fk_procedure_type foreign key (procedure_type_id) references procedure_type(id),
    constraint fk_room foreign key (room_id) references room(id)
);

create table certificate_template (
    id serial primary key,
    name varchar not null,
    template text not null
);

create table certificate (
    id serial primary key,
    patient_id integer not null,
    doctor_id integer not null,
    template_id integer not null,
    issue_date timestamp not null,
    data jsonb not null,
    constraint fk_patient foreign key (patient_id) references patient(id),
    constraint fk_doctor foreign key (doctor_id) references doctor(id),
    constraint fk_template foreign key (template_id) references certificate_template(id)
);

-- Add metadata for Ukrainian translations
insert into metadata.table (title, is_private, is_protected) values
    ('role', false, true),
    ('permission', false, true),
    ('role_permission', false, true),
    ('user', true, true),
    ('doctor', false, true),
    ('room_type', false, true),
    ('room', false, true),
    ('schedule', false, true),
    ('patient', false, true),
    ('procedure_type', false, true),
    ('visit', false, true),
    ('procedure', false, true),
    ('certificate_template', false, true),
    ('certificate', false, true);

-- Add metadata for all tables
-- Role table (id = 1)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (1, 'id', 'ID', 5, true, false, true),
    (1, 'name', 'Назва ролі', 2, true, false, false);

-- Permission table (id = 2)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (2, 'id', 'ID', 5, true, false, true),
    (2, 'name', 'Назва дозволу', 2, true, false, false);

-- Role_permission table (id = 3)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (3, 'role_id', 'ID ролі', 1, false, false, true),
    (3, 'permission_id', 'ID дозволу', 1, false, false, true);

-- User table (id = 4)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (4, 'id', 'ID', 5, true, false, true),
    (4, 'username', 'Ім''я користувача', 2, true, false, false),
    (4, 'hashed_password', 'Хешований пароль', 2, false, false, false),
    (4, 'role_id', 'ID ролі', 1, false, false, false);

-- Doctor table (id = 5)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (5, 'id', 'ID', 5, true, false, true),
    (5, 'first_name', 'Ім''я', 2, false, false, false),
    (5, 'last_name', 'Прізвище', 2, false, false, false),
    (5, 'patronymic', 'По батькові', 2, false, true, false),
    (5, 'profile', 'Спеціалізація', 2, false, false, false),
    (5, 'phone', 'Телефон', 2, false, false, false);

-- Room_type table (id = 6)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (6, 'id', 'ID', 5, true, false, true),
    (6, 'name', 'Тип кабінету', 2, true, false, false);

-- Room table (id = 7)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (7, 'id', 'ID', 5, true, false, true),
    (7, 'room_number', 'Номер кабінету', 2, true, false, false),
    (7, 'room_type_id', 'Тип кабінету', 1, false, false, false);

-- Schedule table (id = 8)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (8, 'id', 'ID', 5, true, false, true),
    (8, 'doctor_id', 'ID лікаря', 1, false, false, false),
    (8, 'room_id', 'ID кабінету', 1, false, false, false),
    (8, 'day_of_week', 'День тижня', 1, false, false, false),
    (8, 'shift', 'Зміна', 1, false, false, false),
    (8, 'start_hour', 'Час початку', 6, false, false, false),
    (8, 'end_hour', 'Час кінця', 6, false, false, false);

-- Patient table (id = 9)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (9, 'id', 'ID', 5, true, false, true),
    (9, 'first_name', 'Ім''я', 2, false, false, false),
    (9, 'last_name', 'Прізвище', 2, false, false, false),
    (9, 'patronymic', 'По батькові', 2, false, true, false),
    (9, 'birth_date', 'Дата народження', 3, false, false, false),
    (9, 'address', 'Адреса', 2, false, false, false),
    (9, 'phone', 'Телефон', 2, false, false, false),
    (9, 'health_status', 'Стан здоров''я', 2, false, false, false),
    (9, 'district_doctor_id', 'ID дільничного лікаря', 1, false, true, false);

-- Procedure_type table (id = 10)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (10, 'id', 'ID', 5, true, false, true),
    (10, 'name', 'Назва процедури', 2, false, false, false),
    (10, 'description', 'Опис', 4, false, true, false);

-- Visit table (id = 11)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (11, 'id', 'ID', 5, true, false, true),
    (11, 'patient_id', 'ID пацієнта', 1, false, false, false),
    (11, 'doctor_id', 'ID лікаря', 1, false, false, false),
    (11, 'visit_date', 'Дата візиту', 6, false, false, false),
    (11, 'diagnosis', 'Діагноз', 2, false, true, false),
    (11, 'is_home_visit', 'Візит додому', 2, false, false, false),
    (11, 'visit_address', 'Адреса візиту', 2, false, true, false);

-- Procedure table (id = 12)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (12, 'id', 'ID', 5, true, false, true),
    (12, 'visit_id', 'ID візиту', 1, false, false, false),
    (12, 'procedure_type_id', 'ID типу процедури', 1, false, false, false),
    (12, 'scheduled_date', 'Запланована дата', 6, false, false, false),
    (12, 'completed_date', 'Дата виконання', 6, false, true, false),
    (12, 'room_id', 'ID кабінету', 1, false, false, false);

-- Certificate_template table (id = 13)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (13, 'id', 'ID', 5, true, false, true),
    (13, 'name', 'Назва шаблону', 2, true, false, false);

-- Certificate table (id = 14)
insert into metadata.attribute (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary) values
    (14, 'id', 'ID', 5, true, false, true),
    (14, 'patient_id', 'ID пацієнта', 1, false, false, false),
    (14, 'doctor_id', 'ID лікаря', 1, false, false, false),
    (14, 'template_id', 'ID шаблону', 1, false, false, false),
    (14, 'issue_date', 'Дата видачі', 6, false, false, false),
    (14, 'data', 'Дані', 2, false, false, false);

-- Add foreign key metadata relationships
insert into metadata.foreign_key (attribute_id, referenced_attribute_id, update_behavior_id, delete_behavior_id)
select 
    fk.attribute_id,
    fk.referenced_attribute_id,
    ub.id as update_behavior_id,
    db.id as delete_behavior_id
from (
    -- role_permission -> role
    values 
        ((select id from metadata.attribute where table_id = 3 and name = 'role_id'),
         (select id from metadata.attribute where table_id = 1 and name = 'id'),
         'cascade', 'cascade'),
        
    -- role_permission -> permission
        ((select id from metadata.attribute where table_id = 3 and name = 'permission_id'),
         (select id from metadata.attribute where table_id = 2 and name = 'id'),
         'cascade', 'cascade'),

    -- user -> role
        ((select id from metadata.attribute where table_id = 4 and name = 'role_id'),
         (select id from metadata.attribute where table_id = 1 and name = 'id'),
         'cascade', 'restrict'),

    -- schedule -> doctor
        ((select id from metadata.attribute where table_id = 8 and name = 'doctor_id'),
         (select id from metadata.attribute where table_id = 5 and name = 'id'),
         'cascade', 'restrict'),

    -- schedule -> room
        ((select id from metadata.attribute where table_id = 8 and name = 'room_id'),
         (select id from metadata.attribute where table_id = 7 and name = 'id'),
         'cascade', 'restrict'),

    -- patient -> doctor (district_doctor)
        ((select id from metadata.attribute where table_id = 9 and name = 'district_doctor_id'),
         (select id from metadata.attribute where table_id = 5 and name = 'id'),
         'cascade', 'restrict'),

    -- visit -> patient
        ((select id from metadata.attribute where table_id = 11 and name = 'patient_id'),
         (select id from metadata.attribute where table_id = 9 and name = 'id'),
         'cascade', 'restrict'),

    -- visit -> doctor
        ((select id from metadata.attribute where table_id = 11 and name = 'doctor_id'),
         (select id from metadata.attribute where table_id = 5 and name = 'id'),
         'cascade', 'restrict'),

    -- procedure -> visit
        ((select id from metadata.attribute where table_id = 12 and name = 'visit_id'),
         (select id from metadata.attribute where table_id = 11 and name = 'id'),
         'cascade', 'restrict'),

    -- procedure -> procedure_type
        ((select id from metadata.attribute where table_id = 12 and name = 'procedure_type_id'),
         (select id from metadata.attribute where table_id = 10 and name = 'id'),
         'cascade', 'restrict'),

    -- procedure -> room
        ((select id from metadata.attribute where table_id = 12 and name = 'room_id'),
         (select id from metadata.attribute where table_id = 7 and name = 'id'),
         'cascade', 'restrict'),

    -- certificate -> patient
        ((select id from metadata.attribute where table_id = 14 and name = 'patient_id'),
         (select id from metadata.attribute where table_id = 9 and name = 'id'),
         'cascade', 'restrict'),

    -- certificate -> doctor
        ((select id from metadata.attribute where table_id = 14 and name = 'doctor_id'),
         (select id from metadata.attribute where table_id = 5 and name = 'id'),
         'cascade', 'restrict'),

    -- certificate -> certificate_template
        ((select id from metadata.attribute where table_id = 14 and name = 'template_id'),
         (select id from metadata.attribute where table_id = 13 and name = 'id'),
         'cascade', 'restrict'),

    -- room -> room_type
        ((select id from metadata.attribute where table_id = 7 and name = 'room_type_id'),
         (select id from metadata.attribute where table_id = (select id from metadata.table where title = 'room_type') and name = 'id'),
         'cascade', 'restrict')

) as fk(attribute_id, referenced_attribute_id, update_behavior, delete_behavior)
cross join metadata.fk_behavior ub
cross join metadata.fk_behavior db
where ub.name = fk.update_behavior
and db.name = fk.delete_behavior;
