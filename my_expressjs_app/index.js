// Install Node.js:
// https://nodejs.org/en

// Install Express.js:
// http://expressjs.com/en/starter/installing.html
// $ npm install express

// Run this app:
// http://expressjs.com/en/starter/hello-world.html
// Run the app with the following command: $ node index.js

const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('req.query.uname: ' + JSON.stringify(req.query.uname) + '<br>req.query.pw: ' + JSON.stringify(req.query.pw))
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
