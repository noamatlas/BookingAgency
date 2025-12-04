const sqlConnection = require("../config/sql-connection");

const getAllUsers = async () => {
    let pool;
    try {
        // חיבור למסד הנתונים
        pool = await sqlConnection();

        // ביצוע שאילתת SQL
        const result = await pool.request().query("SELECT * FROM users");

        // החזרת התוצאות
        return result.recordset;
    } catch (err) {
        // טיפול בשגיאות
        throw new Error("SQL Error: " + err.message);
    } finally {
        // סגירת החיבור בסוף
        if (pool) await pool.close();
    }
};

const getUserById = async (userId) => {
    let pool;
    try {
        // חיבור למסד הנתונים
        pool = await sqlConnection();

        // ביצוע שאילתת SQL

        if(!isNaN(userId)){
            const result = await pool.input("id", sql.Int, userId)
            return result.recordset[0];
        }else{
            throw new Error("Invalid User ID");
        }
    } catch (err) {
        // טיפול בשגיאות
        throw new Error("SQL Error: " + err.message);
    } finally {
        // סגירת החיבור בסוף
        if (pool) await pool.close();
    }
};


const createNewUser = async (newUser) => {
    let pool;
    let { username, password, email } = newUser;
    try {
        pool = await sqlConnection();
        await pool.request().query(`insert into users (user_name, user_password, email) 
            values ('${username}', '${password}', '${email}')`);
        return "User Created Successfully!";
    } catch (err) {
        throw new Error("SQL Error: " + err.message);
    } finally {
        if (pool) await pool.close();
    }
};

module.exports = { getAllUsers, createNewUser , getUserById };