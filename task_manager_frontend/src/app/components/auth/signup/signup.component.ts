import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService, SignupData } from '../../../services/auth/auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnInit {
  signupForm!: FormGroup;
  submitted = false;
  loading = false;
  errorMessage = '';
  successMessage = '';

  constructor(private fb: FormBuilder, private authService: AuthService) { }

  ngOnInit(): void {
    this.signupForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    this.submitted = true;
    this.errorMessage = '';
    this.successMessage = '';

    if (this.signupForm.valid) {
      const signupData: SignupData = this.signupForm.value;
      this.loading = true;
      this.authService.signup(signupData).subscribe({
        next: (res: any) => {
          this.loading = false;
          this.successMessage = 'Signup successful! Please check your email or login to continue.';
          this.signupForm.reset();
          this.submitted = false;
        },
        error: (err: any) => {
          this.loading = false;
          this.errorMessage = err.error?.message || 'Signup failed. Please try again later.';
        }
      });
    }
  }
}
