from fastapi import APIRouter

from app.common.template.utils import TemplateContextDep
from app.common.database.utils import QueryRunnerDep

router = APIRouter(prefix="/query")


@router.get("/therapists_schedule")
async def get_therapists_schedule(sql: QueryRunnerDep, template: TemplateContextDep):
    schedules = sql.query("""
        SELECT 
            CASE schedule_shift.day_of_week 
                WHEN 1 THEN 'Понеділок'
                WHEN 2 THEN 'Вівторок'
                WHEN 3 THEN 'Середа'
                WHEN 4 THEN 'Четвер'
                WHEN 5 THEN 'П''ятниця'
                WHEN 6 THEN 'Субота'
                WHEN 7 THEN 'Неділя'
            END AS day_of_week,
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS doctor_name,
            to_char(schedule_shift.start_time, 'HH24:MI') as start_hour,
            to_char(schedule_shift.end_time, 'HH24:MI') as end_hour,
            room.room_number,
            room_type.name as room_type_name
        FROM schedule_entry
        JOIN doctor ON schedule_entry.doctor_id = doctor.id
        JOIN schedule_shift ON schedule_entry.shift_id = schedule_shift.id
        JOIN room ON schedule_entry.room_id = room.id
        JOIN room_type ON room.room_type_id = room_type.id
        JOIN doctor_profile_type ON doctor.profile_id = doctor_profile_type.id
        WHERE doctor_profile_type.name = 'Терапевт'
        ORDER BY schedule_shift.day_of_week, schedule_shift.start_time;
    """).many_rows()

    return template("/classic/query/therapists_schedule.html", {"schedules": schedules})
