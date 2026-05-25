import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const roleGuard = (allowed: string[]): CanActivateFn => {
  return () => {
    const role = localStorage.getItem('role');
    if (role && allowed.includes(role)) return true;
    return inject(Router).parseUrl('/auth/login');
  };
};
