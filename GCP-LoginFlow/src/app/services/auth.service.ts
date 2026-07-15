import { Injectable } from '@angular/core';
@Injectable({
 providedIn: 'root'
})
export class AuthService {
 private readonly tokenKey = 'access_token';

 saveToken(token: string): void {
   if (typeof window !== 'undefined') {
     window.localStorage.setItem(
       this.tokenKey,
       token
     );
   }
 }

 getToken(): string | null {
   if (typeof window === 'undefined') {
     return null;
   }
   return window.localStorage.getItem(
     this.tokenKey
   );
 }

 isLoggedIn(): boolean {
   return this.getToken() !== null;
 }

 logout(): void {
   if (typeof window !== 'undefined') {
     window.localStorage.removeItem(
       this.tokenKey
     );
   }
 }
}