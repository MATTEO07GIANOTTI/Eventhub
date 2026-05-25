import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
  <header class="topbar">
    <div class="brand">🎫 EventHub</div>
    <nav>
      <a routerLink="/">Home</a>
      <a routerLink="/auth/login">Login</a>
      <a routerLink="/user/tickets">Biglietti</a>
      <a routerLink="/organizer/dashboard">Dashboard</a>
    </nav>
  </header>
  <main class="page"><router-outlet /></main>
  `,
  styles: [`
    :host { font-family: Inter, system-ui, -apple-system, sans-serif; color: #0f172a; }
    .topbar { display:flex; justify-content:space-between; align-items:center; padding: 1rem 1.25rem; background: rgba(15,23,42,.95); color:#fff; position: sticky; top: 0; z-index: 20; }
    .brand { font-weight: 800; letter-spacing: .3px; }
    nav a { color:#cbd5e1; text-decoration:none; margin-left:1rem; font-weight:600; }
    nav a:hover { color:#fff; }
    .page { padding: 1.2rem; background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%); min-height: calc(100vh - 72px); }
  `]
})
export class AppComponent {}
