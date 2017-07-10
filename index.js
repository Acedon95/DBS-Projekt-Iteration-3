/*
  missing: copy code from simajs.org to add event for mouse click on node 
*/
//first a few variables:
  var i,
      s,
      o,
      csv_header,
      unique_category_counts,
      step = 0,
      arbitraryCsvFile="C:\Users\Maximilian\Desktop\Webserver\trittaufmit.csv";
//create graph 
function createGraph(g){
  if (typeof s != "undefined"){
    s.graph.clear();
    s.refresh()
  }

      s = new sigma({ //just like sigma's examples
        graph: g,
        container: 'graph-container',
        type: 'webgl',
        settings: {
          labelThreshold:10,
          animationsTime: 4000,
          skipErrors: true, //just getting it to work
          minNodeSize:0,
          maxNodeSize:0,
        }
      });
 /*not sure how to give options like better gravity to forceatlas2
  s.forceatlas2.options={ here you can add better gravity options for better clustergenerating
  };*/
  s.startForceAtlas2();
}

function generateVertex(name,i,n,cell_idx,row_idx){
 return {
          id:  name,
          label: name,
          x: i,
          y: Math.floor(i/csv_header.length),
          size: 6,
          //color: add color code with #int here if wanted and update it above
        };
}

//didn't knew how to create a json or gexf so it's done here...
function csv2graph(body){ 
 
  var rows = body.split(/\r\n|\n/); //split rows by this <--
  var num_rows = rows.length;
  var vtx_cache={};
  var row,cells;
  num_rows = 666; //just checking that our index won't run out of rows ;) (nuber of rows of .csv data)
  var num_columns = 2; //select here, from which rows u wanna get you r data 
  var byrow = rows.slice(0,num_rows);
  csv_header = byrow.shift();
  csv_header = csv_header.split(/\,/).slice(0,num_columns); //.split(select your delimiter here and in line 66!)
  var length = csv_header.length;
  var vtx_id = 0;
  var edge_id = 0;
  var g = { nodes: [], edges: []} //format .json wants 
  
  // for every row
  for(var a in byrow){
    cells = byrow[a].split(/\,/).slice(0,num_columns); //seperate all cells 
    // for every cell
    for(var i in cells){
      cell_name_a = cells[i];
      //is the vertex unique?
      if(typeof vtx_cache[cell_name_a] === "undefined"){
        o = generateVertex(cell_name_a, ++vtx_id, num_rows, i,a );
        vtx_cache[cell_name_a] = i;
        // apply attributes to the nodes
        g.nodes.push(o
          /*{ previous version of pushing the attributes in the nodes without use of vertex!
          id:  cells[i],
          label: cells[i],
          x: i,
          y: Math.floor(i/csv_header.length),
          size: 6,
          color: columnColorMap[name.split(":")[0]]
        }*/);
      }
      // n choose 2 cells in a row for an edge
      for(var j=length-1; j > i; j--){ 
        g.edges.push({
          id: 'e'+edge_id++,
          source: cell_name_a,
          target: cells[j],
        });
      }   
    }
  }
  return g; //here is finally our graph g wich is needed for plotting with sigma
}

//just some button functions:

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