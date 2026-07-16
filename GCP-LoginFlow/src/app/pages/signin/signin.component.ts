import { Component, OnDestroy, OnInit, inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { Router } from '@angular/router';
// import {
//  GoogleSigninButtonModule,
//  SocialAuthService,
//  SocialUser
// } from '@abacritt/angularx-social-login';
import { Subject, takeUntil } from 'rxjs';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';

@Component({
 selector: 'app-signin',
 standalone: true,
 imports: [
   CommonModule,
  //  GoogleSigninButtonModule
 ],
 templateUrl: './signin.component.html',
 styleUrl: './signin.component.scss'
})


export class SigninComponent implements OnInit, OnDestroy {

//  private socialAuthService = inject(SocialAuthService);
 private apiService = inject(ApiService);
 private router = inject(Router);
 private authService = inject(AuthService);
 private platformId = inject(PLATFORM_ID)


 private destroy$ = new Subject<void>();
 isLoading = false;
 errorMessage = '';

 ngOnInit(): void {
  //  this.socialAuthService.authState
  //    .pipe(takeUntil(this.destroy$))
  //    .subscribe({
  //      next: (googleUser: SocialUser) => {
  //        if (!googleUser?.idToken) {
  //          return;
  //        }
  //        console.log(
  //          'Google user authenticated:',
  //          googleUser.email
  //        );
  //        this.loginToBackend(googleUser.idToken);
  //      },
  //      error: (error) => {
  //        console.error(
  //          'Google authentication error:',
  //          error
  //        );
  //        this.errorMessage =
  //          'Google Sign-In failed. Please try again.';
  //      }
  //    });
 }

 private loginToBackend(
   googleIdToken: string
 ): void {
   this.isLoading = true;
   this.errorMessage = '';

   let onboardingSessionId: string | null = null;

   if(isPlatformBrowser(this.platformId)){
     onboardingSessionId = sessionStorage.getItem('marketplace_onboarding_session');
   }


   this.apiService
     .googleLogin(googleIdToken, onboardingSessionId)
     .subscribe({
       next: (response) => {
         console.log(
           'Backend authentication response:',
           response
         );

         this.authService.saveToken(response.accessToken);
         
         this.isLoading = false;
         this.router.navigate(['/dashboard']);
       },
       error: (error) => {
         console.error(
           'Backend authentication failed:',
           error
         );
         this.isLoading = false;
         this.errorMessage =
           error.error?.detail
           ?? 'Authentication failed.';
       }
     });
 }

 ngOnDestroy(): void {
   this.destroy$.next();
   this.destroy$.complete();
 }
}