USE student_performance;

INSERT IGNORE INTO students (roll_no, name, section) VALUES
('CSE001', 'Aarav Kumar', 'A'),
('CSE002', 'Ananya Rao', 'A'),
('CSE003', 'Rohan Sharma', 'B'),
('CSE004', 'Meera Patel', 'B'),
('CSE005', 'Ishaan Reddy', 'A');

INSERT IGNORE INTO subjects (subject_name, max_marks, pass_marks) VALUES
('Python Programming', 100, 40),
('Database Management', 100, 40),
('Mathematics', 100, 40),
('Computer Networks', 100, 40);

INSERT IGNORE INTO marks (student_id, subject_id, assessment, marks_obtained)
SELECT s.student_id, sub.subject_id, 'Internal 1',
CASE
  WHEN s.roll_no='CSE001' AND sub.subject_name='Python Programming' THEN 92
  WHEN s.roll_no='CSE001' AND sub.subject_name='Database Management' THEN 88
  WHEN s.roll_no='CSE001' AND sub.subject_name='Mathematics' THEN 85
  WHEN s.roll_no='CSE001' AND sub.subject_name='Computer Networks' THEN 90
  WHEN s.roll_no='CSE002' AND sub.subject_name='Python Programming' THEN 78
  WHEN s.roll_no='CSE002' AND sub.subject_name='Database Management' THEN 82
  WHEN s.roll_no='CSE002' AND sub.subject_name='Mathematics' THEN 75
  WHEN s.roll_no='CSE002' AND sub.subject_name='Computer Networks' THEN 80
  WHEN s.roll_no='CSE003' AND sub.subject_name='Python Programming' THEN 35
  WHEN s.roll_no='CSE003' AND sub.subject_name='Database Management' THEN 48
  WHEN s.roll_no='CSE003' AND sub.subject_name='Mathematics' THEN 52
  WHEN s.roll_no='CSE003' AND sub.subject_name='Computer Networks' THEN 39
  WHEN s.roll_no='CSE004' AND sub.subject_name='Python Programming' THEN 65
  WHEN s.roll_no='CSE004' AND sub.subject_name='Database Management' THEN 70
  WHEN s.roll_no='CSE004' AND sub.subject_name='Mathematics' THEN 68
  WHEN s.roll_no='CSE004' AND sub.subject_name='Computer Networks' THEN 72
  WHEN s.roll_no='CSE005' AND sub.subject_name='Python Programming' THEN 88
  WHEN s.roll_no='CSE005' AND sub.subject_name='Database Management' THEN 91
  WHEN s.roll_no='CSE005' AND sub.subject_name='Mathematics' THEN 94
  ELSE 86
END
FROM students s CROSS JOIN subjects sub;
