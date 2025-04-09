import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface UserProfile {
  first_name: string;
  last_name: string;
  email: string;
  // Add other profile fields if needed
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  // Update this URL to your backend's profile endpoint
  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

  getProfile(): Observable<UserProfile> {
    // Token will be attached automatically by the TokenInterceptor
    return this.http.get<UserProfile>(`${this.baseUrl}/profile`);
  }
}