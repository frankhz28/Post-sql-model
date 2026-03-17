from math import ceil
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import Session, select

DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 100

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    pages: int
    current_page: int
    per_page: int
    items: list[T]

def sanitize_pagination(page: int = 1, per_page: int = DEFAULT_PER_PAGE):
    page = max(1, int(page or 1))
    per_page = min(MAX_PER_PAGE, max(1,int(per_page or DEFAULT_PER_PAGE)))

    return page, per_page

def paginated_query(
    db: Session,
    model,
    base_query = None,
    page: int = 1,
    per_page : int = DEFAULT_PER_PAGE,
    order_by : Optional[str] = None,
    direction : str = "asc",
    allowed_order : Optional[Dict[str,Any]] = None
):
    page, per_page = sanitize_pagination(page=page,per_page=per_page)
    query = base_query if base_query is not None else select(model)

    total= db.scalar(
        select(func.count()).select_from(query.subquery())
    ) or 0

    if total == 0:
        return {
            "total": 0,
            "pages": 0,
            "current_page": page,
            "per_page": per_page,
            "items": []
        }

    if allowed_order and order_by:
        col = allowed_order.get(order_by, allowed_order.get("id"))
        query = query.order_by(col.desc() if direction == "desc" else col.asc())

        
    items = db.exec(
        query.offset((page - 1) * per_page).limit(per_page)
        ).all()
    
    return PaginatedResponse(
        total=total,
        pages=ceil(total / per_page),
        current_page=page,
        per_page=per_page,
        items=items
    )