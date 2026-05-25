import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  role$ = new BehaviorSubject<string | null>(localStorage.getItem('role'));

  saveSession(accessToken: string, role: string) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('role', role);
    this.role$.next(role);
  }

  logout() {
    localStorage.clear();
    this.role$.next(null);
  }
}
