  var i,
      s,
      o,
      csv_header,
      unique_category_counts,
      step = 0,
      arbitraryCsvFile="C:\Users\Maximilian\Desktop\Webserver\trittaufmit.csv";

function createGraph(g){
  if (typeof s != "undefined"){
    s.graph.clear();
    s.refresh()
  }

      s = new sigma({
        graph: g,
        container: 'graph-container',
        type: 'webgl',
        settings: {
          labelThreshold:10,
          animationsTime: 4000,
          skipErrors: false,
          //edgeColor:"rgb(255,0,0)",
          //drawEdges:false,
          minNodeSize:0,
          maxNodeSize:0,
        }
      });
 /*not sure how to give options to forceatlas2
  s.forceatlas2.options={ 
  };*/
  s.startForceAtlas2();
}

function generateColorMap(list){
  var cmap={};
  var len = list.length;
  for(var i=0;i<len;i++){
    cmap[list[i]] = "#"+(
      Math.floor(5000000+i*(10777215/len)).toString(16)+ '000000').substr(0,6);
  }
  return cmap;
  
}
function generateVertex(name,i,n,columnColorMap,cell_idx,row_idx){
 return {
          id:  name,
          label: name,
          x: i,
          y: Math.floor(i/csv_header.length),
          size: 6,
          color: columnColorMap[name.split(":")[0]]
        };
}


function csv2graph(body){
 
  var rows = body.split(/\r\n|\n/);
  
  var num_rows = rows.length;
  var vtx_cache={};
  var row,cells;
  num_rows = 600;
  var num_columns = 2;
  var byrow = rows.slice(0,num_rows);
  csv_header = byrow.shift();
  csv_header = csv_header.split(/\,/).slice(0,num_columns);
  var columnColorMap = generateColorMap(csv_header);
  var length = csv_header.length;
  var vtx_id = 0;
  var edge_id = 0;
  var g = { nodes: [], edges: []}
  // for every row
  for(var a in byrow){
    cells = byrow[a].split(/\,/).slice(0,num_columns);
    // for every cell
    for(var i in cells){
      cell_name_a = cells[i];
      //is the vertex unique?
      if(typeof vtx_cache[cell_name_a] === "undefined"){
        o = generateVertex(cell_name_a, ++vtx_id, num_rows, columnColorMap, i,a );
        vtx_cache[cell_name_a] = i;
        // apply basic attributes
        g.nodes.push(o
          /*{ previous version of pushing the attributes in the nodes.
          id:  cells[i],
          label: cells[i],
          x: i,
          y: Math.floor(i/csv_header.length),
          size: 6,
          //color: columnColorMap[name.split(":")[0]]
        }*/);
      }
      // n choose 2 cells in a row
      for(var j=length-1; j > i; j--){ 
        g.edges.push({
          id: 'e'+edge_id++,
          source: cell_name_a,
          target: cells[j],
        });
      }   
    }
  }
  return g;
}


$('#start-force').click(function(){
  s.startForceAtlas2();
});
$('#stop-force').click(function(){
  s.stopForceAtlas2();
});
$('#clear').click(function(){
  s.graph.clear();
  s.refresh();
});


$.get(arbitraryCsvFile,function(body){
  createGraph(csv2graph(body));
});

function handleFileSelect(e) {
  if (e.target.files != undefined) {
    var reader = new FileReader();
    reader.onload = function(e) {
      createGraph(csv2graph(e.target.result));
    };
    reader.readAsText(e.target.files.item(0));
  }
 }


document.getElementById('file').addEventListener('change', handleFileSelect, false);