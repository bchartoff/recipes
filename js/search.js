function getQueryString(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

$(document).ready(function(){
  var initSearch = getQueryString("search")
  var pageNum = getQueryString("page") == "" ? "1" : getQueryString("page")
  // initSliders();

  // //NOTE: To append in different container
  // var appendToContainer = function(htmlele, record){
  //   console.log(record)
  // };

  var beforeRender = function(records){
    // console.log(record)
    // record.trash = true;
    // $(record).addClass("trash")
    // console.log("foo")
    // $(".trash").remove()
    // console.log(records)

  }

  var recipeCount = 0;

  var afterFilter = function(result, jQ){
    // $(".thumbnail").remove()
    // $(":not(.trash").remove()
    // console.log(result)
    // result.map(function(o){ o.trash = "narp" })
    // this.removeRecords([1])
    recipeCount = 0;
    $('#total_recipes').text(result.length);
  }

  var appendFn = function(html_ele, record) {
    // console.log(html)
    // record.trash = false;
    // console.log(record)
    // console.log(record)
    var colNum = ((recipeCount-1)%3) + 1
    recipeCount += 1
    $(".column_" + String(colNum)).append(html_ele);
    // $(".column_1").append(html_ele);
  }

  var FJS = FilterJS(recipes, ".results_column", {
    template: '#recipe-template',
    
    search: { ele: '#searchbox' },
    //search: {ele: '#searchbox', fields: ['runtime']}, // With specific fields
    callbacks: {
      afterFilter: afterFilter
      // beforeAddRecords: beforeRender
    },
    pagination: {
      container: '#pagination',
      visiblePages: 5,
      startPage: pageNum,
      perPage: {
        values: [20],
        container: '#per_page'
      },
    },
    appendToContainer: appendFn
  });


  if(pageNum != 1){
    var Paginator = FJS.paginator
    Paginator.setCurrentPage(+pageNum)
  }
  window.FJS = FJS;
  if(initSearch != ""){
    $("#searchbox").val(initSearch)
    FJS.filter()
  }

  // FJS.page = { currentPage: 12, perPage: 20 };
  // FJS.renderPagination(40)

});


// function initSliders(){
//   $("#rating_slider").slider({
//     min: 0,
//     max: 5,
//     values:[0, 5],
//     step: 0.1,
//     range:true,
//     slide: function( event, ui ) {
//       $("#rating_range_label" ).html(ui.values[ 0 ] + ' - ' + ui.values[ 1 ]);
//       $('#rating_filter').val(ui.values[0] + '-' + ui.values[1]).trigger('change');
//     }
//   });


//   // $('#genre_criteria :checkbox').prop('checked', true);
//   // $('#all_genre').on('click', function(){
//   //   $('#genre_criteria :checkbox').prop('checked', $(this).is(':checked'));
//   // });
// }
