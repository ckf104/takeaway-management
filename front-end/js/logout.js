$(function () {
  $('#logout').on('click', function () {
    $('html').css('cursor', 'progress')
    $.ajax({
      type: 'POST',
      url: '/auth/logout',
      success: function (data, status) {
        if (data == 'true' && status == 'success') {
          window.location.replace('/login.html')
        }
        else {
          alert(data)
        }
      },
      error: function (jqXHR, status, error) {
        alert('服务器错误, ' + status + ', ' + error)
      },
      complete: function () {
        $('html').css('cursor', 'default')
      }
    })
  })
})