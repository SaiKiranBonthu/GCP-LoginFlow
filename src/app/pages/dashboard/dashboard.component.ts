import { Component,OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})

export class DashboardComponent implements OnInit {

 private apiService = inject( ApiService );
 private authService = inject( AuthService );
 private router = inject( Router );

 user: any = null;
 isLoading = true;
 errorMessage = '';

 ngOnInit(): void {
   this.loadCurrentUser();
 }

 loadCurrentUser(): void {
   this.apiService
     .getCurrentUser()
     .subscribe({
       next: (response) => {
         this.user =
           response.user;
         this.isLoading =
           false;
       },
       error: (error) => {
         console.error(
           'Unable to load user:',
           error
         );

         this.isLoading =
           false;

         this.errorMessage =
           'Your session is invalid '
           + 'or has expired.';

         this.authService
           .logout();

         this.router.navigate(
           ['/signin']
         );
       }
     });
 }

 logout(): void {
   this.authService
     .logout();

   this.router.navigate(
     ['/signin']
   );
 }
}