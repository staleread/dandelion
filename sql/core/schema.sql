-- Metadata tables
create schema if not exists metadata;

create table metadata.data_type (
    id serial primary key,
    name varchar(30) unique not null
);

create table metadata.fk_behavior (
    id serial primary key,
    name varchar(30) unique not null
);

create table metadata.table (
    id serial primary key,
    title varchar(64) unique not null,
    is_private boolean not null default false,
    is_protected boolean not null default false
);

create table metadata.attribute (
    id serial primary key,
    table_id integer not null,
    name varchar(30) not null,
    ukr_name varchar(30) not null,
    constraint_pattern varchar null,
    data_type_id integer not null,
    is_unique boolean not null default false,
    is_nullable boolean not null default false,
    is_primary boolean not null default false,
    constraint fk_table foreign key (table_id) references metadata.table(id)
        on update cascade
        on delete cascade,
    constraint fk_data_type foreign key (data_type_id) references metadata.data_type(id)
        on update cascade
        on delete restrict
);

create table metadata.foreign_key (
    id serial primary key,
    attribute_id integer not null,
    referenced_attribute_id integer not null,
    update_behavior_id integer not null,
    delete_behavior_id integer not null,
    constraint fk_attribute foreign key (attribute_id) references metadata.attribute(id)
        on update cascade
        on delete cascade,
    constraint fk_referenced_attribute foreign key (referenced_attribute_id) references metadata.attribute(id)
        on update cascade
        on delete cascade,
    constraint fk_update_behavior foreign key (update_behavior_id) references metadata.fk_behavior(id)
        on update cascade
        on delete restrict,
    constraint fk_delete_behavior foreign key (delete_behavior_id) references metadata.fk_behavior(id)
        on update cascade
        on delete restrict
); 

-- DBA tables
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

-- Trigger to handle cascade deletes when a table is dropped
create or replace function metadata.handle_table_drop()
returns event_trigger as $$
begin
    delete from metadata.table 
    where not exists (
        select 1 
        from information_schema.tables 
        where table_schema = 'public' 
        and table_name = metadata.table.title
    );
end;
$$ language plpgsql;

create event trigger handle_table_drop_trigger
on sql_drop
execute procedure metadata.handle_table_drop();