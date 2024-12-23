from app.common.database.utils import SqlQueryRunner


def get_therapists_schedule(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
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


def get_all_patients(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT 
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            medical_history.id as history_id,
            COALESCE(
                (SELECT diagnosis 
                FROM visit 
                WHERE medical_history_id = medical_history.id 
                ORDER BY visit_date DESC, start_time DESC 
                LIMIT 1),
                'Здоровий'
            ) as health_state,
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS therapist_name
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        LEFT JOIN doctor ON medical_history.therapist_id = doctor.id
        ORDER BY patient.last_name, patient.first_name
    """).many_rows()


def search_patients_by_last_name(sql: SqlQueryRunner, last_name: str) -> list[dict]:
    return (
        sql.query("""
        SELECT 
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            medical_history.id as history_id,
            COALESCE(
                (SELECT diagnosis 
                FROM visit 
                WHERE medical_history_id = medical_history.id 
                ORDER BY visit_date DESC, start_time DESC 
                LIMIT 1),
                'Здоровий'
            ) as health_state,
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS therapist_name
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        LEFT JOIN doctor ON medical_history.therapist_id = doctor.id
        WHERE LOWER(patient.last_name) LIKE LOWER(:search_param)
        ORDER BY patient.last_name, patient.first_name
    """)
        .bind(search_param=f"%{last_name}%")
        .many_rows()
    )


def search_patients_by_history_id(sql: SqlQueryRunner, history_id: str) -> list[dict]:
    return (
        sql.query("""
        SELECT 
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            medical_history.id as history_id,
            COALESCE(
                (SELECT diagnosis 
                FROM visit 
                WHERE medical_history_id = medical_history.id 
                ORDER BY visit_date DESC, start_time DESC 
                LIMIT 1),
                'Здоровий'
            ) as health_state,
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS therapist_name
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        LEFT JOIN doctor ON medical_history.therapist_id = doctor.id
        WHERE medical_history.id::text LIKE :search_param
        ORDER BY patient.last_name, patient.first_name
    """)
        .bind(search_param=f"%{history_id}%")
        .many_rows()
    )


def search_patients_by_health(sql: SqlQueryRunner, health_query: str) -> list[dict]:
    return (
        sql.query("""
        SELECT 
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            medical_history.id as history_id,
            COALESCE(
                (SELECT diagnosis 
                FROM visit 
                WHERE medical_history_id = medical_history.id 
                ORDER BY visit_date DESC, start_time DESC 
                LIMIT 1),
                'Здоровий'
            ) as health_state,
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS therapist_name
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        LEFT JOIN doctor ON medical_history.therapist_id = doctor.id
        WHERE LOWER(COALESCE(
            (SELECT diagnosis 
            FROM visit 
            WHERE medical_history_id = medical_history.id 
            ORDER BY visit_date DESC, start_time DESC 
            LIMIT 1),
            'Здоровий'
        )) LIKE LOWER(:search_param)
        ORDER BY patient.last_name, patient.first_name
    """)
        .bind(search_param=f"%{health_query}%")
        .many_rows()
    )


def search_patients_by_therapist(
    sql: SqlQueryRunner, therapist_name: str
) -> list[dict]:
    return (
        sql.query("""
        SELECT 
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            medical_history.id as history_id,
            COALESCE(
                (SELECT diagnosis 
                FROM visit 
                WHERE medical_history_id = medical_history.id 
                ORDER BY visit_date DESC, start_time DESC 
                LIMIT 1),
                'Здоровий'
            ) as health_state,
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS therapist_name
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        LEFT JOIN doctor ON medical_history.therapist_id = doctor.id
        WHERE LOWER(doctor.last_name) LIKE LOWER(:search_param)
        ORDER BY patient.last_name, patient.first_name
    """)
        .bind(search_param=f"%{therapist_name}%")
        .many_rows()
    )


def get_patients_with_multiple_doctors(sql: SqlQueryRunner) -> list[dict]:
    """Get patients who visited more than 2 doctors in the last 7 days."""
    return sql.query("""
        SELECT 
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            COUNT(DISTINCT visit.doctor_id) as doctors_count
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        JOIN visit ON medical_history.id = visit.medical_history_id
        WHERE visit.visit_date >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY patient.id, patient.last_name, patient.first_name, patient.patronymic
        HAVING COUNT(DISTINCT visit.doctor_id) > 2
        ORDER BY doctors_count DESC, patient.last_name
    """).many_rows()


def get_angina_patients_count(sql: SqlQueryRunner) -> int:
    """Get count of patients diagnosed with angina in the last 30 days."""
    result = sql.query("""
        SELECT COUNT(DISTINCT medical_history.patient_id) as patients_count
        FROM visit
        JOIN medical_history ON visit.medical_history_id = medical_history.id
        WHERE 
            visit.visit_date >= CURRENT_DATE - INTERVAL '30 days'
            AND LOWER(visit.diagnosis) LIKE '%ангіна%'
    """).one_row()
    return int(result["patients_count"])


def get_doctors_for_dropdown(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT 
            doctor.id,
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS doctor_name
        FROM doctor
        ORDER BY doctor.last_name, doctor.first_name
    """).many_rows()


def get_doctor_schedule(
    sql: SqlQueryRunner, doctor_id: int | None, days_ahead: int
) -> list[dict]:
    if not doctor_id:
        return []

    return (
        sql.query("""
        WITH RECURSIVE dates AS (
            SELECT CURRENT_DATE as date
            UNION ALL
            SELECT date + 1
            FROM dates
            WHERE date < CURRENT_DATE + :days_interval
        )
        SELECT 
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS doctor_name,
            to_char(dates.date, 'DD.MM.YYYY') as shift_date,
            CASE EXTRACT(DOW FROM dates.date)
                WHEN 0 THEN 7
                ELSE EXTRACT(DOW FROM dates.date)
            END as day_of_week,
            room.room_number,
            to_char(schedule_shift.start_time, 'HH24:MI') as start_hour,
            to_char(schedule_shift.end_time, 'HH24:MI') as end_hour
        FROM dates
        CROSS JOIN doctor
        JOIN schedule_entry ON doctor.id = schedule_entry.doctor_id
        JOIN schedule_shift ON schedule_entry.shift_id = schedule_shift.id
        JOIN room ON schedule_entry.room_id = room.id
        WHERE doctor.id = :doctor_id
        AND CASE EXTRACT(DOW FROM dates.date)
            WHEN 0 THEN 7
            ELSE EXTRACT(DOW FROM dates.date)
        END = schedule_shift.day_of_week
        ORDER BY dates.date, schedule_shift.start_time
    """)
        .bind(doctor_id=doctor_id, days_interval=days_ahead)
        .many_rows()
    )


def get_profile_types_for_dropdown(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT id, name
        FROM doctor_profile_type
        ORDER BY name
    """).many_rows()


def get_doctors_count_by_profile(sql: SqlQueryRunner, profile_id: int | None) -> int:
    if not profile_id:
        return 0

    result = (
        sql.query("""
        SELECT COUNT(*) as doctors_count
        FROM doctor
        WHERE profile_id = :profile_id
    """)
        .bind(profile_id=profile_id)
        .scalar()
    )

    return result if result else 0


def get_patients_with_home_visits(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        WITH LastHomeVisits AS (
            SELECT 
                patient_id,
                home_visit_address,
                ROW_NUMBER() OVER (
                    PARTITION BY patient_id 
                    ORDER BY visit_date DESC
                ) as rn
            FROM visit
            JOIN medical_history ON visit.medical_history_id = medical_history.id
            WHERE home_visit_address IS NOT NULL
        )
        SELECT 
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            LastHomeVisits.home_visit_address as last_visit_address
        FROM LastHomeVisits
        JOIN patient ON LastHomeVisits.patient_id = patient.id
        WHERE rn = 1
        ORDER BY patient.last_name, patient.first_name;
    """).many_rows()


def get_doctors_home_visits_count(sql: SqlQueryRunner) -> list[dict]:
    """Get count of home visits handled by each doctor."""
    return sql.query("""
        SELECT 
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS doctor_name,
            COUNT(CASE WHEN home_visit_address IS NOT NULL THEN 1 END) as home_visits_count
        FROM doctor
        LEFT JOIN visit ON doctor.id = visit.doctor_id
        GROUP BY doctor.id, doctor.last_name, doctor.first_name, doctor.patronymic
        ORDER BY home_visits_count DESC, doctor.last_name
    """).many_rows()


def get_procedures_list(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT 
            name as procedure_name,
            COALESCE(description, 'Опис відсутній') as description
        FROM procedure
        ORDER BY name;
    """).many_rows()


def get_last_week_procedures_count(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT 
            procedure.name as procedure_name,
            COUNT(line_procedure.id) as procedures_count
        FROM procedure
        LEFT JOIN line_procedure ON procedure.id = line_procedure.procedure_id
        LEFT JOIN visit ON line_procedure.visit_id = visit.id
            AND visit.visit_date >= CURRENT_DATE - INTERVAL '7 days'
            AND visit.visit_date <= CURRENT_DATE
        GROUP BY procedure.id, procedure.name
        ORDER BY procedures_count DESC, procedure.name;
    """).many_rows()


def get_last_week_procedures_patients(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT DISTINCT
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        JOIN visit ON medical_history.id = visit.medical_history_id
        JOIN line_procedure ON visit.id = line_procedure.visit_id
        WHERE visit.visit_date >= CURRENT_DATE - INTERVAL '7 days'
            AND visit.visit_date <= CURRENT_DATE
        ORDER BY patient_name;
    """).many_rows()


def get_fluorography_patients_by_date(
    sql: SqlQueryRunner, date: str | None
) -> list[dict]:
    if not date:
        return []

    return (
        sql.query("""
        SELECT DISTINCT
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            patient.phone,
            patient.address
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        JOIN visit ON medical_history.id = visit.medical_history_id
        JOIN line_procedure ON visit.id = line_procedure.visit_id
        JOIN procedure ON line_procedure.procedure_id = procedure.id
        WHERE procedure.name = 'Флюрографія'
            AND visit.visit_date = :visit_date
        ORDER BY patient_name;
    """)
        .bind(visit_date=date)
        .many_rows()
    )


def get_overdue_vaccinations_patients(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT DISTINCT
            patient.last_name || ' ' || 
            LEFT(patient.first_name, 1) || '.' ||
            CASE WHEN patient.patronymic IS NOT NULL 
                THEN LEFT(patient.patronymic, 1) || '.'
                ELSE ''
            END AS patient_name,
            patient.phone,
            patient.address,
            vaccination_type.name as vaccination_name,
            vaccination.accept_until as due_date
        FROM patient
        JOIN medical_history ON patient.id = medical_history.patient_id
        JOIN vaccination ON medical_history.id = vaccination.medical_history_id
        JOIN vaccination_type ON vaccination.vaccination_type_id = vaccination_type.id
        WHERE vaccination.completed_date IS NULL
            AND vaccination.accept_until < CURRENT_DATE
        ORDER BY due_date DESC, patient_name;
    """).many_rows()


def get_physiotherapy_rooms(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT 
            room.room_number
        FROM room
        JOIN room_type ON room.room_type_id = room_type.id
        WHERE room_type.name = 'Фізіотерапевтичний'
        ORDER BY room.room_number;
    """).many_rows()


def get_physiotherapy_rooms_schedule(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
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
            room.room_number,
            to_char(schedule_shift.start_time, 'HH24:MI') as start_time,
            to_char(schedule_shift.end_time, 'HH24:MI') as end_time
        FROM schedule_entry
        JOIN room ON schedule_entry.room_id = room.id
        JOIN room_type ON room.room_type_id = room_type.id
        JOIN schedule_shift ON schedule_entry.shift_id = schedule_shift.id
        WHERE room_type.name = 'Фізіотерапевтичний'
        ORDER BY 
            schedule_shift.day_of_week,
            room.room_number,
            schedule_shift.start_time;
    """).many_rows()


def get_doctors_count_by_room(sql: SqlQueryRunner) -> list[dict]:
    """Get count of unique doctors working in each room during the week."""
    return sql.query("""
        SELECT 
            room.room_number,
            room_type.name as room_type_name,
            COUNT(DISTINCT schedule_entry.doctor_id) as doctors_count
        FROM room
        JOIN room_type ON room.room_type_id = room_type.id
        LEFT JOIN schedule_entry ON room.id = schedule_entry.room_id
        GROUP BY room.id, room.room_number, room_type.name
        ORDER BY room.room_number;
    """).many_rows()


def get_clinic_visits_last_month(sql: SqlQueryRunner) -> int:
    result = sql.query("""
        SELECT COUNT(*) as visits_count
        FROM visit
        WHERE visit_date >= CURRENT_DATE - INTERVAL '30 days'
            AND visit_date <= CURRENT_DATE
            AND home_visit_address IS NULL;
    """).one_row()
    return result["visits_count"]


def get_clinic_visits_count_by_profile(sql: SqlQueryRunner) -> list[dict]:
    return sql.query("""
        SELECT 
            doctor_profile_type.name as profile_name,
            COUNT(visit.id) as visits_count
        FROM doctor_profile_type
        LEFT JOIN doctor ON doctor_profile_type.id = doctor.profile_id
        LEFT JOIN visit ON doctor.id = visit.doctor_id 
            AND visit.home_visit_address IS NULL
            AND visit.visit_date >= CURRENT_DATE - INTERVAL '30 days'
            AND visit.visit_date <= CURRENT_DATE
        GROUP BY doctor_profile_type.id, doctor_profile_type.name
        ORDER BY visits_count DESC;
    """).many_rows()
