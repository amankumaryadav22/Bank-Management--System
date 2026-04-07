// Dashboard logic — load data, handle banking actions, modals

// ─── State ──────────────────────────────────────────
let currentBalance = 0;

// ─── Init ────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    loadTransactions();
});

// ─── Data Loading ────────────────────────────────────
async function loadDashboard() {
    try {
        const res = await fetch('/api/dashboard');
        if (res.status === 401) { window.location.href = '/'; return; }
        const data = await res.json();
        if (!data.success) return;

        currentBalance = data.balance;

        // Sidebar
        document.getElementById('sidebar-name').textContent = data.name || data.username;
        document.getElementById('sidebar-acno').textContent = 'Acc: ' + data.account_number;

        // Greeting
        document.getElementById('greeting-name').textContent = (data.name || data.username).split(' ')[0];

        // Balance card
        document.getElementById('balance-display').textContent = formatCurrency(data.balance);
        document.getElementById('acno-display').textContent = data.account_number;

        // Info card
        document.getElementById('info-name').textContent = data.name;
        document.getElementById('info-city').textContent = data.city;
        document.getElementById('info-age').textContent = data.age + ' yrs';
    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

async function loadTransactions() {
    try {
        const res = await fetch('/api/transactions');
        if (res.status === 401) { window.location.href = '/'; return; }
        const data = await res.json();
        if (!data.success) return;

        renderRecentTxns(data.transactions.slice(0, 5));
        renderAllTxns(data.transactions);
    } catch (err) {
        console.error('Transaction load error:', err);
    }
}

// ─── Rendering ───────────────────────────────────────
function formatCurrency(amount) {
    return '₹ ' + Number(amount).toLocaleString('en-IN');
}

function badgeClass(remarks) {
    const r = (remarks || '').toLowerCase();
    if (r.includes('deposit')) return 'badge badge-deposit';
    if (r.includes('withdraw')) return 'badge badge-withdraw';
    return 'badge badge-transfer';
}

function formatDate(dateStr) {
    try {
        return new Date(dateStr).toLocaleString('en-IN', {
            day: '2-digit', month: 'short', year: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    } catch { return dateStr; }
}

function txnRow(t) {
    return `<tr>
    <td class="td-date">${formatDate(t.date)}</td>
    <td><span class="${badgeClass(t.remarks)}"><span class="badge-dot"></span>${t.remarks}</span></td>
    <td class="td-acno">${t.account_number}</td>
    <td class="td-amount">${formatCurrency(t.amount)}</td>
  </tr>`;
}

function renderRecentTxns(txns) {
    const el = document.getElementById('recent-txn-body');
    if (!txns || txns.length === 0) {
        el.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#9ca3af;padding:32px">No transactions yet.</td></tr>';
        return;
    }
    el.innerHTML = txns.map(txnRow).join('');
}

function renderAllTxns(txns) {
    const el = document.getElementById('all-txn-body');
    if (!txns || txns.length === 0) {
        el.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#9ca3af;padding:32px">No transactions yet.</td></tr>';
        return;
    }
    el.innerHTML = txns.map(txnRow).join('');
}

// ─── Section Navigation ──────────────────────────────
function showSection(name) {
    document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
    document.getElementById('section-' + name).classList.add('active');

    document.querySelectorAll('.nav-link').forEach(btn => btn.classList.remove('active'));
    const activeNav = document.getElementById('nav-' + name);
    if (activeNav) activeNav.classList.add('active');
}

// ─── Modals ──────────────────────────────────────────
function openModal(type) {
    document.getElementById('modal-' + type).classList.add('open');
    clearModalAlert(type);
    const amtInput = document.getElementById(type + '-amount');
    if (amtInput) { amtInput.value = ''; setTimeout(() => amtInput.focus(), 50); }
    if (type === 'transfer') {
        const acnoInput = document.getElementById('transfer-acno');
        if (acnoInput) acnoInput.value = '';
    }
}

function closeModal(type) {
    document.getElementById('modal-' + type).classList.remove('open');
}

function showModalAlert(type, message, isSuccess) {
    const el = document.getElementById(type + '-alert');
    el.textContent = message;
    el.className = 'modal-alert ' + (isSuccess ? 'success' : 'error');
}

function clearModalAlert(type) {
    const el = document.getElementById(type + '-alert');
    if (el) { el.textContent = ''; el.className = 'modal-alert'; }
}

function setLoading(btnId, loading, defaultText) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.disabled = loading;
    btn.textContent = loading ? 'Processing…' : defaultText;
}

// ─── Banking Actions ─────────────────────────────────
async function handleDeposit() {
    const amount = parseInt(document.getElementById('deposit-amount').value, 10);
    if (!amount || amount <= 0) { showModalAlert('deposit', 'Please enter a valid amount.', false); return; }

    setLoading('btn-deposit', true, 'Deposit');
    try {
        const res = await fetch('/api/deposit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ amount }) });
        const data = await res.json();
        if (data.success) {
            currentBalance = data.balance;
            document.getElementById('balance-display').textContent = formatCurrency(data.balance);
            showModalAlert('deposit', '✓ ' + data.message + ' New balance: ' + formatCurrency(data.balance), true);
            await loadTransactions();
            setTimeout(() => closeModal('deposit'), 2000);
        } else {
            showModalAlert('deposit', data.message || 'Deposit failed.', false);
        }
    } catch { showModalAlert('deposit', 'Network error. Try again.', false); }
    setLoading('btn-deposit', false, 'Deposit');
}

async function handleWithdraw() {
    const amount = parseInt(document.getElementById('withdraw-amount').value, 10);
    if (!amount || amount <= 0) { showModalAlert('withdraw', 'Please enter a valid amount.', false); return; }

    setLoading('btn-withdraw', true, 'Withdraw');
    try {
        const res = await fetch('/api/withdraw', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ amount }) });
        const data = await res.json();
        if (data.success) {
            currentBalance = data.balance;
            document.getElementById('balance-display').textContent = formatCurrency(data.balance);
            showModalAlert('withdraw', '✓ ' + data.message + ' New balance: ' + formatCurrency(data.balance), true);
            await loadTransactions();
            setTimeout(() => closeModal('withdraw'), 2000);
        } else {
            showModalAlert('withdraw', data.message || 'Withdrawal failed.', false);
        }
    } catch { showModalAlert('withdraw', 'Network error. Try again.', false); }
    setLoading('btn-withdraw', false, 'Withdraw');
}

async function handleTransfer() {
    const account_number = parseInt(document.getElementById('transfer-acno').value, 10);
    const amount = parseInt(document.getElementById('transfer-amount').value, 10);
    if (!account_number || !amount || amount <= 0) {
        showModalAlert('transfer', 'Please enter a valid account number and amount.', false);
        return;
    }

    setLoading('btn-transfer', true, 'Transfer');
    try {
        const res = await fetch('/api/transfer', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ account_number, amount }) });
        const data = await res.json();
        if (data.success) {
            currentBalance = data.balance;
            document.getElementById('balance-display').textContent = formatCurrency(data.balance);
            showModalAlert('transfer', '✓ ' + data.message + ' New balance: ' + formatCurrency(data.balance), true);
            await loadTransactions();
            setTimeout(() => closeModal('transfer'), 2000);
        } else {
            showModalAlert('transfer', data.message || 'Transfer failed.', false);
        }
    } catch { showModalAlert('transfer', 'Network error. Try again.', false); }
    setLoading('btn-transfer', false, 'Transfer');
}

// ─── Sign Out ────────────────────────────────────────
async function handleSignout() {
    try { await fetch('/api/signout', { method: 'POST' }); } finally { window.location.href = '/'; }
}
