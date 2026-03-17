/* ============================================
   PlantGuard AI — main.js
   jQuery + Vanilla JS frontend logic
   ============================================ */

$(document).ready(function () {

  /* ── 1. Dark Mode Toggle ───────────────────── */
  const $html      = $('html');
  const $toggle    = $('#darkModeToggle');
  const savedTheme = localStorage.getItem('theme') || 'light';

  // Apply saved theme on load
  $html.attr('data-theme', savedTheme);
  if (savedTheme === 'dark') $toggle.prop('checked', true);

  $toggle.on('change', function () {
    const theme = $(this).is(':checked') ? 'dark' : 'light';
    $html.attr('data-theme', theme);
    localStorage.setItem('theme', theme);
  });


  /* ── 2. File Input & Drag-Drop ─────────────── */
  const $fileInput   = $('#fileInput');
  const $dropZone    = $('#dropZone');
  const $fileInfo    = $('#fileInfo');
  const $fileName    = $('#fileName');
  const $fileSize    = $('#fileSize');
  const $previewCont = $('#previewContainer');
  const $previewImg  = $('#previewImg');
  const $analyzeBtn  = $('#analyzeBtn');
  const $removeBtn   = $('#removeFile');
  const $formError   = $('#formError');
  const $errorMsg    = $('#errorMsg');

  let selectedFile = null;

  // Click on drop zone → trigger file input
  $dropZone.on('click', function () {
    $fileInput.trigger('click');
  });

  // File chosen via browse
  $fileInput.on('change', function () {
    if (this.files && this.files[0]) {
      handleFile(this.files[0]);
    }
  });

  // Drag events
  $dropZone.on('dragover dragenter', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).addClass('dragover');
  });

  $dropZone.on('dragleave dragend drop', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).removeClass('dragover');
  });

  $dropZone.on('drop', function (e) {
    const files = e.originalEvent.dataTransfer.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  });

  // Remove file
  $removeBtn.on('click', function (e) {
    e.stopPropagation();
    resetUpload();
  });


  /* ── 3. Handle File ────────────────────────── */
  function handleFile(file) {
    clearError();

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      showError('Invalid file type. Please upload a JPG, PNG, or WEBP image.');
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      showError('File is too large. Maximum size is 10MB.');
      return;
    }

    selectedFile = file;

    // Show file info
    $fileName.text(file.name);
    $fileSize.text(formatFileSize(file.size));
    $fileInfo.removeClass('d-none');

    // Preview image
    const reader = new FileReader();
    reader.onload = function (e) {
      $previewImg.attr('src', e.target.result);
      $previewCont.removeClass('d-none');
    };
    reader.readAsDataURL(file);

    // Enable analyze button
    $analyzeBtn.prop('disabled', false);
    $dropZone.find('.drop-title').text(file.name.length > 30 ? file.name.substring(0, 30) + '...' : file.name);
  }

  function resetUpload() {
    selectedFile = null;
    $fileInput.val('');
    $fileInfo.addClass('d-none');
    $previewCont.addClass('d-none');
    $previewImg.attr('src', '');
    $analyzeBtn.prop('disabled', true);
    $dropZone.find('.drop-title').text('Drag & Drop your leaf image here');
    clearError();
  }


  /* ── 4. Form Validation on Submit ─────────── */
  $('#uploadForm').on('submit', function (e) {
    clearError();

    // Check if file is selected
    if (!selectedFile) {
      e.preventDefault();
      showError('Please select a leaf image before analyzing.');
      return false;
    }

    // Double-check file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(selectedFile.type)) {
      e.preventDefault();
      showError('Invalid file type. Only JPG, PNG, and WEBP are allowed.');
      return false;
    }

    // Double-check file size
    if (selectedFile.size > 10 * 1024 * 1024) {
      e.preventDefault();
      showError('File exceeds 10MB limit.');
      return false;
    }

    // Show loading state on button
    $analyzeBtn.prop('disabled', true).html(
      '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Analyzing...'
    );

    return true; // allow form submission
  });


  /* ── 5. Helper Functions ───────────────────── */
  function showError(msg) {
    $errorMsg.text(msg);
    $formError.removeClass('d-none');
    // Scroll to error
    $('html, body').animate({ scrollTop: $formError.offset().top - 100 }, 300);
  }

  function clearError() {
    $formError.addClass('d-none');
    $errorMsg.text('');
  }

  function formatFileSize(bytes) {
    if (bytes < 1024)       return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  }


  /* ── 6. Smooth Scroll for Anchor Links ─────── */
  $('a[href^="#"]').on('click', function (e) {
    const target = $(this.getAttribute('href'));
    if (target.length) {
      e.preventDefault();
      $('html, body').animate({ scrollTop: target.offset().top - 80 }, 500);
    }
  });


  /* ── 7. Auto-dismiss alerts after 5s ───────── */
  setTimeout(function () {
    $('.alert-dismissible').fadeOut(500, function () {
      $(this).remove();
    });
  }, 5000);


  /* ── 8. Animate elements on scroll ─────────── */
  function revealOnScroll() {
    $('.step-card, .plant-chip, .tip-card').each(function () {
      const top    = $(this).offset().top;
      const bottom = $(window).scrollTop() + $(window).height();
      if (top < bottom - 50) {
        $(this).addClass('visible');
        $(this).css({ opacity: 1, transform: 'translateY(0)' });
      }
    });
  }

  // Initial hide for scroll-reveal elements
  $('.step-card, .tip-card').css({ opacity: 0, transform: 'translateY(20px)', transition: 'all 0.5s ease' });

  $(window).on('scroll', revealOnScroll);
  revealOnScroll(); // Run on page load too


  /* ── 9. Tooltip initialization ─────────────── */
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

});
