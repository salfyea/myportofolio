let toastTimeoutId = null;

function showToast(title, message, type = 'normal', duration = 3000) {
    const toast = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');

    if (!toast || !toastTitle || !toastMessage) {
        return;
    }

    toast.classList.remove('toast-success', 'toast-error', 'toast-normal');

    if (type === 'success') {
        toast.classList.add('toast-success');
    } else if (type === 'error') {
        toast.classList.add('toast-error');
    } else {
        toast.classList.add('toast-normal');
    }

    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // Reset the timer so a new toast is not closed early by the previous one.
    clearTimeout(toastTimeoutId);

    if (!toast.matches(':popover-open')) {
        toast.showPopover();
    }

    toastTimeoutId = setTimeout(function () {
        if (toast.matches(':popover-open')) {
            toast.hidePopover();
        }
    }, duration);
}
