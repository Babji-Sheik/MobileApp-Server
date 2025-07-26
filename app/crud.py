# app/crud.py

from .supabase_client import supabase
from passlib.context import CryptContext
from .schemas import UserCreate, MessageCreate

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username: str):
    res = (
        supabase
        .from_("users")
        .select("*")
        .eq("username", username)
        .execute()
    )
    rows = res.data or []
    return rows[0] if rows else None


def create_user(user_in: UserCreate):
    hashed = pwd_ctx.hash(user_in.password)
    payload = {
        "username": user_in.username,
        "password_hash": hashed,
    }
    res = supabase.from_("users").insert(payload).execute()
    rows = res.data or []
    if not rows:
        raise Exception(f"User creation failed (status {res.status_code})")
    return rows[0]


def get_messages_for_user(user_id: int):
    res = (
        supabase
        .from_("messages")
        .select("*, users!messages_from_id_fkey(username)")
        .or_(f"to_id.eq.{user_id},from_id.eq.{user_id}")
        .order("timestamp", desc=False)  # use your actual column
        .execute()
    )
    msgs = res.data or []
    return [
        {
            **m,
            "from_username": (
                m.get("users", {}).get("username")
                if isinstance(m.get("users"), dict)
                else str(m.get("from_id"))
            ),
        }
        for m in msgs
    ]


def create_message(from_user_id: int, msg: MessageCreate):
    payload = {
        "from_id": from_user_id,
        "to_id":   msg.to_id,
        "payload": msg.payload,
        "nonce":   msg.nonce,
    }
    # Insert message
    res = supabase.from_("messages").insert(payload).execute()
    rows = res.data or []
    if not rows:
        raise Exception(f"Message insert failed (status {res.status_code})")

    m = rows[0]
    # Look up sender username manually
    user = get_user_by_username(msg.username if hasattr(msg, 'username') else None)
    sender_username = user.get('username') if user else str(from_user_id)

    # Build return dict matching MessageOut schema
    return {
        "id":            m.get("id"),
        "from_id":       m.get("from_id"),
        "to_id":         m.get("to_id"),
        "payload":       m.get("payload"),
        "nonce":         m.get("nonce"),
        "timestamp":     m.get("timestamp"),
        "delivered":     m.get("delivered"),
        "read":          m.get("read"),
        "from_username": sender_username,
    }
