// import { Component, OnInit, inject } from '@angular/core';
// import { ActivatedRoute, RouterLink } from '@angular/router';
// import { CommonModule } from '@angular/common';

// @Component({
//  selector: 'app-signup',
//  standalone: true,
//  imports: [CommonModule, RouterLink],
//  templateUrl: './signup.component.html',
//  styleUrl: './signup.component.scss'
// })

// export class SignupComponent implements OnInit {
//  private route = inject( ActivatedRoute );
//  onboardingSession = '';

//  ngOnInit(): void {
//    this.onboardingSession = this.route.snapshot.queryParamMap.get('session')?? '';

//    if ( this.onboardingSession ) {
//      sessionStorage.setItem( 'marketplace_onboarding_session', this.onboardingSession );
//    } 

//    console.log('Onboarding session:',this.onboardingSession);
//  }
// }


import { CommonModule, isPlatformBrowser} from '@angular/common';
import { Component,OnInit,inject, PLATFORM_ID } from '@angular/core';
import { ActivatedRoute,RouterLink } from '@angular/router';
import { ApiService } from '../../services/api.service';

@Component({
 selector: 'app-signup',
 standalone: true,
 imports: [CommonModule,RouterLink],
 templateUrl: './signup.component.html',
 styleUrl:'./signup.component.scss'
})

export class SignupComponent implements OnInit {

 private route = inject(ActivatedRoute);

 private apiService = inject(ApiService);

 private platformId = inject(PLATFORM_ID);

 onboardingSession = '';
 procurementAccountId = '';
 isLoading = true;
 isSessionValid = false;
 errorMessage = '';

 ngOnInit(): void {
   this.onboardingSession = (this.route.snapshot.queryParamMap.get('session')?? '');

   if (!this.onboardingSession) {
     this.isLoading = false;
     this.errorMessage = ('Marketplace onboarding session is missing.');
     return;
   }

   if(isPlatformBrowser(this.platformId)) {
     sessionStorage.setItem('marketplace_onboarding_session',this.onboardingSession);
   }


   this.validateSession();
 }

 private validateSession(): void {
   this.apiService.validateOnboardingSession(this.onboardingSession)
     .subscribe({
       next: (response) => {
         this.isLoading = false;
         this.isSessionValid = (response.valid);

         this.procurementAccountId = (response.marketplaceAccount.procurementAccountId);

         console.log('Marketplace account:',this.procurementAccountId);
       },

       error: (error) => {
         console.error('Onboarding session validation failed:',error);

         this.isLoading = false;
         this.isSessionValid = false;

         if(isPlatformBrowser(this.platformId)) {
           sessionStorage.removeItem('marketplace_onboarding_session');
         }


         this.errorMessage = (
           error.error?.detail
           ??
           'The Marketplace onboarding session is invalid or has expired.'
         );
       }
     });
 }
}