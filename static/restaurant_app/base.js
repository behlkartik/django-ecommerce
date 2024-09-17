window.addEventListener('DOMContentLoaded', (event) => {
    const toastEl = document.getElementById('cart-toast');
    if (toastEl) {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }
});

// document.querySelector()