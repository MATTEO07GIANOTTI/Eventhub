import { Component } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `<form [formGroup]="form"><input formControlName="email" placeholder="Email"/><input type="password" formControlName="password"/><button [disabled]="form.invalid">Login</button></form>`
})
export class LoginComponent {
  form = new FormBuilder().group({ email: ['', [Validators.required, Validators.email]], password: ['', Validators.required] });
}
