PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- table attendance
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL,
    attendance_date TEXT NOT NULL,
    morning TEXT NOT NULL,
    evening INTEGER NOT NULL
);

-- table fees
CREATE TABLE fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL,
    receipt_number TEXT NOT NULL,
    reason TEXT NOT NULL,
    amount TEXT NOT NULL,
    fees_date TEXT NOT NULL
);

-- table mark
CREATE TABLE mark (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL,
    trimestre INTEGER NOT NULL,
    language INTEGER NOT NULL,
    english INTEGER NOT NULL,
    maths INTEGER NOT NULL,
    science INTEGER NOT NULL,
    social INTEGER NOT NULL
);

-- table student
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number TEXT NOT NULL,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    standard TEXT NOT NULL
);
INSERT INTO student
(registration_number, full_name, gender, date_of_birth, address, phone, email, standard)
VALUES
('1', 'Lucas Martin', 'male', '2007-05-12', 'Paris', '20123456', 'lucas@gmail.com', '4th'),
('2', 'Emma Bernard', 'female', '2007-09-23', 'Lyon', '22123456', 'emma@gmail.com', '4th'),
('3', 'Louis Dubois', 'male', '2008-01-15', 'Marseille', '23123456', 'louis@gmail.com', '3rd'),
('4', 'Camille Lefevre', 'female', '2007-07-10', 'Toulouse', '24123456', 'chloe@gmail.com', '4th'),
('5', 'Jules Petit', 'male', '2008-03-08', 'Nice', '25123456', 'jules@gmail.com', '3rd');
INSERT INTO mark
(registration_number, trimestre, language, english, maths, science, social)
VALUES
('1', 1, 15, 14, 17, 16, 13),
('1', 2, 16, 15, 18, 15, 14),

('2', 1, 18, 17, 19, 18, 16),
('2', 2, 17, 18, 18, 17, 17),

('3', 1, 12, 13, 14, 12, 11),
('3', 2, 13, 12, 15, 13, 12),

('4', 1, 19, 18, 20, 19, 18),

('5', 1, 14, 15, 13, 14, 15);

INSERT INTO fees
(registration_number, receipt_number, reason, amount, fees_date)
VALUES
('1', '1001', 'Tuition Fees', '300', '2026-01-05'),
('2', '1002', 'Tuition Fees', '300', '2026-01-06'),
('3', '1003', 'Library Fees', '50', '2026-01-07'),
('4', '1004', 'Tuition Fees', '300', '2026-01-08'),
('5', '1005', 'Laboratory Fees', '75', '2026-01-09');
INSERT INTO attendance
(registration_number, attendance_date, morning, evening)
VALUES
('1', '2026-01-10', 'Present', 1),
('2', '2026-01-10', 'Present', 1),
('3', '2026-01-10', 'Absent', 0),
('4', '2026-01-10', 'Present', 1),
('5', '2026-01-10', 'Present', 1);


COMMIT;
