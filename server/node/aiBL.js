const axios = require("axios");

const general_AI_path = 'http://127.0.0.1:8000/ask_ai_general';
const travel_AI_path = 'http://127.0.0.1:8000/ask_ai_travel';

// const config = {
//     headers: {
//         'Content-Type': 'text/plain'
//     }
// };

const sendPrompToAI = async (userPromptText, kind) => {
    //kind: "travel", "general"
    const finalPath = kind == "travel" ? travel_AI_path : general_AI_path;
    const config = {
        headers: {
            'Content-Type': 'text/plain'
        }
    };
    try {
        let { data: response } = await axios.post(finalPath, userPromptText, config);
        return response;
    } catch (error) {
        return error.message;
    }
}

module.exports = { sendPrompToAI }
