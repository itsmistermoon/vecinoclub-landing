const reduceButtonMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
document.addEventListener('click', (event) => {
  const button = event.target.closest('.btn, .reward-rotation-toggle');
  if (!button || button.matches(':disabled') || reduceButtonMotion.matches) return;
  let label = button.querySelector('.btn-label');
  if (!label) {
    const text = [...button.childNodes].filter((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim());
    if (!text.length) return;
    label = document.createElement('span');
    label.className = 'btn-label';
    text[0].replaceWith(label);
    label.append(...text);
  }
  label.animate(
    [{ opacity: 0, transform: 'translateY(4px)', filter: 'blur(3px)' }, { opacity: 1, transform: 'none', filter: 'blur(0)' }],
    { duration: 220, easing: 'cubic-bezier(.2,.75,.25,1)' }
  );
});
