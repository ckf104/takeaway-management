//const jquery361 = require("./jquery-3.6.1");

$(function () {
  $.ajax({
    type: 'GET',
    url: 'https://v1.hitokoto.cn/?c=a',
    dataType: 'jsonp',
    jsonp: 'callback',
    success(data) {
      let j = JSON.parse(data)
      $('#hitokoto_text').text(j.hitokoto)
      $('#hitokoto_source').text("—————" + j.from)
    },
    error(jqXHR, textStatus, errorThrown) {
      // 错误信息处理
      console.error(textStatus, errorThrown)
    }
  })
  //$("#source").
})
