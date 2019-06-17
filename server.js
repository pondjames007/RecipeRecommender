// Create server
let port = process.env.PORT || 8000;
let express = require('express');
let app = express();
let server = require('http').createServer(app).listen(port, function () {
  console.log('Server listening at port: ', port);
});

// Tell server where to look for files
app.use(express.static('public'));

// Create socket connection
let io = require('socket.io').listen(server);


const util = require('util');
const exec = util.promisify(require('child_process').exec);
const fs = require('fs');


// Listen for individual clients to connect
io.sockets.on('connection',
  // Callback function on connection
  // Comes back with a socket object
  function (socket) {

    console.log("We have a new client: " + socket.id);

    // Listen for username
    // Stick the username on the socket object
    socket.on('recipeName', (recipeName)=>{

        runPyScripts(recipeName.filename, socket);

        
        
    })

    // Listen for this client to disconnect
    socket.on('disconnect', function () {
      console.log("Client has disconnected " + socket.id);
    });
  }
);

async function runPyScripts(filename, socket){
  let command = "python3 recipe.py -i " + filename;
  const response1 = await exec(command);
  console.log(response1.stdout);

  const keywords = await fs.readFileSync('public/keywords.txt', 'utf-8');
  console.log(keywords);

  const send_keywords = await socket.emit('keywords', keywords);

  command = 'python3 useownimg.py -i ' + filename + ' -o output.jpg'
  console.log(command)
  const response2 = await exec(command);
  console.log(response2.stdout);

  let message = {
    inputImages: filename.split(',')
  }

  const msg_to_client = await socket.emit('message', message);

  return 'All Done'
}