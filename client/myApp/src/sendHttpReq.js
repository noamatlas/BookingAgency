import axios from "axios";
const nodeServerPath = 'http://127.0.0.1:3500/api/ai/';

export const sendHttpPost = async (userPromptText, addToPath) => {
    const requestedPath = nodeServerPath + addToPath;
    // console.log('requestedPath: ' + requestedPath);
    const config = {
        headers: {
            'Content-Type': 'text/plain'
        }
    };
    try {
        let { data: response } = await axios.post(requestedPath, userPromptText, config);
        return response;
    } catch (error) {
        return error.message;
    }
}

