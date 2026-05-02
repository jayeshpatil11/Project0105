from src.database import SessionLocal
from src.models import User, Batch, Session, Attendance, BatchStudent
from src.auth import hash_password
import random

db = SessionLocal()

# 2 institutions
inst1 = User(name="Inst1", email="inst1@test.com", role="institution", hashed_password=hash_password("123"))
inst2 = User(name="Inst2", email="inst2@test.com", role="institution", hashed_password=hash_password("123"))

db.add_all([inst1, inst2])
db.commit()

# 4 trainers
trainers = []
for i in range(4):
    t = User(name=f"trainer{i}", email=f"trainer{i}@test.com", role="trainer", hashed_password=hash_password("123"))
    db.add(t)
    trainers.append(t)

# 15 students
students = []
for i in range(15):
    s = User(name=f"student{i}", email=f"student{i}@test.com", role="student", hashed_password=hash_password("123"))
    db.add(s)
    students.append(s)

db.commit()

# 3 batches
batches = []
for i in range(3):
    b = Batch(name=f"batch{i}", institution_id=inst1.id)
    db.add(b)
    batches.append(b)

db.commit()

# assign students to batches
for i, student in enumerate(students):
    db.add(BatchStudent(batch_id=batches[i % 3].id, student_id=student.id))

db.commit()

# 8 sessions
sessions = []
for i in range(8):
    s = Session(
        batch_id=batches[i % 3].id,
        trainer_id=trainers[i % 4].id,
        title=f"Session {i}"
    )
    db.add(s)
    sessions.append(s)

db.commit()

# attendance
for session in sessions:
    for student in students:
        db.add(Attendance(
            session_id=session.id,
            student_id=student.id,
            status=random.choice(["present", "absent", "late"])
        ))

db.commit()

print("✅ Seed data created")