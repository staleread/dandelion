create table role (
    id serial primary key,
    name varchar(30) unique not null
);

create table permission (
    id serial primary key,
    name varchar(50) unique not null
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
    username varchar(30) unique not null,
    hashed_password varchar(72) not null,
    role_id integer not null,
    constraint fk_role foreign key (role_id) references role(id)
        on update cascade
        on delete restrict
);

-- metadata schema
create schema if not exists metadata;

create table metadata.table (
    id serial primary key,
    title varchar(30) unique not null,
    is_private boolean not null default false,
    is_protected boolean not null default false
);

create table metadata.attribute (
    id serial primary key,
    table_id integer not null,
    name varchar(30) not null,
    ukr_name varchar(30) not null,
    type varchar(30) not null,
    is_primary boolean not null default false,
    constraint fk_table foreign key (table_id) references metadata.table(id)
        on update cascade
        on delete cascade
);