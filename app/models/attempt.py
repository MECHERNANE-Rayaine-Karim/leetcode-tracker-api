from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum
from app.core.database import Base
from enum import Enum
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.problem import Problem

class Status(Enum):
    SOLVED = "solved"
    ATTEMPTED = "attempted"

class Language(Enum):
    """Core programming languages supported on LeetCode."""
    # ===== MOST POPULAR =====
    PYTHON = "Python"
    JAVA = "Java"
    C_PLUS_PLUS = "C++"
    JAVASCRIPT = "JavaScript"
    # ===== ALSO COMMONLY USED =====
    C = "C"
    C_SHARP = "C#"
    GO = "Go"
    RUBY = "Ruby"
    RUST = "Rust"
    TYPESCRIPT = "TypeScript"
    PHP = "PHP"
    KOTLIN = "Kotlin"
    SWIFT = "Swift"
    SCALA = "Scala"
    DART = "Dart"
    ELIXIR = "Elixir"
    ERLANG = "Erlang"
    # ===== OTHERS =====
    R = "R"
    MATLAB = "MATLAB"
    PERL = "Perl"
    HASKELL = "Haskell"
    CANGJIE = "Cangjie"  # Supported on LeetCode China[citation:2][citation:6]
    Other = "other"

class Complexity(Enum):
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINEAR_LOG = "O(n log n)"
    QUADRATIC = "O(n²)"
    CUBIC = "O(n³)"
    EXPONENTIAL = "O(2ⁿ)"
    FACTORIAL = "O(n!)"

class Attempt(Base):
    __tablename__ = 'attempts'
    id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"))
    used_language: Mapped[Language] = mapped_column(SQLAlchemyEnum(Language))
    code_source: Mapped[str] = mapped_column()
    attempted_at: Mapped[datetime] = mapped_column()
    time_complexity: Mapped[Complexity] = mapped_column(SQLAlchemyEnum(Complexity))
    space_complexity: Mapped[Complexity] = mapped_column(SQLAlchemyEnum(Complexity))
    status: Mapped[Status] = mapped_column(SQLAlchemyEnum(Status))
    problem: Mapped["Problem"] = relationship(back_populates="attempts")



