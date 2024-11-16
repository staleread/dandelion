insert into doctor_profile_type (name) values
    (N'Терапевт'),
    (N'Хірург'),
    (N'Педіатр'),
    (N'Невролог'),
    (N'Кардіолог'),
    (N'Офтальмолог');

insert into room_type (name) values
    (N'Кабінет сімейного лікаря'),
    (N'Маніпуляційна'),
    (N'Операційна'),
    (N'Фізіотерапевтичний'),
    (N'Лабораторія');

insert into visit_status_type (name) values
    (N'Заплановано'),
    (N'В процесі'),
    (N'Завершено'),
    (N'Скасовано');

insert into vaccination_type (name) values
    (N'Гепатит B'),
    (N'Коронавірус'),
    (N'Поліомієліт');

insert into doctor (first_name, last_name, patronymic, profile_id, phone) values
    (N'Олена', N'Коваленко', N'Петрівна', 1, '+380501234567'),
    (N'Михайло', N'Шевченко', N'Іванович', 2, '+380672345678'),
    (N'Ірина', N'Бондаренко', N'Василівна', 3, '+380633456789'),
    (N'Андрій', N'Мельник', N'Олександрович', 4, '+380944567890'),
    (N'Наталія', N'Ткаченко', N'Миколаївна', 5, '+380975678901'),
    (N'Василь', N'Петренко', N'Андрійович', 6, '+380966789012'),
    (N'Тетяна', N'Лисенко', N'Сергіївна', 1, '+380987890123'),
    (N'Сергій', N'Марченко', N'Володимирович', 2, '+380998901234');

insert into room (room_number, room_type_id) values
    (N'101-А', 1),
    (N'102-А', 1),
    (N'103-А', 1),
    (N'201-Б', 2),
    (N'202-Б', 2),
    (N'301-В', 3),
    (N'302-В', 3),
    (N'401-Г', 4),
    (N'501-Д', 5),
    (N'502-Д', 5);

insert into schedule_shift (day_of_week, start_time, end_time) values
    -- Monday (1)
    (1, '08:00', '13:00'),
    (1, '14:00', '19:00'),
    -- Tuesday (2)
    (2, '08:00', '13:00'),
    (2, '14:00', '19:00'),
    -- Wednesday (3)
    (3, '08:00', '13:00'),
    (3, '14:00', '19:00'),
    -- Thursday (4)
    (4, '08:00', '13:00'),
    (4, '14:00', '19:00'),
    -- Friday (5)
    (5, '08:00', '13:00'),
    (5, '14:00', '19:00'),
    -- Saturday (6)
    (6, '08:00', '13:00'),
    (6, '14:00', '19:00'),
    -- Sunday (7)
    (7, '09:00', '13:00'),
    (7, '14:00', '18:00');

insert into schedule_entry (doctor_id, room_id, shift_id) values
    -- Олена Коваленко (Терапевт, id=1) - Sunday off
    (1, 1, 1),  -- Monday morning
    (1, 1, 4),  -- Tuesday afternoon
    (1, 1, 5),  -- Wednesday morning
    (1, 1, 8),  -- Thursday afternoon
    (1, 1, 9),  -- Friday morning
    (1, 1, 12), -- Saturday afternoon

    -- Михайло Шевченко (Хірург, id=2) - Saturday and Sunday off
    (2, 6, 1),  -- Monday morning
    (2, 6, 4),  -- Tuesday afternoon
    (2, 6, 5),  -- Wednesday morning
    (2, 6, 8),  -- Thursday afternoon
    (2, 6, 9),  -- Friday morning

    -- Ірина Бондаренко (Педіатр, id=3) - Friday and Sunday off
    (3, 2, 1),  -- Monday morning
    (3, 2, 4),  -- Tuesday afternoon
    (3, 2, 5),  -- Wednesday morning
    (3, 2, 8),  -- Thursday afternoon
    (3, 2, 11), -- Saturday morning

    -- Андрій Мельник (Невролог, id=4) - Wednesday and Sunday off
    (4, 3, 1),  -- Monday morning
    (4, 3, 4),  -- Tuesday afternoon
    (4, 3, 7),  -- Thursday morning
    (4, 3, 10), -- Friday afternoon
    (4, 3, 11), -- Saturday morning

    -- Наталія Ткаченко (Кардіолог, id=5) - Tuesday and Sunday off
    (5, 3, 1),  -- Monday morning
    (5, 3, 5),  -- Wednesday morning
    (5, 3, 8),  -- Thursday afternoon
    (5, 3, 9),  -- Friday morning
    (5, 3, 12), -- Saturday afternoon

    -- Василь Петренко (Офтальмолог, id=6) - Saturday off
    (6, 4, 1),  -- Monday morning
    (6, 4, 4),  -- Tuesday afternoon
    (6, 4, 5),  -- Wednesday morning
    (6, 4, 8),  -- Thursday afternoon
    (6, 4, 9),  -- Friday morning
    (6, 4, 13), -- Sunday morning

    -- Тетяна Лисенко (Терапевт, id=7) - Saturday off
    (7, 2, 2),  -- Monday afternoon
    (7, 2, 3),  -- Tuesday morning
    (7, 2, 6),  -- Wednesday afternoon
    (7, 2, 7),  -- Thursday morning
    (7, 2, 10), -- Friday afternoon
    (7, 2, 14), -- Sunday afternoon

    -- Сергій Марченко (Хірург, id=8) - Thursday and Sunday off
    (8, 7, 2),  -- Monday afternoon
    (8, 7, 3),  -- Tuesday morning
    (8, 7, 6),  -- Wednesday afternoon
    (8, 7, 10), -- Friday afternoon
    (8, 7, 11); -- Saturday morning

insert into patient (first_name, last_name, patronymic, birth_date, address, phone) values
    (N'Марія', N'Іваненко', N'Олександрівна', '1985-03-15', N'вул. Шевченка 45, кв. 12', '+380501112233'),
    (N'Петро', N'Василенко', N'Михайлович', '1976-08-22', N'вул. Франка 23, кв. 5', '+380672223344'),
    (N'Софія', N'Григоренко', N'Андріївна', '1992-11-30', N'просп. Перемоги 78, кв. 41', '+380633334455'),
    (N'Олександр', N'Павленко', N'Вікторович', '1968-04-05', N'вул. Сагайдачного 12, кв. 8', '+380944445566'),
    (N'Анна', N'Романенко', N'Ігорівна', '1998-07-17', null, '+380955556677'),
    (N'Максим', N'Даниленко', N'Олегович', '1982-12-03', N'вул. Хрещатик 89, кв. 32', '+380966667788'),
    (N'Вікторія', N'Тимошенко', N'Василівна', '1995-09-25', N'вул. Лесі Українки 34, кв. 19', null),
    (N'Дмитро', N'Захаренко', N'Андрійович', '1973-06-11', N'просп. Науки 67, кв. 23', '+380988889900'),
    (N'Оксана', N'Литвиненко', N'Петрівна', '1989-01-28', N'вул. Богдана Хмельницького 90, кв. 7', '+380991112233'),
    (N'Артем', N'Кравченко', N'Миколайович', '2001-05-14', N'вул. Пушкінська 45, кв. 11', '+380992223344'),
    (N'Наталія', N'Федоренко', N'Олексіївна', '1979-10-09', N'вул. Грушевського 23, кв. 16', '+380993334455'),
    (N'Ігор', N'Савченко', N'Володимирович', '1965-02-19', N'просп. Миру 78, кв. 29', '+380994445566'),
    (N'Юлія', N'Кузьменко', N'Ярославівна', '1994-08-07', N'вул. Київська 12, кв. 3', '+380995556677'),
    (N'Андрій', N'Поліщук', N'Степанович', '1987-11-23', N'вул. Гоголя 56, кв. 14', '+380996667788'),
    (N'Катерина', N'Ткаченко', N'Дмитрівна', '1999-04-30', N'вул. Івана Франка 89, кв. 25', '+380997778899');

-- Medical history records for each patient
insert into medical_history (patient_id, therapist_id)
select 
    p.id,
    -- Assign either Олена Коваленко or Тетяна Лисенко (both therapists) as family doctor
    case when random() > 0.5 then 1 else 7 end
from patient p;

insert into procedure (name, description) values
    (N'Вимірювання артеріального тиску', N'Вимірювання систолічного та діастолічного артеріального тиску за допомогою тонометра'),
    (N'Електрокардіограма (ЕКГ)', N'Реєстрація електричної активності серця для діагностики серцево-судинних захворювань'),
    (N'Загальний аналіз крові', N'Лабораторне дослідження крові для оцінки загального стану здоров''я'),
    (N'Ультразвукове дослідження', N'УЗД внутрішніх органів для діагностики патологій'),
    (N'Вакцинація', N'Введення вакцини для профілактики інфекційних захворювань'),
    (N'Перев''язка', N'Заміна перев''язувального матеріалу та обробка ран'),
    (N'Видалення швів', N'Видалення післяопераційних швів'),
    (N'Рентгенографія', N'Рентгенівське дослідження органів та кісток'),
    (N'Офтальмоскопія', N'Обстеження очного дна за допомогою офтальмоскопа'),
    (N'Аудіометрія', N'Перевірка гостроти слуху'),
    (N'Спірометрія', N'Дослідження функції зовнішнього дихання'),
    (N'Глюкометрія', N'Вимірювання рівня глюкози в крові'),
    (N'Взяття мазка', N'Забір біологічного матеріалу для лабораторного дослідження'),
    (N'Фізіотерапевтичні процедури', N'Лікувальні процедури з використанням фізичних факторів'),
    (N'Ін''єкція', N'Внутрішньом''язове або внутрішньовенне введення лікарських засобів');

insert into visit (medical_history_id, doctor_id, visit_date, start_time, end_time, diagnosis, status_id, home_visit_address) values
    -- Past regular visits (at clinic)
    (1, 1, '2024-10-05', '09:00', '09:30', N'Ангіна', 3, null),
    (2, 5, '2024-10-05', '10:00', '10:30', N'Гіпертонічна хвороба', 3, null),
    (3, 3, '2024-10-06', '11:00', '11:30', N'Профілактичний огляд', 3, null),
    (4, 4, '2024-10-07', '14:00', '14:30', N'Остеохондроз шийного відділу', 3, null),
    (5, 6, '2024-10-08', '15:00', '15:30', N'Міопія середнього ступеня', 3, null),
    
    -- Past home visits
    (6, 1, '2024-10-10', '16:00', '16:30', N'Ангіна', 3, N'вул. Хрещатик 89, кв. 32'),
    (7, 7, '2024-10-12', '17:00', '17:30', N'ГРВІ', 3, N'вул. Лесі Українки 34, кв. 19'),
    
    -- Future appointments
    (8, 2, '2024-11-20', '09:00', '09:30', null, 1, null),
    (9, 5, '2024-11-21', '10:00', '10:30', null, 1, null),
    (10, 3, '2024-11-22', '11:00', '11:30', null, 1, null),
    
    -- More past regular visits
    (11, 4, '2024-10-15', '09:00', '09:30', N'Мігрень', 3, null),
    (12, 6, '2024-10-16', '10:00', '10:30', N'Кон''юнктивіт', 3, null),
    (13, 1, '2024-10-18', '11:00', '11:30', N'Ангіна', 3, null),
    (14, 2, '2024-10-20', '14:00', '14:30', N'Апендицит', 3, null),
    (15, 5, '2024-10-22', '15:00', '15:30', N'Аритмія', 3, null),
    
    -- More past home visits
    (1, 7, '2024-10-25', '16:00', '16:30', N'Пневмонія', 3, N'вул. Шевченка 45, кв. 12'),
    (2, 1, '2024-10-27', '17:00', '17:30', N'Ангіна', 3, N'вул. Франка 23, кв. 5'),
    
    -- Cancelled visits
    (3, 3, '2024-11-01', '09:00', '09:30', null, 4, null),
    (4, 4, '2024-11-02', '10:00', '10:30', null, 4, null),
    
    -- In progress (current date visits)
    (5, 5, '2024-11-17', '09:00', '09:30', null, 2, null),
    (6, 6, '2024-11-17', '10:00', '10:30', null, 2, null),
    
    -- More past regular visits
    (7, 1, '2024-11-01', '11:00', '11:30', N'Гастрит', 3, null),
    (8, 2, '2024-11-03', '14:00', '14:30', N'Варикозне розширення вен', 3, null),
    (9, 3, '2024-11-05', '15:00', '15:30', N'Ангіна', 3, null),
    
    -- More past home visits
    (10, 7, '2024-11-07', '16:00', '16:30', N'Харчове отруєння', 3, N'просп. Перемоги 78, кв. 41'),
    
    -- Future appointments with home visits
    (11, 1, '2024-11-25', '09:00', '09:30', null, 1, N'вул. Грушевського 23, кв. 16'),
    (12, 7, '2024-11-27', '10:00', '10:30', null, 1, N'просп. Миру 78, кв. 29'),
    
    -- Regular future appointments
    (13, 2, '2024-12-01', '11:00', '11:30', null, 1, null),
    (14, 3, '2024-12-05', '14:00', '14:30', null, 1, null),
    (15, 4, '2024-12-10', '15:00', '15:30', null, 1, null);

insert into line_procedure (visit_id, procedure_id, room_id) values
    -- Regular visits
    (1, 1, 1),   -- Blood pressure for angina patient in therapist's room
    (1, 13, 1),  -- Swab taking for the same patient
    
    (2, 2, 3),   -- ECG for hypertension patient in cardiologist's room
    (2, 1, 3),   -- Blood pressure for the same patient
    
    (3, 1, 2),   -- Blood pressure for check-up
    (3, 3, 5),   -- Blood test in laboratory
    
    (4, 8, 5),   -- X-ray for osteochondrosis
    
    (5, 9, 4),   -- Ophthalmoscopy for myopia
    
    -- Home visits (no room_id)
    (6, 1, null),  -- Blood pressure for angina at home
    (6, 13, null), -- Swab taking at home
    
    (7, 1, null),  -- Blood pressure for ARVI at home
    (7, 13, null), -- Swab taking at home
    
    -- More regular visits
    (11, 8, 3),    -- X-ray for migraine
    
    (12, 9, 4),    -- Ophthalmoscopy for conjunctivitis
    
    (13, 1, 1),    -- Blood pressure for angina
    (13, 13, 1),   -- Swab taking for angina
    
    (14, 6, 4),    -- Dressing after appendicitis
    
    (15, 2, 3),    -- ECG for arrhythmia
    
    -- More home visits
    (16, 1, null),  -- Blood pressure for pneumonia at home
    (16, 13, null), -- Swab taking for pneumonia at home
    
    (17, 1, null),  -- Blood pressure for angina at home
    (17, 13, null), -- Swab taking for angina at home
    
    -- Regular visits
    (22, 1, 1),    -- Blood pressure for gastritis
    
    (23, 6, 6),    -- Dressing for varicose veins
    
    (24, 1, 2),    -- Blood pressure for angina
    (24, 13, 2),   -- Swab taking for angina
    
    -- Home visit
    (25, 1, null),  -- Blood pressure for food poisoning at home
    (25, 13, null); -- Swab taking for food poisoning at home

insert into document_type (name, description, template) values
    (N'Листок непрацездатності', N'дає право на звільнення від роботи у зв’язку з непрацездатністю та призначення матеріального забезпечення застрахованій особі в разі тимчасової непрацездатності, вагітності та пологів', '{"patient_full_name": "ПІБ пацієнта", "doctor_full_name": "ПІБ лікаря", "diagnosis": "Назва захворювання", "start_date": "Дата початку непрацездатності", "end_date": "Дата закінчення непрацездатності", "issue_date": "Дата видачі листка"}'),
    (N'Сертифікат про вакцинацію', N'підтверджує факт вакцинації від інфекційних захворювань', '{"patient_full_name": "ПІБ пацієнта", "vaccination_date": "Дата вакцинації", "vaccination_type": "Назва вакцини", "doctor_full_name": "ПІБ лікаря", "issue_date": "Дата видачі сертифіката"}');

insert into document (visit_id, document_type_id, data) values
    -- Sick leaves for angina cases
    (1, 1, '{
        "patient_full_name": "Іваненко Марія Олександрівна",
        "doctor_full_name": "Коваленко Олена Петрівна",
        "diagnosis": "Ангіна",
        "start_date": "2024-10-05",
        "end_date": "2024-10-12",
        "issue_date": "2024-10-05"
    }'::json),
    
    (6, 1, '{
        "patient_full_name": "Даниленко Максим Олегович",
        "doctor_full_name": "Коваленко Олена Петрівна",
        "diagnosis": "Ангіна",
        "start_date": "2024-10-10",
        "end_date": "2024-10-17",
        "issue_date": "2024-10-10"
    }'::json),
    
    -- Sick leave for appendicitis (longer period)
    (14, 1, '{
        "patient_full_name": "Поліщук Андрій Степанович",
        "doctor_full_name": "Шевченко Михайло Іванович",
        "diagnosis": "Апендицит",
        "start_date": "2024-10-20",
        "end_date": "2024-11-03",
        "issue_date": "2024-10-20"
    }'::json),
    
    -- Sick leave for pneumonia
    (16, 1, '{
        "patient_full_name": "Іваненко Марія Олександрівна",
        "doctor_full_name": "Лисенко Тетяна Сергіївна",
        "diagnosis": "Пневмонія",
        "start_date": "2024-10-25",
        "end_date": "2024-11-08",
        "issue_date": "2024-10-25"
    }'::json),
    
    -- Vaccination certificates
    (3, 2, '{
        "patient_full_name": "Григоренко Софія Андріївна",
        "vaccination_date": "2024-10-06",
        "vaccination_type": "Коронавірус",
        "doctor_full_name": "Бондаренко Ірина Василівна",
        "issue_date": "2024-10-06"
    }'::json);

insert into vaccination (doctor_id, medical_history_id, vaccination_type_id, completed_date, accept_since, accept_until) values
    -- Completed vaccinations
    (1, 1, 2, '2024-10-06 10:30:00', '2024-10-06', '2025-10-06'),    -- Коронавірус for patient 1
    (3, 3, 1, '2024-10-15 11:15:00', '2024-10-15', '2025-10-15'),    -- Гепатит B for patient 3
    (7, 5, 2, '2024-10-20 09:45:00', '2024-10-20', '2025-10-20'),    -- Коронавірус for patient 5
    
    -- Planned vaccinations (completed_date is null)
    (1, 6, 1, null, '2024-11-20', '2025-11-20'),  -- Гепатит B for patient 6
    (3, 7, 2, null, '2024-11-22', '2025-11-22'),  -- Коронавірус for patient 7
    (7, 8, 3, null, '2024-11-25', '2025-11-25'),  -- Поліомієліт for patient 8
    (1, 9, 2, null, '2024-11-28', '2025-11-28'),  -- Коронавірус for patient 9
    
    -- Second doses planned (for those who completed first dose)
    (1, 1, 2, null, '2024-12-06', '2025-12-06'),  -- Коронавірус second dose
    (3, 3, 1, null, '2024-12-15', '2025-12-15'),  -- Гепатит B second dose
    (7, 5, 2, null, '2024-12-20', '2025-12-20');  -- Коронавірус second dose
