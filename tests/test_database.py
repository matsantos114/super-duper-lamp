from sqlalchemy import text
from sqlalchemy.orm import Session


def test_uses_isolated_database(db_session: Session) -> None:
    result = db_session.execute(text("SELECT current_database()"))

    assert result.scalar_one() == "running_app_test"