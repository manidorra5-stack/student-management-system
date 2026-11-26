-- ============================================================================
-- Student Management System - Initial Seed Data
-- Default credentials:
--   Admin   -> username: admin   | password: admin123
--   Teacher -> username: teacher | password: teacher123
-- ============================================================================

USE student_management_db;

-- 1. Seed Users
INSERT INTO users (username, email, password_hash, full_name, role) VALUES
('admin', 'admin@isgs.rnu.tn', 'pbkdf2:sha256:600000$isgs2026admin$324087d4435c48b698eac4123bb72b81a978b8934a11a1b29a11678bf4e81e11', 'Administrateur ISG Sousse', 'admin'),
('teacher', 'z.sakhrawi@isgs.rnu.tn', 'pbkdf2:sha256:600000$isgs2026prof$edf7621c71dbeea16d1c971f720b89d9b2a1336576bf270db5cbdb38b5a93cc9', 'Zaineb Sakhrawi', 'teacher');

-- 2. Seed Teachers
INSERT INTO teachers (teacher_code, first_name, last_name, email, department, phone) VALUES
('TCH-001', 'Zaineb', 'Sakhrawi', 'z.sakhrawi@isgs.rnu.tn', 'Informatique & DevOps', '+216 73 332 976'),
('TCH-002', 'Mohamed', 'Ben Ali', 'm.benali@isgs.rnu.tn', 'Génie Logiciel & Web', '+216 73 332 977'),
('TCH-003', 'Sarra', 'Trabelsi', 's.trabelsi@isgs.rnu.tn', 'Systèmes d''Information & BD', '+216 73 332 978');

-- 3. Seed Students
INSERT INTO students (student_code, first_name, last_name, email, date_of_birth, major, academic_level, status) VALUES
('STD-2026-001', 'Dorra', 'Mansour', 'dorra.mansour@etudiant-isgs.tn', '2004-05-14', 'Business Computing (3 LIG)', '3rd Year', 'active'),
('STD-2026-002', 'Youssef', 'Khelifi', 'youssef.khelifi@etudiant-isgs.tn', '2004-08-22', 'Business Computing (3 LIG)', '3rd Year', 'active'),
('STD-2026-003', 'Ines', 'Bouazizi', 'ines.bouazizi@etudiant-isgs.tn', '2004-11-03', 'Business Computing (3 LIG)', '3rd Year', 'active'),
('STD-2026-004', 'Ahmed', 'Jebali', 'ahmed.jebali@etudiant-isgs.tn', '2003-02-19', 'Business Computing (3 LIG)', '3rd Year', 'active'),
('STD-2026-005', 'Mariem', 'Gharbi', 'mariem.gharbi@etudiant-isgs.tn', '2004-07-30', 'Business Computing (3 LIG)', '3rd Year', 'active');

-- 4. Seed Courses
INSERT INTO courses (course_code, title, description, credits, semester, teacher_id) VALUES
('DEVOPS-301', 'Introduction au DevOps & CI/CD', 'Git, GitHub, Jenkins Pipelines, Docker et automatisation des tests.', 4.0, 'S1', 1),
('WEB-302', 'Développement Web Avancé (Python/Flask)', 'Architecture MVC, APIs REST, sécurité et intégration front-end.', 3.5, 'S1', 2),
('BDD-303', 'Administration Bases de Données Relationnelles', 'Modélisation MySQL, indexation, transactions et optimisation SQL.', 3.0, 'S1', 3),
('BI-304', 'Business Intelligence & Data Analytics', 'Entrepôts de données, ETL et tableaux de bord décisionnels.', 3.0, 'S2', 3);

-- 5. Seed Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, status) VALUES
(1, 1, '2026-09-15', 'enrolled'),
(1, 2, '2026-09-15', 'enrolled'),
(1, 3, '2026-09-15', 'enrolled'),
(2, 1, '2026-09-16', 'enrolled'),
(2, 2, '2026-09-16', 'enrolled'),
(3, 1, '2026-09-16', 'enrolled'),
(3, 3, '2026-09-16', 'enrolled'),
(4, 1, '2026-09-17', 'enrolled'),
(5, 2, '2026-09-17', 'enrolled');

-- 6. Seed Grades (Formula: 40% CC + 60% Exam)
INSERT INTO grades (enrollment_id, continuous_assessment, exam_score, final_grade, remarks) VALUES
(1, 17.50, 18.00, 17.80, 'Excellent maîtrise CI/CD'),
(2, 16.00, 15.50, 15.70, 'Très bon travail'),
(3, 14.50, 15.00, 14.80, 'Bien'),
(4, 13.00, 12.50, 12.70, 'Assez bien'),
(5, 11.00, 10.50, 10.70, 'Passable'),
(6, 15.50, 16.50, 16.10, 'Très bien'),
(7, 8.50, 9.00, 8.80, 'Session de rattrapage'),
(8, 14.00, 14.50, 14.30, 'Bon niveau'),
(9, 16.50, 17.00, 16.80, 'Excellent');