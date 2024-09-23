from firebase_admin import auth, credentials
import firebase_admin
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException


class FirebaseAuth:
    def __init__(self) -> None:
        cred = credentials.Certificate('keyFirebase.json')
        firebase_admin.initialize_app(cred, {
    'storageBucket': 'fluttereatsily.appspot.com'
})

    def verify_firebase_token(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            token = credentials.credentials
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
