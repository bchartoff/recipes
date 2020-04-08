function getQueryString(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

$(document).ready(function(){

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
    console.log(recipeCount)
    $(".column_" + String(colNum)).append(html_ele);
    // $(".column_1").append(html_ele);
    html_ele.addClass("trash")
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
      perPage: {
        values: [20],
        container: '#per_page'
      },
    },
    appendToContainer: appendFn
  });

  // FJS.addCallback('beforeAddRecords', function(){
  //   // if(this.recordsCount >= 48){
  //     // this.stopStreaming();
  //   // }
  //   console.log(this.recordsCount)
  // });

  // FJS.addCallback('afterAddRecords', function(){
  //   console.log(this.recordsCount)
  //   var percent = (this.recordsCount - 363)*100/363;

  //   $('#stream_progress').text(percent + '%').attr('style', 'width: '+ percent +'%;');

  //   if (percent == 100){
  //     $('#stream_progress').parent().fadeOut(1000);
  //   }
  // });

  // FJS.setStreaming({
  //   data_url: 'data/streaming_recipes.json',
  //   stream_after: 1,
  //   batch_size: 10
  // });

  // FJS.addCriteria({field: 'year', ele: '#year_filter', type: 'range', all: 'all'});
  // FJS.addCriteria({field: 'rating', ele: '#rating_filter', type: 'range'});
  // FJS.addCriteria({field: 'runtime', ele: '#runtime_filter', type: 'range'});
  // FJS.addCriteria({field: 'genre', ele: '#genre_criteria input:checkbox'});

  /*
   * Add multiple criterial.
    FJS.addCriteria([
      {field: 'genre', ele: '#genre_criteria input:checkbox'},
      {field: 'year', ele: '#year_filter', type: 'range'}
    ])
  */
  var initSearch = getQueryString("search")
  window.FJS = FJS;
  if(initSearch != ""){
    $("#searchbox").val(initSearch)
    FJS.filter()
  }

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
