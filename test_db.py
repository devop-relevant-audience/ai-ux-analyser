from sqlmodel import Session

from database import create_db_and_tables, engine
from models import Run

create_db_and_tables()

with Session(engine) as session:
    run = Run(
        url="https://google.com",
        screenshots={
            "mobile": "screenshots/mobile.png",
            "tablet": "screenshots/tablet.png",
            "desktop": "screenshots/desktop.png",
        },
        report={
            "lighthouse": {"score": 95},
            "axe": {"violations": 2},
        },
    )

    session.add(run)
    session.commit()
    session.refresh(run)

    print(f"Run saved with ID: {run.id}")