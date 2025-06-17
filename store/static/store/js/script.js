// ✅ Theme toggle
document.getElementById("themeToggle")?.addEventListener("change", function () {
  document.body.classList.toggle("dark-theme");
});

// ✅ Toggle sensitive account info
document.getElementById("toggleAccount")?.addEventListener("click", function () {
  const infoFields = document.querySelectorAll(".account-info p");
  infoFields.forEach(p => {
    if (p.dataset.original) {
      p.textContent = p.dataset.original;
      delete p.dataset.original;
    } else {
      p.dataset.original = p.textContent;
      p.textContent = "••••••••";
    }
  });

  const icon = this.querySelector("i");
  icon.classList.toggle("fa-eye-slash");
  icon.classList.toggle("fa-eye");
});

// ✅ Particle background animation
const canvas = document.createElement("canvas");
canvas.id = "background";
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");
let particles = [];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeCanvas);
resizeCanvas();

function createParticles() {
  particles = [];
  for (let i = 0; i < 60; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 4 + 1,
      dx: (Math.random() - 0.5) * 2,
      dy: (Math.random() - 0.5) * 2
    });
  }
}

function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let p of particles) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff22";
    ctx.fill();
    p.x += p.dx;
    p.y += p.dy;

    if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
    if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
  }
  requestAnimationFrame(animateParticles);
}

createParticles();
animateParticles();

