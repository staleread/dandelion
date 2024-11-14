-- Enum tables
insert into doctor_profile_type (name) values
    ('Терапевт'),
    ('Хірург'),
    ('Педіатр'),
    ('Невролог'),
    ('Кардіолог'),
    ('Офтальмолог');

insert into room_type (name) values
    ('Кабінет лікаря'),
    ('Процедурна'),
    ('Операційна'),
    ('Лабораторія');

insert into visit_status_type (name) values
    ('Заплановано'),
    ('В процесі'),
    ('Завершено'),
    ('Скасовано');

insert into vaccination_type (name) values
    ('БЦЖ'),
    ('Гепатит B'),
    ('АКДП'),
    ('Поліомієліт'),
    ('КПК');

-- Metadata tables
insert into metadata.table (title, is_private, is_protected) values
    ('patient', false, true),
    ('doctor_profile_type', false, true),
    ('doctor', false, true),
    ('room_type', false, true),
    ('room', false, true),
    ('schedule_shift', false, true),
    ('schedule_entry', false, true),
    ('medical_history', true, true),
    ('visit_status_type', false, true),
    ('visit', true, true),
    ('procedure', false, true),
    ('line_procedure', false, true),
    ('document_type', false, true),
    ('document', true, true),
    ('vaccination_type', false, true),
    ('vaccination', true, true);

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
    -- Patient attributes
    ('patient', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('patient', 'first_name', 'Ім''я', 'varchar', false, false, false),
    ('patient', 'last_name', 'Прізвище', 'varchar', false, false, false),
    ('patient', 'patronymic', 'По батькові', 'varchar', false, true, false),
    ('patient', 'birth_date', 'Дата народження', 'date', false, false, false),
    ('patient', 'address', 'Адреса', 'varchar', false, false, false),
    ('patient', 'phone', 'Телефон', 'varchar', false, true, false),
    -- Doctor profile type attributes
    ('doctor_profile_type', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('doctor_profile_type', 'name', 'Назва', 'varchar', true, false, false),
    -- Doctor attributes
    ('doctor', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('doctor', 'first_name', 'Ім''я', 'varchar', false, false, false),
    ('doctor', 'last_name', 'Прізвище', 'varchar', false, false, false),
    ('doctor', 'patronymic', 'По батькові', 'varchar', false, true, false),
    ('doctor', 'profile_id', 'Спеціальність', 'integer', false, false, false),
    ('doctor', 'phone', 'Телефон', 'varchar', false, true, false),
    -- Room type attributes
    ('room_type', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('room_type', 'name', 'Назва', 'varchar', true, false, false),
    -- Room attributes
    ('room', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('room', 'room_number', 'Номер кабінету', 'varchar', true, false, false),
    ('room', 'room_type_id', 'Тип кабінету', 'integer', false, true, false),
    -- Schedule shift attributes
    ('schedule_shift', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('schedule_shift', 'day_of_week', 'День тижня', 'integer', false, false, false),
    ('schedule_shift', 'start_time', 'Час початку', 'time', false, false, false),
    ('schedule_shift', 'end_time', 'Час кінця', 'time', false, false, false),
    -- Schedule entry attributes
    ('schedule_entry', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('schedule_entry', 'doctor_id', 'Лікар', 'integer', false, false, false),
    ('schedule_entry', 'room_id', 'Кабінет', 'integer', false, false, false),
    ('schedule_entry', 'shift_id', 'Зміна', 'integer', false, false, false),
    -- Medical history attributes
    ('medical_history', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('medical_history', 'patient_id', 'Пацієнт', 'integer', true, false, false),
    ('medical_history', 'therapist_id', 'Сімейний лікар', 'integer', false, true, false),
    -- Visit attributes
    ('visit', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('visit', 'medical_history_id', 'Медична карта', 'integer', false, false, false),
    ('visit', 'doctor_id', 'Лікар', 'integer', false, false, false),
    ('visit', 'visit_date', 'Дата візиту', 'date', false, false, false),
    ('visit', 'start_time', 'Час початку', 'time', false, false, false),
    ('visit', 'end_time', 'Час кінця', 'time', false, false, false),
    ('visit', 'diagnosis', 'Діагноз', 'varchar', false, true, false),
    ('visit', 'status_id', 'Статус', 'integer', false, false, false),
    ('visit', 'home_visit_address', 'Адреса виклику', 'varchar', false, true, false),
    -- Procedure attributes
    ('procedure', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('procedure', 'name', 'Назва', 'varchar', true, false, false),
    ('procedure', 'description', 'Опис', 'text', false, true, false),
    -- Line procedure attributes
    ('line_procedure', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('line_procedure', 'visit_id', 'Візит', 'integer', false, false, false),
    ('line_procedure', 'procedure_id', 'Процедура', 'integer', false, false, false),
    ('line_procedure', 'room_id', 'Кабінет', 'integer', false, true, false),
    -- Document type attributes
    ('document_type', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('document_type', 'name', 'Назва', 'varchar', true, false, false),
    ('document_type', 'description', 'Опис', 'text', false, true, false),
    ('document_type', 'template', 'Шаблон', 'json', false, false, false),
    -- Document attributes
    ('document', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('document', 'visit_id', 'Візит', 'integer', false, false, false),
    ('document', 'document_type_id', 'Тип документу', 'integer', false, false, false),
    ('document', 'data', 'Дані', 'json', false, false, false),
    -- Vaccination type attributes
    ('vaccination_type', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('vaccination_type', 'name', 'Назва', 'varchar', true, false, false),
    -- Vaccination attributes
    ('vaccination', 'id', 'Ідентифікатор', 'serial', true, false, true),
    ('vaccination', 'doctor_id', 'Лікар', 'integer', false, false, false),
    ('vaccination', 'medical_history_id', 'Медична карта', 'integer', false, false, false),
    ('vaccination', 'vaccination_type_id', 'Тип вакцинації', 'integer', false, false, false),
    ('vaccination', 'completed_date', 'Дата виконання', 'timestamp', false, true, false),
    ('vaccination', 'accept_since', 'Дійсно з', 'date', false, false, false),
    ('vaccination', 'accept_until', 'Дійсно по', 'date', false, false, false)
) as a(table_name, name, ukr_name, data_type_name, is_unique, is_nullable, is_primary)
join metadata.data_type dt on dt.name = a.data_type_name
where t.title = a.table_name;

-- Constraints
update metadata.attribute 
set constraint_pattern = 'between 1 and 7' 
where table_id = (select id from metadata.table where title = 'schedule_shift')
    and name = 'day_of_week';

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
    -- Doctor foreign keys
    (t.title = 'doctor' and a.name = 'profile_id' and rt.title = 'doctor_profile_type'
        and ub.name = 'cascade' and db.name = 'restrict')
    
    -- Room foreign keys
    or (t.title = 'room' and a.name = 'room_type_id' and rt.title = 'room_type'
        and ub.name = 'cascade' and db.name = 'set null')
    
    -- Schedule entry foreign keys
    or (t.title = 'schedule_entry' and a.name = 'doctor_id' and rt.title = 'doctor'
        and ub.name = 'cascade' and db.name = 'set null')
    or (t.title = 'schedule_entry' and a.name = 'room_id' and rt.title = 'room'
        and ub.name = 'cascade' and db.name = 'set null')
    or (t.title = 'schedule_entry' and a.name = 'shift_id' and rt.title = 'schedule_shift'
        and ub.name = 'cascade' and db.name = 'restrict')
    
    -- Medical history foreign keys
    or (t.title = 'medical_history' and a.name = 'patient_id' and rt.title = 'patient'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'medical_history' and a.name = 'therapist_id' and rt.title = 'doctor'
        and ub.name = 'cascade' and db.name = 'set null')
    
    -- Visit foreign keys
    or (t.title = 'visit' and a.name = 'medical_history_id' and rt.title = 'medical_history'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'visit' and a.name = 'doctor_id' and rt.title = 'doctor'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'visit' and a.name = 'status_id' and rt.title = 'visit_status_type'
        and ub.name = 'cascade' and db.name = 'restrict')

    -- Line procedure foreign keys
    or (t.title = 'line_procedure' and a.name = 'visit_id' and rt.title = 'visit'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'line_procedure' and a.name = 'procedure_id' and rt.title = 'procedure'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'line_procedure' and a.name = 'room_id' and rt.title = 'room'
        and ub.name = 'cascade' and db.name = 'restrict')

    -- Document foreign keys
    or (t.title = 'document' and a.name = 'visit_id' and rt.title = 'visit'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'document' and a.name = 'document_type_id' and rt.title = 'document_type'
        and ub.name = 'cascade' and db.name = 'restrict')

    -- Vaccination foreign keys
    or (t.title = 'vaccination' and a.name = 'doctor_id' and rt.title = 'doctor'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'vaccination' and a.name = 'medical_history_id' and rt.title = 'medical_history'
        and ub.name = 'cascade' and db.name = 'restrict')
    or (t.title = 'vaccination' and a.name = 'vaccination_type_id' and rt.title = 'vaccination_type'
        and ub.name = 'cascade' and db.name = 'restrict');