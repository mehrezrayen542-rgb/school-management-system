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


COMMIT;
