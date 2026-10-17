// JavaScript handles interface behavior; Python remains the source of all totals.
const search = document.querySelector('#search');
search.addEventListener('input', () => {
  let visible = 0;
  document.querySelectorAll('.product').forEach(card => {
    card.hidden = !card.dataset.name.includes(search.value.trim().toLowerCase());
    if (!card.hidden) visible++;
  });
  document.querySelector('#no-results').hidden = visible > 0;
});
document.querySelector('#print-receipt')?.addEventListener('click', () => window.print());
