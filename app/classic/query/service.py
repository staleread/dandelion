from app.common.database.utils import SqlQueryRunner


def get_all_patients(sql: SqlQueryRunner) -> list[dict]:
    """Get basic information about all patients."""
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
    """Search patients by last name."""
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
    """Search patients by medical history ID."""
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
    """Search patients by health state or diagnosis."""
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
    """Search patients by therapist's last name."""
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
