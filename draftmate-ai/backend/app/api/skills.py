from fastapi import APIRouter
from ..services.skills import SKILLS
router=APIRouter(prefix="/api/skills",tags=["skills"])
@router.get("")
def skills(): return SKILLS
