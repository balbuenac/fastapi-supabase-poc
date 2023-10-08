import bcrypt
from fastapi import FastAPI
from app.models import User
from db.supabase import create_supabase_client

app = FastAPI()

# Initialize supabase client
supabase = create_supabase_client()

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

# Create a new user
@app.post("/user")
def create_user(user: User):
    try:
        # Convert email to lowercase
        user_email = user.email.lower()
        # Hash password
        hased_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

        # Check if user already exists
        if user_exists(value=user_email):
            return {"message": "User already exists"}

        # Add user to users table
        print(user.name, user_email, hased_password)
        user = supabase.from_("users")\
            .insert({"name": user.name, "email": user_email, "password": str(hased_password)})\
            .execute()

        # Check if user was added
        if user:
            return {"message": "User created successfully"}
        else:
            return {"message": "User creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "User creation failed"}