import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { authInterceptor } from './interceptors/auth.interceptor';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';

// import { GoogleLoginProvider, SocialAuthServiceConfig, SocialLoginModule, SOCIAL_AUTH_CONFIG } from '@abacritt/angularx-social-login';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideHttpClient(
      withInterceptors([authInterceptor])
    ),
    // {
    //   provide: SOCIAL_AUTH_CONFIG,
    //   useValue: {
    //     autoLogin: false,
    //     providers: [
    //       {
    //         id: GoogleLoginProvider.PROVIDER_ID,
    //         provider: new GoogleLoginProvider(
    //           '870553932901-6ott8e0l3fm8hp1ajfj81ig42ha38166.apps.googleusercontent.com'
    //         )
    //       }
    //     ],
    //     onError: (error: unknown) => {
    //       console.error('Google Sign-In error:', error);
    //     }
    //   } as SocialAuthServiceConfig
    // }
  ]
};


