const router = require("express").Router();
const { sendPrompToAI } = require('./aiBL.js');

router.post("/ai_general", async (req, res) => {
    let prompt = req.body;
    let response = await sendPrompToAI(prompt, 'general');
    res.send(response)
});

router.post("/ai_travel", async (req, res) => {
    let prompt = req.body;
    let response = await sendPrompToAI(prompt, 'travel');
    res.send(response)
});

module.exports = router;




