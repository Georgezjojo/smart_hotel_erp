// ============================================
// Hotel ERP – Main JavaScript
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  // ==================== SEARCH ====================
  const searchInput = document.getElementById('headerSearch');
  const searchButton = document.getElementById('searchButton');
  function doSearch() {
    if (!searchInput) return;
    const query = searchInput.value.trim();
    if (query.length > 0) {
      window.location.href = `/search/?q=${encodeURIComponent(query)}`;
    }
  }
  if (searchButton) {
    searchButton.addEventListener('click', doSearch);
  }
  if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') doSearch();
    });
  }

  // ==================== ADD BOOKING MODAL ====================
  const modal = document.getElementById('addBookingModal');
  const openBtn = document.getElementById('openAddBookingModal');
  const closeBtn = document.getElementById('closeAddBookingModal');

  if (openBtn && modal) {
    openBtn.addEventListener('click', () => modal.classList.remove('hidden'));
    if (closeBtn) {
      closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
    }
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.add('hidden');
    });
  }

  // Foreign / Local toggle inside the modal
  const guestType = document.getElementById('guestType');
  const localFields = document.getElementById('localFields');
  const foreignFields = document.getElementById('foreignFields');
  if (guestType && localFields && foreignFields) {
    guestType.addEventListener('change', () => {
      if (guestType.value === 'foreign') {
        localFields.classList.add('hidden');
        foreignFields.classList.remove('hidden');
      } else {
        localFields.classList.remove('hidden');
        foreignFields.classList.add('hidden');
      }
    });
  }

  // AJAX form submission for Add Booking
  const bookingForm = document.getElementById('addBookingForm');
  if (bookingForm) {
    bookingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(bookingForm);
      try {
        const response = await fetch(bookingForm.action, {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (response.ok) {
          const data = await response.json();
          showToast(data.message || 'Reservation created!', 'success');
          modal.classList.add('hidden');
          bookingForm.reset();
        } else {
          const errorText = await response.text();
          showToast('Error: ' + errorText, 'error');
        }
      } catch (err) {
        showToast('Network error', 'error');
      }
    });
  }

  // ==================== SLIDE PANEL (kept for future use) ====================
  const slidePanel = document.getElementById('slidePanel');
  const closeSlide = document.getElementById('closeSlidePanel');

  function openSlidePanel() {
    if (!slidePanel) return;
    slidePanel.classList.remove('translate-x-full');
    slidePanel.classList.add('translate-x-0');
    loadNotifications();
  }

  function closeSlidePanel() {
    if (!slidePanel) return;
    slidePanel.classList.add('translate-x-full');
    slidePanel.classList.remove('translate-x-0');
  }

  if (closeSlide) closeSlide.addEventListener('click', closeSlidePanel);

  // Close panel when clicking outside
  document.addEventListener('click', (e) => {
    if (!slidePanel) return;
    if (!slidePanel.contains(e.target) && e.target !== notificationBell) {
      closeSlidePanel();
    }
  });

  async function loadNotifications() {
    const list = document.getElementById('notificationsList');
    if (!list) return;
    list.innerHTML = '<p class="text-sm text-slate-500 text-center">Loading...</p>';
    try {
      const res = await fetch('/notifications/api/notifications/');
      if (res.ok) {
        const data = await res.json();
        if (data.length === 0) {
          list.innerHTML = '<div class="text-center text-slate-400 py-4"><i class="fa-solid fa-bell-slash text-2xl mb-2"></i><p class="text-sm">No notifications</p></div>';
          return;
        }
        list.innerHTML = data.map(n =>
          `<div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg text-sm ${n.is_read ? '' : 'border-l-4 border-primary'}">
            <p>${n.message}</p>
            <span class="text-xs text-slate-400">${new Date(n.created_at).toLocaleString()}</span>
          </div>`
        ).join('');
      } else {
        list.innerHTML = '<p class="text-sm text-rose-500">Failed to load notifications.</p>';
      }
    } catch (err) {
      list.innerHTML = '<p class="text-sm text-rose-500">Could not load notifications.</p>';
    }
  }

  // Make globally available (not needed by sidebar now, but keep it)
  window.loadNotifications = loadNotifications;

  // ==================== NOTIFICATION BELL -> Full Notifications Page ====================
  const notificationBell = document.getElementById('notificationBell');
  if (notificationBell) {
    notificationBell.addEventListener('click', () => {
      window.location.href = '/notifications/list/';
    });
  }

  // ==================== USER DROPDOWN ====================
  const userMenuBtn = document.getElementById('userMenuButton');
  const userDropdown = document.getElementById('userDropdown');

  if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('hidden');
    });
    document.addEventListener('click', (e) => {
      if (!userDropdown.contains(e.target) && e.target !== userMenuBtn) {
        userDropdown.classList.add('hidden');
      }
    });
  }

  // Dropdown -> Settings / Notifications now go to dedicated pages
  const dropdownSettingsBtn = document.getElementById('dropdownSettingsBtn');
  const dropdownNotificationsBtn = document.getElementById('dropdownNotificationsBtn');

  if (dropdownSettingsBtn) {
    dropdownSettingsBtn.addEventListener('click', () => {
      userDropdown.classList.add('hidden');
      window.location.href = '/settings/';
    });
  }
  if (dropdownNotificationsBtn) {
    dropdownNotificationsBtn.addEventListener('click', () => {
      userDropdown.classList.add('hidden');
      window.location.href = '/notifications/list/';
    });
  }

  // ==================== DARK MODE ====================
  const html = document.documentElement;
  const darkIcon = document.getElementById('darkIcon');
  const slideDarkToggle = document.getElementById('slideDarkToggle');

  function updateDarkUI() {
    const isDark = html.classList.contains('dark');
    if (slideDarkToggle) {
      slideDarkToggle.querySelector('span').style.transform = isDark ? 'translateX(100%)' : 'translateX(0)';
    }
    if (darkIcon) {
      darkIcon.className = isDark ? 'fa-solid fa-sun text-lg' : 'fa-solid fa-moon text-lg';
    }
  }

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') html.classList.add('dark');
  updateDarkUI();

  const darkToggle = document.getElementById('darkToggle');
  if (darkToggle) {
    darkToggle.addEventListener('click', () => {
      html.classList.toggle('dark');
      localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
      updateDarkUI();
    });
  }

  if (slideDarkToggle) {
    slideDarkToggle.addEventListener('click', () => {
      html.classList.toggle('dark');
      localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
      updateDarkUI();
    });
  }

  // ==================== NOTIFICATION BELL DOT ====================
  const bellDot = document.getElementById('notificationDot');
  if (bellDot) {
    fetch('/notifications/api/notifications/?unread=1')
      .then(res => res.json())
      .then(data => {
        if (data.length > 0) bellDot.classList.remove('hidden');
      })
      .catch(() => {});
  }

  // ==================== DASHBOARD AUTO‑REFRESH ====================
  if (window.location.pathname === '/dashboard/') {
    setInterval(() => {
      fetch('/dashboard/api/summary/')
        .then(res => res.json())
        .then(data => {
          const setText = (id, text) => {
            const el = document.getElementById(id);
            if (el) el.textContent = text;
          };
          setText('checkinsCount', data.checkins);
          setText('checkoutsCount', data.checkouts);
          setText('occupancyRate', data.occupancy + '%');
          setText('revenueMonth', '₹' + data.revenue);
        })
        .catch(() => {});
    }, 60000);
  }

});

// ==================== GLOBAL TOAST FUNCTION ====================
window.showToast = function (message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const colors = {
    success: 'bg-emerald-500',
    error: 'bg-rose-500',
    warning: 'bg-amber-500',
    info: 'bg-primary'
  };
  const icons = {
    success: 'fa-circle-check',
    error: 'fa-circle-xmark',
    warning: 'fa-triangle-exclamation',
    info: 'fa-circle-info'
  };
  const toast = document.createElement('div');
  toast.className = `${colors[type]} text-white px-4 py-3 rounded-lg shadow-lg flex items-center space-x-2 animate__animated animate__fadeInRight text-sm`;
  toast.innerHTML = `<i class="fa-solid ${icons[type]}"></i><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('animate__fadeOutRight');
    setTimeout(() => toast.remove(), 500);
  }, 4000);
};