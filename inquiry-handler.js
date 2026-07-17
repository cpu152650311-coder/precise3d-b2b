async function handleInquiry(event) {
  event.preventDefault();
  const form = event.target;
  const data = {
    name: form.querySelector('[name="name"]')?.value || '',
    email: form.querySelector('[name="email"]')?.value || '',
    message: form.querySelector('[name="message"]')?.value || '',
    source: 'ems-3dp.com',
  };
  try {
    const res = await fetch('https://inquiry-proxy.cpu152650311.workers.dev/inquiry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const result = await res.json();
    if (result.success) {
      alert('Thank you! Your inquiry has been received. We will respond within 24 hours.');
      form.reset();
      if (typeof closeModal === 'function') closeModal();
    } else {
      alert(result.message || 'Submission failed. Please try again.');
    }
  } catch {
    alert('Network error. Please try again later.');
  }
  return false;
}
