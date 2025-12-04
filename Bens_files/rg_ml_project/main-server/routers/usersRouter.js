const express = require("express");
const router = express.Router();
const { getAllUsers, createNewUser, getUserById } = require("../Bls/usersBl");

router.get("/", async (req, res) => {
    try {
        const users = await getAllUsers();
        res.json(users);
    } catch (err) {
        res.status(500).send(err.message);
    }
});
router.get("/:id", async (req, res) => {
    try {
        const userId = req.params.id;
        const user = await getUserById(userId);
        res.json(user);
    } catch (err) {
        res.status(500).send(err.message);
    }
});

router.post("/", async (req, res) => {
    let newUser = req.body;
    try {
        const users = await createNewUser(newUser);
        res.json(users);
    } catch (err) {
        res.status(500).send(err.message);
    }
})
module.exports = router;
