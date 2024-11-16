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
    get_patients_with_multiple_doctors,
    get_angina_patients_count,
    get_therapists_schedule,
    get_doctors_for_dropdown,
    get_doctor_schedule,
    get_profile_types_for_dropdown,
    get_doctors_count_by_profile,
    get_patients_with_home_visits,
    get_doctors_home_visits_count,
    get_procedures_list,
    get_last_week_procedures_count,
    get_last_week_procedures_patients,
    get_fluorography_patients_by_date,
    get_overdue_vaccinations_patients,
)

router = APIRouter(prefix="/query")


@router.get("/therapist/schedule")
async def get_therapists_schedule_view(
    sql: QueryRunnerDep, template: TemplateContextDep
):
    schedules = get_therapists_schedule(sql)
    return template("/classic/query/therapists_schedule.html", {"schedules": schedules})


@router.get("/doctor/overview")
async def get_doctors_overview_view(sql: QueryRunnerDep, template: TemplateContextDep):
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


@router.get("/document/given")
async def get_given_documents_view(sql: QueryRunnerDep, template: TemplateContextDep):
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


@router.get("/doctor/visits_per_week")
async def get_doctors_visits_per_week_view(
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


@router.get("/patient/search/by_last_name")
async def search_by_last_name_view(
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


@router.get("/patient/search/by_history")
async def search_by_history_view(
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


@router.get("/patient/search/by_health")
async def search_by_health_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    query: Annotated[str, Query(description="Health state or diagnosis")] = "",
):
    patients = search_patients_by_health(sql, query) if query else get_all_patients(sql)
    return template(
        "/classic/query/patient_search/by_health.html",
        {"patients": patients, "filter_type": "health_state", "search_query": query},
    )


@router.get("/patient/search/by_therapist")
async def search_by_therapist_view(
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


@router.get("/patient/multiple_doctors")
async def get_patients_multiple_doctors_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    patients = get_patients_with_multiple_doctors(sql)
    return template(
        "/classic/query/patients_multiple_doctors.html", {"patients": patients}
    )


@router.get("/patient/angina_patients_count")
async def get_angina_patients_count_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    count = get_angina_patients_count(sql)
    return template(
        "/classic/query/angina_patients_count.html", {"patients_count": count}
    )


@router.get("/doctor/schedule/week")
async def get_doctor_week_schedule_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    doctor_id: Annotated[int | None, Query(description="Doctor ID")] = None,
):
    doctors = get_doctors_for_dropdown(sql)
    schedule = get_doctor_schedule(sql, doctor_id, 7)
    return template(
        "/classic/query/doctor_schedule.html",
        {
            "doctors": doctors,
            "schedule": schedule,
            "selected_doctor_id": doctor_id,
            "period": "week",
        },
    )


@router.get("/doctor/schedule/month")
async def get_doctor_month_schedule_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    doctor_id: Annotated[int | None, Query(description="Doctor ID")] = None,
):
    doctors = get_doctors_for_dropdown(sql)
    schedule = get_doctor_schedule(sql, doctor_id, 30)
    return template(
        "/classic/query/doctor_schedule.html",
        {
            "doctors": doctors,
            "schedule": schedule,
            "selected_doctor_id": doctor_id,
            "period": "month",
        },
    )


@router.get("/doctor/count_by_profile")
async def get_doctors_count_by_profile_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    profile_id: Annotated[int | None, Query(description="Profile Type ID")] = None,
):
    profile_types = get_profile_types_for_dropdown(sql)
    count = get_doctors_count_by_profile(sql, profile_id)
    return template(
        "/classic/query/doctors_count_by_profile.html",
        {
            "profile_types": profile_types,
            "doctors_count": count,
            "selected_profile_id": profile_id,
        },
    )


@router.get("/patient/home_visits")
async def get_patients_home_visits_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    patients = get_patients_with_home_visits(sql)
    return template("/classic/query/patients_home_visits.html", {"patients": patients})


@router.get("/doctor/home_visits_count")
async def get_doctors_home_visits_count_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    visits = get_doctors_home_visits_count(sql)
    return template("/classic/query/doctors_home_visits_count.html", {"visits": visits})


@router.get("/procedure")
async def get_procedures_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    procedures = get_procedures_list(sql)
    return template("/classic/query/procedures.html", {"procedures": procedures})


@router.get("/procedure/recent_count")
async def get_recent_procedures_count_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    procedures = get_last_week_procedures_count(sql)
    return template(
        "/classic/query/procedures_recent_count.html", {"procedures": procedures}
    )


@router.get("/procedure/recent_patients")
async def get_recent_procedures_patients_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    patients = get_last_week_procedures_patients(sql)
    return template(
        "/classic/query/procedures_recent_patients.html", {"patients": patients}
    )


@router.get("/procedure/fluorography")
async def get_fluorography_patients_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
    date: Annotated[str | None, Query(description="Visit date")] = None,
):
    patients = get_fluorography_patients_by_date(sql, date)
    return template(
        "/classic/query/fluorography_patients.html",
        {
            "patients": patients,
            "selected_date": date,
        },
    )


@router.get("/vaccination/overdue")
async def get_overdue_vaccinations_view(
    sql: QueryRunnerDep,
    template: TemplateContextDep,
):
    patients = get_overdue_vaccinations_patients(sql)
    return template("/classic/query/overdue_vaccinations.html", {"patients": patients})
