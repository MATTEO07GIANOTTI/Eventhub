import { Routes } from '@angular/router';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  { path: '', loadComponent: () => import('./features/public/home.component').then(m => m.HomeComponent) },
  { path: 'event/:id', loadComponent: () => import('./features/event-detail/event-detail.component').then(m => m.EventDetailComponent) },
  { path: 'auth/login', loadComponent: () => import('./features/auth/login.component').then(m => m.LoginComponent) },
  { path: 'user/tickets', canActivate: [roleGuard(['user', 'organizer', 'admin'])], loadComponent: () => import('./features/user/tickets.component').then(m => m.TicketsComponent) },
  { path: 'organizer/dashboard', canActivate: [roleGuard(['organizer', 'admin'])], loadComponent: () => import('./features/organizer/dashboard.component').then(m => m.OrganizerDashboardComponent) },
  { path: 'admin/users', canActivate: [roleGuard(['admin'])], loadComponent: () => import('./features/admin/users.component').then(m => m.AdminUsersComponent) }
];
