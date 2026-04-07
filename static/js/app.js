// Landing page logic — tab switching, form submission, alerts

function switchTab(tab) {
  const signinForm = document.getElementById('form-signin');
  const signupForm = document.getElementById('form-signup');
  const tabSignin = document.getElementById('tab-signin');
  const tabSignup = document.getElementById('tab-signup');

  clearAlert();

  if (tab === 'signin') {
    signinForm.classList.remove('form-hidden');
    signupForm.classList.add('form-hidden');
    tabSignin.classList.add('active');
    tabSignup.classList.remove('active');
  } else {
    signinForm.classList.add('form-hidden');
    signupForm.classList.remove('form-hidden');
    tabSignup.classList.add('active');
    tabSignin.classList.remove('active');
  }
}

function showAlert(message, type = 'error') {
  const el = document.getElementById('alert');
  el.textContent = message;
  el.classList.remove('hidden', 'bg-red-500', 'bg-green-500', 'bg-opacity-20',
    'text-red-300', 'text-green-300', 'border', 'border-red-500', 'border-green-500');

  if (type === 'error') {
    el.classList.add('bg-red-500', 'bg-opacity-20', 'text-red-300', 'border', 'border-red-500');
    el.style.borderColor = 'rgba(239,68,68,0.3)';
  } else {
    el.classList.add('bg-green-500', 'bg-opacity-20', 'text-green-300', 'border', 'border-green-500');
    el.style.borderColor = 'rgba(34,197,94,0.3)';
  }
  el.classList.remove('hidden');
}

function clearAlert() {
  const el = document.getElementById('alert');
  el.classList.add('hidden');
}

function setLoading(btnId, loading, defaultText) {
  const btn = document.getElementById(btnId);
  btn.disabled = loading;
  btn.textContent = loading ? 'Please wait…' : defaultText;
  btn.style.opacity = loading ? '0.7' : '1';
}

async function handleSignin(e) {
  e.preventDefault();
  clearAlert();
  const username = document.getElementById('si-username').value.trim();
  const password = document.getElementById('si-password').value.trim();

  if (!username || !password) {
    showAlert('Please fill in all fields.');
    return;
  }

  setLoading('btn-signin', true, 'Sign In to NovBank');
  try {
    const res = await fetch('/api/signin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (data.success) {
      showAlert('Signing in…', 'success');
      setTimeout(() => { window.location.href = '/dashboard'; }, 600);
    } else {
      showAlert(data.message || 'Sign in failed.');
      setLoading('btn-signin', false, 'Sign In to NovBank');
    }
  } catch (err) {
    showAlert('Network error. Please try again.');
    setLoading('btn-signin', false, 'Sign In to NovBank');
  }
}

async function handleSignup(e) {
  e.preventDefault();
  clearAlert();
  const username = document.getElementById('su-username').value.trim();
  const password = document.getElementById('su-password').value.trim();
  const name = document.getElementById('su-name').value.trim();
  const age = document.getElementById('su-age').value.trim();
  const city = document.getElementById('su-city').value.trim();

  if (!username || !password || !name || !age || !city) {
    showAlert('Please fill in all fields.');
    return;
  }

  setLoading('btn-signup', true, 'Create Account');
  try {
    const res = await fetch('/api/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, name, age, city })
    });
    const data = await res.json();
    if (data.success) {
      showAlert(`Account created! Your account number is ${data.account_number}. Redirecting…`, 'success');
      setTimeout(() => { window.location.href = '/dashboard'; }, 1800);
    } else {
      showAlert(data.message || 'Sign up failed.');
      setLoading('btn-signup', false, 'Create Account');
    }
  } catch (err) {
    showAlert('Network error. Please try again.');
    setLoading('btn-signup', false, 'Create Account');
  }
}
