// Auto-dismiss messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    document.querySelectorAll('.message').forEach(el => {
      el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-6px)';
      setTimeout(() => el.remove(), 400);
    });
  }, 4000);
});

// Live avatar preview on file select
document.addEventListener('change', (e) => {
  if (e.target && e.target.matches('input[type="file"][name="profile_image"]')) {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const avatar = document.querySelector('.current-avatar, .welcome-avatar');
      if (avatar) avatar.innerHTML = `<img src="${ev.target.result}" style="width:100%;height:100%;object-fit:cover;">`;
    };
    reader.readAsDataURL(file);
  }
});
