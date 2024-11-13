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
    title varchar(30) unique not null,
    is_private boolean not null default false,
    is_protected boolean not null default false
);

create table metadata.attribute (
    id serial primary key,
    table_id integer not null,
    name varchar(30) not null,
    ukr_name varchar(30) not null,
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

-- Template used to create new tables
create table metadata.template (
    id serial primary key
);

insert into metadata.data_type (name) values
    ('integer'),
    ('varchar'),
    ('date'),
    ('text'),
    ('serial'),
    ('timestamp'),
    ('boolean');

insert into metadata.fk_behavior (name) values
    ('cascade'),
    ('restrict'),
    ('set null'),
    ('set default'),
    ('no action');

