const sql = require("mssql");

const sqlConnection = async () => {
  const config = {
    user: "test",         // שם המשתמש
    password: "1234",     // הסיסמה
    server: "localhost",  // שם השרת (למשל localhost)
    database: "mydb",     // שם מסד הנתונים
    options: {
      encrypt: true,                  // הצפנה אם נדרש
      trustServerCertificate: true,   // אם אין SSL
    },
  };

  try {
    // יצירת חיבור למסד הנתונים
    const pool = await sql.connect(config);
    return pool; // החזרת החיבור לפונקציות אחרות
  } catch (err) {
    console.error("Error in SQL connection: ", err.message);
    throw new Error("Unable to connect to the database.");
  }
};

module.exports = sqlConnection;