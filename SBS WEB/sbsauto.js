document.addEventListener('DOMContentLoaded', () => {
  // Açılır Menü (Dropdown)
  const dropdownButton = document.querySelector('.dropdown-button');
  const dropdownContent = document.querySelector('.dropdown-content');

  if (dropdownButton && dropdownContent) {
    dropdownButton.addEventListener('click', () => {
      dropdownContent.classList.toggle('show');
    });

    document.addEventListener('click', (event) => {
      if (!dropdownButton.contains(event.target)) {
        dropdownContent.classList.remove('show');
      }
    });
  }

  // Sayfa Bölüm Geçişleri
  window.showSection = (id) => {
    document.querySelectorAll('.section').forEach(section => {
      section.classList.remove('active');
    });
    const target = document.getElementById(id);
    if (target) target.classList.add('active');
  };

  // Admin Formu Gönderimi
  const adminForm = document.getElementById('adminForm');
  if (adminForm) {
    adminForm.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Araç kaydedildi!');
      adminForm.reset();
    });
  }

  // İletişim Formu Gönderimi
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Mesajınız gönderildi!');
      contactForm.reset();
    });
  }

  // API'den Veri Çekme
  const fetchData = async () => {
    try {
      const response = await fetch('https://api.example.com/data'); // Gerçek API adresi
      const data = await response.json();

      const dataContainer = document.getElementById('data-container');
      if (dataContainer && Array.isArray(data)) {
        dataContainer.innerHTML = data.map(item => `
          <div class="data-item">
            <h3>${item.title}</h3>
            <p>${item.description}</p>
          </div>
        `).join('');
      }
    } catch (error) {
      console.error('Veri çekme hatası:', error);
    }
  };
  fetchData();

  // Grafik Gösterimi (Chart.js)
  const chartCanvas = document.getElementById('myChart');
  if (chartCanvas) {
    const ctx = chartCanvas.getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs'],
        datasets: [{
          label: 'Servis Miktarı',
          data: [10, 20, 15, 30, 25],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  }
});
