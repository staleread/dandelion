from typing import Annotated
from fastapi import APIRouter, Query

from app.common.template.utils import TemplateContextDep
from app.common.database.utils import QueryRunnerDep
from app.classic.query.service import (
    get_all_patients,
    search_patients_by_last_name,
    search_patients_by_history_id,
    search_patients_by_health,
    search_patients_by_therapist,
)

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


@router.get("/doctors_overview")
async def get_doctors_overview(sql: QueryRunnerDep, template: TemplateContextDep):
    doctors = sql.query("""
        SELECT 
            doctor.first_name,
            doctor.last_name,
            doctor.patronymic,
            doctor_profile_type.name as profile_name,
            doctor.phone
        FROM doctor
        JOIN doctor_profile_type ON doctor.profile_id = doctor_profile_type.id
        ORDER BY doctor.last_name, doctor.first_name;
    """).many_rows()

    return template("/classic/query/doctors_overview.html", {"doctors": doctors})


@router.get("/given_documents")
async def get_given_documents(sql: QueryRunnerDep, template: TemplateContextDep):
    documents = sql.query("""
        SELECT 
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS doctor_name,
            document_type.name as document_type_name,
            visit.visit_date as issue_date
        FROM document
        JOIN visit ON document.visit_id = visit.id
        JOIN doctor ON visit.doctor_id = doctor.id
        JOIN document_type ON document.document_type_id = document_type.id
        ORDER BY visit.visit_date DESC;
    """).many_rows()

    return template("/classic/query/given_documents.html", {"documents": documents})


@router.get("/doctors_visits_per_week")
async def get_doctors_visits_per_week(
    sql: QueryRunnerDep, template: TemplateContextDep
):
    visits = sql.query("""
        SELECT 
            doctor.last_name || ' ' || 
            LEFT(doctor.first_name, 1) || '.' ||
            CASE WHEN doctor.patronymic IS NOT NULL 
                THEN LEFT(doctor.patronymic, 1) || '.'
                ELSE ''
            END AS doctor_name,
            COUNT(visit.id) as visits_count
        FROM doctor
        LEFT JOIN visit ON doctor.id = visit.doctor_id
            AND visit.visit_date >= CURRENT_DATE - INTERVAL '7 days'
            AND visit.visit_date <= CURRENT_DATE
        GROUP BY doctor.id, doctor.last_name, doctor.first_name, doctor.patronymic
        ORDER BY visits_count DESC;
    """).many_rows()

    return template("/classic/query/doctors_visits_per_week.html", {"visits": visits})


@router.get("/patient_search/by_last_name")
async def search_by_last_name(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    query: Annotated[str, Query(description="Patient's last name")] = "",
):
    patients = (
        search_patients_by_last_name(sql, query) if query else get_all_patients(sql)
    )
    return template(
        "/classic/query/patient_search/by_last_name.html",
        {"patients": patients, "filter_type": "last_name", "search_query": query},
    )


@router.get("/patient_search/by_history")
async def search_by_history(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    query: Annotated[str, Query(description="Medical history ID")] = "",
):
    patients = (
        search_patients_by_history_id(sql, query) if query else get_all_patients(sql)
    )
    return template(
        "/classic/query/patient_search/by_history.html",
        {"patients": patients, "filter_type": "history_id", "search_query": query},
    )


@router.get("/patient_search/by_health")
async def search_by_health(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    query: Annotated[str, Query(description="Health state or diagnosis")] = "",
):
    patients = search_patients_by_health(sql, query) if query else get_all_patients(sql)
    return template(
        "/classic/query/patient_search/by_health.html",
        {"patients": patients, "filter_type": "health_state", "search_query": query},
    )


@router.get("/patient_search/by_therapist")
async def search_by_therapist(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    query: Annotated[str, Query(description="Therapist's last name")] = "",
):
    patients = (
        search_patients_by_therapist(sql, query) if query else get_all_patients(sql)
    )
    return template(
        "/classic/query/patient_search/by_therapist.html",
        {"patients": patients, "filter_type": "therapist", "search_query": query},
    )
