(function () {
  const modal = document.getElementById('modal');
  const openBtn = document.getElementById('openModal');
  const cancelBtn = document.getElementById('cancelBtn');
  const confirmBtn = document.getElementById('confirmBtn');
  const modalContent = modal.querySelector('.modal-content');
  let lastFocused = null;

  function openModal() {
    lastFocused = document.activeElement;
    modal.setAttribute('aria-hidden', 'false');
    // trap focus
    setTimeout(() => modalContent.focus(), 0);
    document.addEventListener('keydown', onKeyDown);
  }

  function closeModal() {
    modal.setAttribute('aria-hidden', 'true');
    document.removeEventListener('keydown', onKeyDown);
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  function onKeyDown(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      closeModal();
      return;
    }
    if (e.key === 'Tab') {
      // simple focus trap
      const focusables = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      const list = Array.prototype.slice.call(focusables).filter(el => !el.hasAttribute('disabled'));
      const first = list[0];
      const last = list[list.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  openBtn.addEventListener('click', openModal);
  cancelBtn.addEventListener('click', closeModal);
  confirmBtn.addEventListener('click', closeModal);
})();

