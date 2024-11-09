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
    password varchar(60) not null,
    role_id integer not null,
    constraint fk_role foreign key (role_id) references role(id)
        on update cascade
        on delete restrict
);
