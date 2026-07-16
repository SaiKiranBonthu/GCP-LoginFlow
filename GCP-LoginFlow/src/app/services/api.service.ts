import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})

export class ApiService {

  private http = inject(HttpClient);
  // private baseUrl = 'http://localhost:8000/api/v1';
  private baseUrl = 'https://marketplace-saas-backend-870553932901.asia-south1.run.app' + '/api/v1';

  signup(token: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/signup`, {
      marketplaceToken: token,
    });
  }

  googleLogin(idToken: string, onboardingSessionId: string| null): Observable<any> {
    return this.http.post(`${this.baseUrl}/auth/google`, {
      idToken: idToken,
      onboardingSessionId: onboardingSessionId,
    });
  }

  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.baseUrl}/auth/me`);
  };
  

  validateOnboardingSession(sessionId: string): Observable<any> {
    return this.http.get(`${this.baseUrl}`+ `/marketplace/onboarding/`+ sessionId);
  }
}
