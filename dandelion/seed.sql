insert into metadata.attribute 
    (table_id, name, ukr_name, data_type_id, is_unique, is_nullable, is_primary, constraint_pattern) 
select 
    t.id,
    a.name,
    a.ukr_name,
    dt.id,
    a.is_unique,
    a.is_nullable,
    a.is_primary,
    a.constraint_pattern
from metadata.table t
cross join (values
    // ... existing attributes ...
    ('schedule_shift', 'id', 'Ідентифікатор', 'serial', true, false, true, null),
    ('schedule_shift', 'day_of_week', 'День тижня', 'integer', false, false, false, '^[1-7]$'),
    ('schedule_shift', 'start_time', 'Час початку', 'time', false, false, false, null),
    ('schedule_shift', 'end_time', 'Час кінця', 'time', false, false, false, null),
    // ... remaining attributes ...
) as a(table_name, name, ukr_name, data_type_name, is_unique, is_nullable, is_primary, constraint_pattern) 