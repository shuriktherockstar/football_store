document.querySelectorAll('.sort-link').forEach(link => {
      link.addEventListener('click', function (event) {
        event.preventDefault();
        const sortValue = this.getAttribute('data-sort');
        const url = `?sort_by=${sortValue}`;

        fetch(url)
          .then(response => response.text())
          .then(data => {
            document.getElementById('product-list').innerHTML = data;
          })
          .catch(error => console.error('Error:', error));
      });
    });

    document.getElementById('filter-form').addEventListener('submit', function (event) {
      event.preventDefault();
      const formData = new FormData(this);
      const url = `?${new URLSearchParams(formData)}`;

      fetch(url)
        .then(response => response.text())
        .then(data => {
          document.getElementById('product-list').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
    });