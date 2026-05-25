import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-home',
  imports: [CommonModule, FormsModule],
  template: `
  <section class="hero">
    <div>
      <p class="chip">Piattaforma eventi culturali</p>
      <h1>Scopri, prenota e vivi i migliori eventi della tua città.</h1>
      <p class="sub">Concerti, workshop e presentazioni libri in un'unica esperienza moderna.</p>
    </div>
  </section>

  <section class="filters">
    <input [(ngModel)]="city" placeholder="Filtra per città" />
    <input [(ngModel)]="category" placeholder="Filtra per categoria" />
    <input [(ngModel)]="maxPrice" type="number" placeholder="Prezzo max" />
  </section>

  <section class="cards">
    <article *ngFor="let e of filteredEvents()" class="card">
      <div class="badge">{{ e.category }}</div>
      <h3>{{ e.title }}</h3>
      <p>📍 {{ e.city }} · {{ e.date }}</p>
      <p class="price">€ {{ e.price }}</p>
      <button>Dettagli evento</button>
    </article>
  </section>
  `,
  styles: [`
    .hero{background: radial-gradient(circle at 20% 20%, #60a5fa 0%, #4f46e5 45%, #0f172a 100%); color:#fff; padding:2rem; border-radius:1.2rem; box-shadow: 0 20px 40px rgba(79,70,229,.3)}
    h1{margin:.4rem 0 0; font-size:clamp(1.6rem,3vw,2.4rem); max-width:800px}
    .sub{opacity:.92; margin-top:.6rem}
    .chip{display:inline-block;background:rgba(255,255,255,.2);padding:.25rem .75rem;border-radius:999px;font-size:.85rem}
    .filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:.8rem;margin:1.2rem 0}
    input{padding:.7rem .8rem;border:1px solid #cbd5e1;border-radius:.7rem}
    .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem}
    .card{background:#fff; border:1px solid #e2e8f0; border-radius:1rem; padding:1rem; box-shadow:0 10px 30px rgba(15,23,42,.06)}
    .badge{display:inline-block;background:#dbeafe;color:#1e3a8a;padding:.2rem .55rem;border-radius:999px;font-size:.75rem;font-weight:700}
    .price{font-size:1.15rem;font-weight:800;color:#0f172a}
    button{background:#4f46e5;color:#fff;border:none;padding:.55rem .85rem;border-radius:.6rem;cursor:pointer}
  `]
})
export class HomeComponent {
  city = '';
  category = '';
  maxPrice: number | null = null;

  events = [
    { title: 'Concerto Jazz sotto le Stelle', city: 'Roma', category: 'Concerto', date: '12 Giugno', price: 15 },
    { title: 'Workshop di Fotografia Urbana', city: 'Milano', category: 'Workshop', date: '21 Giugno', price: 25 },
    { title: 'Presentazione libro: Nuove Visioni', city: 'Torino', category: 'Libri', date: '3 Luglio', price: 0 }
  ];

  filteredEvents() {
    return this.events.filter(e =>
      (!this.city || e.city.toLowerCase().includes(this.city.toLowerCase())) &&
      (!this.category || e.category.toLowerCase().includes(this.category.toLowerCase())) &&
      (this.maxPrice === null || this.maxPrice === undefined || e.price <= this.maxPrice)
    );
  }
}
