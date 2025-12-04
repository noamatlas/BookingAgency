const express = require('express');
const usersRouter = require("./routers/usersRouter");
const app = express();
require("dotenv").config();

app.use(require("cors")());
app.use(express.json());


app.use("/api/users", usersRouter);

app.listen(process.env.PORT, () => {
    console.log(`Server is running on port ${process.env.PORT}`);
})