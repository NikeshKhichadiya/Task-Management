import { Component, OnInit } from '@angular/core';
import { UserService, UserProfile } from '../../../services/user/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: UserProfile | null = null;
  loading = false;
  errorMessage = '';

  constructor(
    private userService: UserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loading = true;
    this.userService.getProfile().subscribe({
      next: (data) => {
        this.user = data;
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Failed to load user profile.';
        this.loading = false;
      }
    });
  }

  // Call this method when the logout button is clicked
  logout(): void {
    // For example, clear any stored authentication tokens or data
    localStorage.removeItem('authToken');

    // Optionally, you can clear other user data here
    // For example: localStorage.removeItem('userData');

    // Navigate to the login page or landing page
    this.router.navigate(['/login']);
  }
}
