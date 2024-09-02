const express = require('express');
const path = require('path');
const app = express();
const port = 4000;

var http = require('http');
var fs = require('fs');


//npm install dotenv
require('dotenv').config();



const currentDirectory = process.cwd();
// Join the current directory with a subdirectory or file
const pagePath = path.join(currentDirectory, 'dashboard.html');
const homePagePath = path.join(currentDirectory, 'index.html');




// Serve static files from the "public" directory.. JS files sepcifically
app.use(express.static(path.join(__dirname, 'public')));

// allow json to be parsed in API calls (will fail without)
app.use(express.json());


app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "frame-src 'self' http://127.0.0.1:8100/; script-src 'self' http://127.0.0.1; connect-src 'self' http://127.0.0.1"
  );
  next();
});



app.get('/', (req, res) => {
  res.sendFile(homePagePath);
});


app.get('/dashboard', (req, res) => {
  res.sendFile(pagePath);

});




app.post('/verifyAccessCode', (req, res) => {
  console.log('reached api...')
  
  const accessCode = req.body.accessCode;
  
  console.log(process.env.accessCode)
  // Simple logic to verify the access code (you can replace this with your own logic)
  if (accessCode === process.env.accessCode) {
      res.status(200).json({ message: 'Access granted! Redirecting...' });
  } else {
      res.status(400).json({ message: 'Access denied!' });
  }
});



app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});