const express = require("express");
AI_routers = require('./agencyRouter.js');
const cors = require("cors");

const app = express();
app.use(cors());

// for JSON bodies
app.use(express.json());

// for text/plain bodies
app.use(express.text());

app.get("/", (req, res) => {
    res.send("Node.js Server is online!");
});

app.use("/api/ai", AI_routers);

app.listen(3500, () => {
    console.log("Node.js Server is runing...");
});



