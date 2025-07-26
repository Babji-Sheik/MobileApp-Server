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
def get_username_by_id(user_id: int) -> str:
    try:
        response = supabase.table("users").select("username").eq("id", user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]["username"]
    except Exception as e:
        print(f"[ERROR] Failed to fetch username for {user_id}: {e}")
    return "unknown"  # 👈 important fallback



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
        .select("*")
        .or_(f"to_id.eq.{user_id},from_id.eq.{user_id}")
        .order("timestamp", desc=False)
        .execute()
    )
    msgs = res.data or []

    for m in msgs:
        m["from_username"] = get_username_by_id(m["from_id"])
        m["to_username"] = get_username_by_id(m["to_id"])

    return msgs



def create_message(from_user_id: int, msg: MessageCreate):
    # Step 1: Prepare payload
    payload = {
        "from_id": from_user_id,
        "to_id": msg.to_id,
        "payload": msg.payload,
        "nonce": msg.nonce,
    }

    # Step 2: Insert into Supabase
    res = supabase.from_("messages").insert(payload).execute()

    # Step 3: Validate insertion
    rows = res.data or []
    if not rows:
        raise Exception(f"Message insert failed (status {res.status_code})")

    m = rows[0]

    # Step 4: Resolve sender username (reliable fallback)
    sender_username = get_username_by_id(from_user_id)  # Recommended over get_user_by_username
    to_username = get_username_by_id(msg.to_id)

    # Step 5: Construct return message object
    return {
        "id":            m.get("id"),
        "from_id":       m.get("from_id"),
        "to_id":         m.get("to_id"),
        "payload":       m.get("payload"),
        "nonce":         m.get("nonce"),
        "timestamp":     m.get("timestamp"),
        "delivered":     m.get("delivered", False),
        "read":          m.get("read", False),
        "from_username": sender_username,
        "to_username": to_username
    }
