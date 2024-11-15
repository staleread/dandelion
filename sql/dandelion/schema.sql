create table patient (
    id serial primary key,
    first_name varchar not null,
    last_name varchar not null,
    patronymic varchar null,
    birth_date date not null,
    address varchar not null,
    phone varchar null
);

create table doctor_profile_type (
    id serial primary key,
    name varchar not null unique
);

create table doctor (
    id serial primary key,
    first_name varchar not null,
    last_name varchar not null,
    patronymic varchar null,
    profile_id integer not null,
    phone varchar null,
    constraint fk_profile foreign key (profile_id) references doctor_profile_type(id)
        on update cascade
        on delete restrict
);

create table room_type (
    id serial primary key,
    name varchar not null unique
);

create table room (
    id serial primary key,
    room_number varchar not null unique,
    room_type_id integer not null,
    constraint fk_room_type foreign key (room_type_id) references room_type(id)
        on update cascade
        on delete set null
);

create table schedule_shift (
    id serial primary key,
    day_of_week integer not null check (day_of_week between 1 and 7),
    start_time time not null,
    end_time time not null
);

create table schedule_entry (
    id serial primary key,
    doctor_id integer not null,
    room_id integer not null,
    shift_id integer not null,
    constraint fk_doctor foreign key (doctor_id) references doctor(id)
        on update cascade
        on delete set null,
    constraint fk_room foreign key (room_id) references room(id)
        on update cascade
        on delete set null,
    constraint fk_shift foreign key (shift_id) references schedule_shift(id)
        on update cascade
        on delete restrict
);

create table medical_history (
    id serial primary key,
    patient_id integer not null unique,
    therapist_id integer,
    constraint fk_patient foreign key (patient_id) references patient(id)
        on update cascade
        on delete restrict,
    constraint fk_therapist foreign key (therapist_id) references doctor(id)
        on update cascade
        on delete set null
);

create table visit_status_type (
    id serial primary key,
    name varchar not null unique
);

create table visit (
    id serial primary key,
    medical_history_id integer not null,
    doctor_id integer not null,
    visit_date date not null,
    start_time time not null,
    end_time time not null,
    diagnosis varchar null,
    status_id integer not null,
    home_visit_address varchar null,
    constraint fk_medical_history foreign key (medical_history_id) references medical_history(id)
        on update cascade
        on delete restrict,
    constraint fk_doctor foreign key (doctor_id) references doctor(id)
        on update cascade
        on delete restrict,
    constraint fk_status foreign key (status_id) references visit_status_type(id)
        on update cascade
        on delete restrict
);

create table procedure (
    id serial primary key,
    name varchar not null unique,
    description text null
);

create table line_procedure (
    id serial primary key,
    visit_id integer not null,
    procedure_id integer not null,
    room_id integer null,
    constraint fk_visit foreign key (visit_id) references visit(id)
        on update cascade
        on delete restrict,
    constraint fk_procedure foreign key (procedure_id) references procedure(id)
        on update cascade
        on delete restrict,
    constraint fk_room foreign key (room_id) references room(id)
        on update cascade
        on delete restrict
);

create table document_type (
    id serial primary key,
    name varchar not null unique,
    description text null,
    template json not null
);

create table document (
    id serial primary key,
    visit_id integer not null,
    document_type_id integer not null,
    data json not null,
    constraint fk_visit foreign key (visit_id) references visit(id)
        on update cascade
        on delete restrict,
    constraint fk_document_type foreign key (document_type_id) references document_type(id)
        on update cascade
        on delete restrict
);

create table vaccination_type (
    id serial primary key,
    name varchar not null unique
);

create table vaccination (
    id serial primary key,
    doctor_id integer not null,
    medical_history_id integer not null,
    vaccination_type_id integer not null,
    completed_date timestamp null,
    accept_since date not null,
    accept_until date not null,
    constraint fk_medical_history foreign key (medical_history_id) references medical_history(id)
        on update cascade
        on delete restrict,
    constraint fk_vaccination_type foreign key (vaccination_type_id) references vaccination_type(id)
        on update cascade
        on delete restrict,
    constraint fk_doctor foreign key (doctor_id) references doctor(id)
        on update cascade
        on delete restrict
); 
