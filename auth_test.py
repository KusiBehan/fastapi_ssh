from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import requests

# Assuming you already have the token from the previous request
# Replace 'your_access_token' with the actual token you retrieved
def request_user_data(access_token: str):
    # Endpoint URL
    url = "http://10.3.32.18:3000/users/me"
    
# Headers with Bearer Token Authorization
    headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
    }

# Disable SSL verification (use caution; only for trusted endpoints)
    response = requests.get(url, headers=headers, verify=False)

# Check response
    if response.status_code == 200:
    # Successfully retrieved data
        return response.json()
    else:
        print(f"Failed to retrieve user data, status code: {response.status_code}")
        print("Response:", response.text)

# Define the token URL for OAuth2 (typically "/token" if using OAuth2 token endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key and algorithm for JWT token verification (make sure to replace with your key and algorithm)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userdata = request_user_data(access_token=token)
        user_id = userdata.get('user_id')
        return user_id
        # Extract user info if needed, e.g., user_id or email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )